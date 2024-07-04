# APK downloader using Android Debug Bridge
This repository provides some scripts use in bachelor thesis to get APK of Android application by installing them in an emulator and then pulling them into the computer. A brief explaination of each file provided will follow.

In order to use these scripts you must have Python 3.6+, Java 8+ and Android SDK platform tools (that provides adb) installed in your system, along with others packages that will be listed later.

### adb-downloader.py
The main script that allows for retrieving APK from emulator. The script collects the package names of applications in ```appnames.txt``` if it is not empty (otherwise it retrieve packages from ```packages.txt```), then access the Play Store in application details page and performs a tap to start app installation. Once it is completed, it pulls the APK(s) into the computer and, if necessary, merges them in a single file, then uninstall the app from the device.
If you want to skip installation, add ```--skip-install``` when running. 

To get things work, you need apktool version 2.9.3+ and some packages from pip. The required packages are:
+ pure-python-adb
+ beautifulsoup4
+ requests
which can be found in file ```adb-requirements.txt```.

### apktool-extractor.py
This script was used to massively *reverse-engineer* the APKs in a directory with apktool. It requires apktool version 2.9.3+.

### fast-pull.py
Allows pulling a single package from emulator.

### jar-downloader.py
Downloads a file from the given URL, it is used to download libraries version files from Maven Central.

### match-finder.py
This script finds the matching paths in some reverse-engineered APKs, exploring ```smali_classes``` subdirectories tree and comparing the paths pairwise to find common libraries in APKs. 
