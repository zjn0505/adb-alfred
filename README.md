# adb-alfred [![release](https://img.shields.io/github/release/zjn0505/adb-alfred.svg)](https://github.com/zjn0505/adb-alfred/releases/latest)
![logo](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/adb%20alfred.png)

adb with alfred workflow

Keywords
----

`adb`, `apk`, `avd`


Dependencies
----
- [adb](https://developer.android.com/studio/command-line/adb)
- [aapt](https://developer.android.com/studio/command-line/aapt2)
- [emulator](https://developer.android.com/studio/run/emulator-commandline)

These dependencies are included in Android Studio and Android command line tools. [link](https://developer.android.com/studio/#downloads)

Configurations
----

Add the path of the executable files of dependencies to workflow settings.

Here is a screenshot of my configurations.

![Workflow config screenshot](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/configs.png)

What's required:

|Name|Value (example)|
|--|--|
|`adb_path`|~/Library/Android/sdk/platform-tools/adb|
|`aapt_path`|~/Library/Android/sdk/build-tools/28.0.3/aapt|
|`emulator_path`|~/Library/Android/sdk/emulator/emulator|

Features
----
- `adb` to list connected devices

  - `adb connect`, `adb disconnect` `adb restart` can also be accessed from root level

![list devices](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2001%20list%20devices.png)

- select one connected device for device options

  - Input custom commands like `shell dumpsys -l | grep wifi` to execute directly in terminal

![device options](https://github.com/zjn0505/adb-alfred/raw/master/art/screenshot%2002%20show%20device%20options.png)

- select `Show app list` in device options to list and search in all installed applications

  - select one application to show package options
  
![package options](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2003%20show%20package%20options.png)

- select `Install apk` in device options to select APK or APKs on local drive for installation

  - `adb install -t -d -g` and bulk installation
  
![install options](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2004%20show%20install%20options.png)

- `apk` to search for local apk files, and check package info

- `avd` to list installed emulators, select one to start an emulator

References
------
- [109021017/alfred-adb-workflow](https://github.com/109021017/alfred-adb-workflow)

- [nassendelft/alfred-android-adb](https://github.com/nassendelft/alfred-android-adb)
