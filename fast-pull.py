from ppadb.client import Client as AdbClient
import os
from subprocess import *

destination_path = "C:\\Users\\denno\\Desktop\\Tesi\\apks\\"
package = 'com.justplay.app'

def pull_apk(phone, package, paths):
    
    local_path = destination_path + package + (os.sep + "parts" if len(paths) > 1 else "")
    os.makedirs(local_path, exist_ok=True)
    
    for device_path in paths:
        print("Pulling from " + device_path)
        cmd = "adb pull " + device_path + " " + local_path
        p = os.system(cmd)
        os.rename(local_path + os.sep + "base.apk", local_path + os.sep + package + ".apk") if len(paths) == 1 else None

def merge_apks(package):
    parts_path = destination_path + package + os.sep + "parts"
    merged_path = destination_path + package + os.sep
    cmd = "java -jar APKEditor.jar m -i " + parts_path
    os.system(cmd)
    os.rename(merged_path + "parts_merged.apk", merged_path + package + ".apk")


def main_tat():
    adb = AdbClient(host='localhost', port=5037)
    phone = adb.devices()[0]
    
    paths = phone.shell('pm path ' + package)
    print(paths)
    try:
        for device_path in paths.splitlines():
            device_path = device_path.split(':')[-1].strip()
            print(device_path)
            local_path = destination_path + package
            print(local_path)
            os.makedirs(local_path, exist_ok=True)
            cmd = "adb pull " + device_path + " " + local_path
            os.system(cmd)
    except Exception as e:
        print("Error ", str(e))
            
    input("Press Enter to continue...")
    
def main():
    adb = AdbClient(host='localhost', port=5037)
    phone = adb.devices()[0]
    paths = phone.shell('pm path ' + package).splitlines()
    paths = [p.split(':')[-1].strip() for p in paths]
    pull_apk(phone, package, paths)
            
    if len(paths) > 1:
        merge_apks(package)
        print("Merged " + package)

    
if __name__ == '__main__':
    main()