# adb-alfred [![release](https://img.shields.io/github/release/zjn0505/adb-alfred.svg)](https://github.com/zjn0505/adb-alfred/releases/latest) [![Build Status][1]][2] ![Total downloads][3]

[1]: 
https://app.bitrise.io/app/48bd64d386f7c944/status.svg?token=5M-EP8LTG0wjJSKcqCoSew&branch=master "Bitrise build status icon"
[2]: https://app.bitrise.io/app/48bd64d386f7c944#/builds "Bitrise build page"
[3]: https://img.shields.io/github/downloads/zjn0505/adb-alfred/total.svg "Total downloads"
![logo](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/adb%20alfred.png)

adb with alfred workflow

Android developers may need to work on 
  - multiple connected devices
  - devices beyound your arm's reach
  - devices without hard and soft navigation buttons
  - or need to clear app data 200 times a day
  
then this workflow is very handy for them, as most `adb -s {serial} shell` commands can be done within 10 keystrokes in alfred.

Keywords
----

`adb`, `apk`, `apkf`, `avd`, `geny`


Dependencies
----

These dependencies are included in Android Studio and Android command line tools. [link](https://developer.android.com/studio/#downloads)

- [adb](https://developer.android.com/studio/command-line/adb)
- [aapt](https://developer.android.com/studio/command-line/aapt2)
- [emulator](https://developer.android.com/studio/run/emulator-commandline)
- [apksigner](https://developer.android.com/studio/command-line/apksigner) (optional)

Other optional but powerful widgets this workflow uses

- [scrcpy](https://github.com/Genymobile/scrcpy)  - screen mirror, control device from your mac
- [Genymotion](https://www.genymotion.com/) - Genymotion emulators can be listed and launched with adb-alfred

Configurations
----

Add the path of the executable files of dependencies to workflow settings.

Here is a screenshot of my configurations.

![Workflow config screenshot](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/configs.png)

What's required:

|Name|Value (example)|
|--|--|
|`adb_path`|~/Library/Android/sdk/platform-tools/adb|
|`aapt_path`|~/Library/Android/sdk/build-tools/29.0.2/aapt|
|`emulator_path`|~/Library/Android/sdk/emulator/emulator|

What's optional:

|Name|Value (example)|
|--|--|
|`apksigner_path`|~/Library/Android/sdk/build-tools/29.0.2/apksigner|
|`config_clipboard`|`1` to copy some outputs to clipboard|

Features
----
- `adb` to list connected devices

  - `adb connect`, `adb disconnect` `adb restart` can also be accessed from root level
  
  - devices have modifiers to run history commands

![list devices](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2001%20list%20devices.png)

- select one connected device for device options

  - input custom commands like `shell dumpsys -l | grep wifi` to execute directly in terminal
  
  - select from options like 'app list', 'debug layout', 'screenshot', 'dump task stack', etc.
  
  - most options have modifiers for quick control.

![device options](https://github.com/zjn0505/adb-alfred/raw/master/art/screenshot%2002%20show%20device%20options.png)

- select `Show app list` in device options to list and search in all installed applications

  - select one application to show package options
  
![package options](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2003%20show%20package%20options.png)

- select `Install apk` in device options to select APK or APKs on local drive for installation

  - `adb install -t -d -g` and bulk installation
  
  - apk signature info will be listed
  
![install options](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2004%20show%20install%20options.png)

- `apk` to search for local apk files, and check package info

  - `apkf` to directly list apk files under current front Finder window

  - custom hotkey to open current selected apk file

- `avd` to list installed emulators, select one to start an emulator

  - modifier keys to do cold boot, or wipe emulator data

References
------
- [109021017/alfred-adb-workflow](https://github.com/109021017/alfred-adb-workflow)

- [nassendelft/alfred-android-adb](https://github.com/nassendelft/alfred-android-adb)
