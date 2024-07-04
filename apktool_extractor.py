import os
import subprocess
import time

apks_dir = os.getcwd() + os.sep + "apktool_apks" + os.sep

def main():
    processes = 0
    active_processes = []
    files_list = []
    print(apks_dir)
    for root, dirs, files in os.walk(apks_dir):
        print(files)
        for file in files:
            if file.endswith(".apk"):
                files_list.append(apks_dir + file)
               
                
    while processes < len(files_list):
        if len(active_processes) < 4:
            file = files_list.pop(0)
            print("Extracting " + file + "...")
            cmd = "apktool d " + file + " -o " + file[:-4]
            active_processes.append(subprocess.Popen(cmd, shell=True))
            print("Extraction of " + file + " complete.")
        
        for process in active_processes:
            if process.poll() is not None:
                active_processes.remove(process)
                processes += 1
        
        time.sleep(10)

if __name__ == "__main__":
    main()