# adb-alfred [![release](https://img.shields.io/github/release/zjn0505/adb-alfred.svg)][4] [![Build Status][1]][2] [![Total downloads][3]][4]

[1]: 
https://app.bitrise.io/app/48bd64d386f7c944/status.svg?token=5M-EP8LTG0wjJSKcqCoSew&branch=master "Bitrise build status icon"
[2]: https://app.bitrise.io/app/48bd64d386f7c944#/builds "Bitrise build page"
[3]: https://img.shields.io/github/downloads/zjn0505/adb-alfred/total.svg "Total downloads"
[4]: https://github.com/zjn0505/adb-alfred/releases/latest

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
  
<details><summary> <b>Full features at this level</b> </summary>

|Feature|Trigger|
|:--|:--|
|Check all connected devices|`adb` or hotkey|
|Check ip address of connected device|`adb` + `cmd` (emulators and wireless connected devices excluded)|
|Copy device serial to clipboard|`adb` + `cmd` + `c`|
|Check device system info|`adb` + `option`|
|Re-run last used command on one device|`adb` + `ctrl`|
|Check history commands of one device|`adb` + `fn`|
|Check wireless connection history|`adb connect`|
|Clear wireless connection history|`adb connect` + `cmd`|
|Connect to device wirelessly|`adb connect {ip}:{port}`|
|Remove wireless connection history of one device|`adb connect` + `cmd` on device|
|Disconnect wireless devices|`adb disconnect`|

</details>

![list devices](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2001%20list%20devices.png)

- select one connected device for device options

  - input custom commands like `shell dumpsys -l | grep wifi` to execute directly in terminal
  
  - select from options like 'app list', 'debug layout', 'screenshot', 'dump task stack', etc.
  
  - most options have modifiers for quick control.
  
<details><summary> <b>Full features at this level</b> </summary>

|Feature|Trigger|
|:--|:--|
|Custom command in terminal|input directly, e.g. `shell dumpsys -l \| grep wifi`|
|Custom command silently|input + `cmd`|
|Show history command|`Command history`|
|Clear history command|`Command history` + `cmd`|
|Show applications list|`Show apps list`|
|Select app to launch|`Show apps list` + `cmd`|
|Select app to uninstall|`Show apps list` + `option`|
|Select app to force stop|`Show apps list` + `ctrl`|
|Select app to clear data|`Show apps list` + `fn`|
|Select app to show app info|`Show apps list` + `shift`|
|Install apk or all apks in folder|`Install apk`|
|Take screenshot to clipboard|`Take screenshot`|
|Take screenshot to desktop|`Take screenshot` + `cmd`|
|Open settings|`Open settings`|
|Open developer tools|`Open settings` + `cmd`|
|Open WiFi settings|`Open settings` + `option`|
|Open application settings|`Open settings` + `ctrl`|
|Open date settings|`Open settings` + `fn`|
|Open accessibility settings|`Open settings` + `shift`|

</details>

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

Full feature list
------

<details><summary> in this workflow  </summary>
  
  
  
|Function|Trigger|
|:--|:--|
|Check all connected devices|`adb` or hotkey|
|Check ip address of connected device|`adb` + `cmd` (emulators and wireless connected devices excluded)|
|Copy device serial to clipboard|`adb` + `cmd` + `c`|
|Check device system info|`adb` + `option`|
|Re-run last used command on one device|`adb` + `ctrl`|
|Check history commands of one device|`adb` + `fn`|
|Check wireless connection history|`adb connect`|
|Clear wireless connection history|`adb connect` + `cmd`|
|Connect to device wirelessly|`adb connect {ip}:{port}`|
|Remove wireless connection history of one device|`adb connect` + `cmd` on device|
|Disconnect wireless devices|`adb disconnect`|

    
  

</details>
