from ppadb.client import Client as AdbClient # Import the ppadb library
import os # Import the os library
import time
import argparse
import requests
from bs4 import BeautifulSoup

MAX_WAIT_TIME = 300 # 5 seconds

destination_path = os.getcwd() + os.sep + "apks" + os.sep # Set the destination path for the APKs

def download_apk(phone, package):
    if os.path.exists(destination_path + package):
        print(package + "APK already downloaded")
        return
    # phone.shell('am start -W -a android.intent.action.VIEW -d "market://details?id=' + package + '"')
    phone.shell('am start -W -a android.intent.action.VIEW -d "https://play.google.com/store/apps/details?id=' + package + '"')
    time.sleep(8)
    # tries with two taps because the position depends on the app info
    phone.shell('input tap 500 770')
    phone.shell('input tap 500 820')
    time.sleep(3)
    print("Started download of " + package)
    
    
def pull_apk(package, paths):
    
    local_path = destination_path + package + (os.sep + "parts" if len(paths) > 1 else "")
    if os.path.exists(local_path):
        print(package + " APK already pulled")
        return
    os.makedirs(local_path, exist_ok=True)
    
    for device_path in paths:
        print("Pulling from " + device_path + " " + local_path)
        cmd = "adb pull " + device_path + " " + local_path
        p = os.system(cmd)
        apk_name = device_path.split("/")[-1]
        os.rename(local_path + os.sep + apk_name, local_path + os.sep + package + ".apk") if len(paths) == 1 else None

def merge_apks(package):
    parts_path = destination_path + package + os.sep + "parts"
    merged_path = destination_path + package + os.sep
    cmd = "java -jar APKEditor.jar m -i " + parts_path
    os.system(cmd)
    os.rename(merged_path + "parts_merged.apk", merged_path + package + ".apk")
    
def get_tag_from_url(url, tag_name):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tag = soup.find('a', class_='Qfxief')
        if tag:
            return tag['href']
        else:
            print(f"No {tag_name} tag found with the specified class in the HTML.")
            return None
    else:
        print(f"Failed to fetch URL. Status code: {response.status_code}")
        return None

def main(skip_download=False):
    # create a new ADB Client
    adb = AdbClient(host='localhost', port=5037)
    print(adb.devices()[0].serial)
    phone = adb.devices()[0]
    packages = []
    
    with open('appnames.txt', 'r') as file:
        appnames = file.read().splitlines()

    for appname in appnames:
        url = f"https://play.google.com/store/search?q={appname}&c=apps"
        tag_name = "a"
        result = get_tag_from_url(url, tag_name)
        if result is None or 'id=' not in result:
            continue
        result = result.split('id=')[1]
        packages.append(result)

    if appnames is None or len(appnames) == 0:   
        # read the package names from the file
        packages = []
        with open('packages3.txt', 'r') as file:
            packages = file.read().splitlines()
    
    if not skip_download:    
        for package in packages:
            download_apk(phone, package)
        
        time.sleep(10)
        
    packages_left = packages.copy()
    uninstallable_packages = []
    start_time = time.time()
    elapsed = 0
    
    # Loops untill all the packages are downloaded or the MAX_WAIT_TIME is reached
    while len(packages_left) > 0 and elapsed < MAX_WAIT_TIME:
        elapsed = time.time() - start_time
        package = packages_left.pop(0)
        paths = phone.shell('pm path ' + package).splitlines()
        
        local_path = destination_path + package + (os.sep + "parts" if len(paths) > 1 else "")
        if os.path.exists(local_path):
            print(package + " already collected")
            continue
        
        if len(paths) == 0 :
            time.sleep(2)
            packages_left.append(package)
            continue
        
        paths = [p.split(':')[-1].strip() for p in paths]
        pull_apk(package, paths)
        uninstallable_packages.append(package)
            
        if len(paths) > 1:
            merge_apks(package)
            print("Merged " + package)
        
        time.sleep(5)
        
        if len(uninstallable_packages) > 0:
            package = uninstallable_packages.pop(0)
            cmd = 'adb uninstall ' + package
            os.system(cmd)
            
        start_time = time.time()
        
        
    if len(packages_left) > 0:
        print("Some packages could not be downloaded: " + str(packages_left))
            
    
    # Move the apks to the final directory
    output_dir = None
    if output_dir is None:
        output_dir = os.getcwd() + os.sep + "final_apks"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for dir in os.listdir(destination_path):
            if (os.path.exists(destination_path + dir + os.sep + dir + ".apk")):
                os.replace(destination_path + dir + os.sep + dir + ".apk", output_dir + os.sep + dir + ".apk")
        
        
        
    print("Download completed")
    print("Apks are stored in " + output_dir)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='APK Downloader')
    parser.add_argument('--skip-download', action='store_true', help='Output directory for APKs')
    args = parser.parse_args()

    main(args.skip_download)