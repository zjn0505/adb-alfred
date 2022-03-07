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

- [scrcpy](https://github.com/Genymobile/scrcpy)  - screen mirror, screen recording, control device from your mac
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

What's customizable:

|Name|Value (example)|
|--|--|
|`self_script_app_` + `{number}`|Open in Google Play\|self_scripts/open_in_google_play.py|
|`self_script_device_` + `{number}`|Toggle Airplane Mode\|self_scripts/toggle_airplane_mode.py|

see  [Self script customization](#self-script-customization)

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
|Re-run second last used command on one device|`adb` + `shift`|
|Check history commands of one device|`adb` + `fn`|
|Check wireless connection history|`adb connect`|
|Clear wireless connection history|`adb connect` + `cmd`|
|Connect to device wirelessly|`adb connect {ip}:{port}`|
|Remove wireless connection history of one device|`adb connect` + `cmd` on device|
|Disconnect wireless devices|`adb disconnect`|
|Restart adb service|`adb restart`|

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
|Toggle debug layout|`Toggle debug layout`|
|Toggle pointer location|`Toggle debug layout` + `cmd`|
|Toggle show taps|`Toggle debug layout` + `option`|
|Toggle GPU profile|`Toggle debug layout` + `ctrl`|
|Toggle GPU overdraw|`Toggle debug layout` + `fn`|
|Turn off all UI debuggers|`Toggle debug layout` + `shift`|
|Demo mode (API 23+)|`Toggle demo mode`|
|Reboot|`Reboot system`|
|Reboot to bootloader|`Reboot system` + `cmd`|
|Reboot to recovery|`Reboot system` + `option`|
|Reboot to sideload|`Reboot system` + `ctrl`|
|Connect over WiFi (wired device)|`Connect over Wi-Fi`|
|Input text or button keyevent|in `Keyevent input`|
|Dump task stacks|`Dump task stacks`|
|Dump task stacks of first app|`Dump task stacks` + `cmd`|
|Dump first task stacks|`Dump task stacks` + `option`|
|Screen copy (real device)|`Screen Copy with scrcpy`|
|Screen copy with max dimemsion 1024|`Screen Copy with scrcpy` + `cmd`|
|Screen copy with record screen|`Screen Copy with scrcpy` + `option`|

</details>

![device options](https://github.com/zjn0505/adb-alfred/raw/master/art/screenshot%2002%20show%20device%20options.png)

- select `Show app list` in device options to list and search in all installed applications

  - select one application to show package options
  
<details><summary> <b>Full features at this level</b> </summary>

|Feature|Trigger|
|:--|:--|
|Copy package name|`cmd` + `c` here or in previous level|
|Open app info page|`App info`|
|Force stop application|`Force stop`|
|Start application|`Start application`|
|Clear data|`Clear app data`|
|Uninstall|`Uninstall app`|
|Uninstall but keep data and cache|`Uninstall app` + `cmd`|
|Disable/Enable app|`Disable app`/`Enable app`|
|Disable app for current user|`Disable app` + `cmd`|
|Get apk file|`Extract apk file`|

</details>
  
![package options](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2003%20show%20package%20options.png)

- select `Install apk` in device options to select APK or APKs on local drive for installation

  - `adb install -t -d -g` and bulk installation
  
  - apk signature info will be listed
  
![install options](https://raw.githubusercontent.com/zjn0505/adb-alfred/master/art/screenshot%2004%20show%20install%20options.png)

- `apk` to search for local apk files, and check package info, or analyze it in Android Studio

  - `apkf` to directly list apk files under current front Finder window

  - custom hotkey to open current selected apk file

- `avd` to list installed emulators, select one to start an emulator

  - modifier keys to do cold boot, or wipe emulator data
  
- `geny` to list installed Genymotion emulators, select one to start an emulator


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
|Restart adb service|`adb restart`|
|Custom command in terminal|`adb` -> input, e.g. `shell dumpsys -l \| grep wifi`|
|Custom command silently|`adb` -> input + `cmd`|
|Show history command|`adb` -> `Command history`|
|Clear history command|`adb` -> `Command history` + `cmd`|
|Show applications list|`adb` -> `Show apps list`|
|Select app to launch|`adb` -> `Show apps list` + `cmd`|
|Select app to uninstall|`adb` -> `Show apps list` + `option`|
|Select app to force stop|`adb` -> `Show apps list` + `ctrl`|
|Select app to clear data|`adb` -> `Show apps list` + `fn`|
|Select app to show app info|`adb` -> `Show apps list` + `shift`|
|Install apk or all apks in folder|`adb` -> `Install apk`|
|Take screenshot to clipboard|`adb` -> `Take screenshot`|
|Take screenshot to desktop|`adb` -> `Take screenshot` + `cmd`|
|Open settings|`adb` -> `Open settings`|
|Open developer tools|`adb` -> `Open settings` + `cmd`|
|Open WiFi settings|`adb` -> `Open settings` + `option`|
|Open application settings|`adb` -> `Open settings` + `ctrl`|
|Open date settings|`adb` -> `Open settings` + `fn`|
|Open accessibility settings|`adb` -> `Open settings` + `shift`|
|Toggle debug layout|`adb` -> `Toggle debug layout`|
|Toggle pointer location|`adb` -> `Toggle debug layout` + `cmd`|
|Toggle show taps|`adb` -> `Toggle debug layout` + `option`|
|Toggle GPU profile|`adb` -> `Toggle debug layout` + `ctrl`|
|Toggle GPU overdraw|`adb` -> `Toggle debug layout` + `fn`|
|Turn off all UI debuggers|`adb` -> `Toggle debug layout` + `shift`|
|Demo mode (API 23+)|`adb` -> `Toggle demo mode`|
|Reboot|`adb` -> `Reboot system`|
|Reboot to bootloader|`adb` -> `Reboot system` + `cmd`|
|Reboot to recovery|`adb` -> `Reboot system` + `option`|
|Reboot to sideload|`adb` -> `Reboot system` + `ctrl`|
|Connect over WiFi (wired device)|`adb` -> `Connect over Wi-Fi`|
|Keyevent|`adb` -> `Keyevent input` -> `Back`/`Home`/`App switch`/`Power`/`Status bar`|
|Text input|`adb` -> `Keyevent input` -> input directly|
|Dump task stacks|`adb` -> `Dump task stacks`|
|Dump task stacks of first app|`adb` -> `Dump task stacks` + `cmd`|
|Dump first task stacks|`adb` -> `Dump task stacks` + `option`|
|Screen copy (real device)|`adb` -> `Screen Copy with scrcpy`|
|Screen copy with max dimemsion 1024|`adb` -> `Screen Copy with scrcpy` + `cmd`|
|Screen copy with record screen|`adb` -> `Screen Copy with scrcpy` + `option`|
|Copy package name|`adb` -> `Show apps list` -> `cmd` + `c`|
|Open app info page|`adb` -> `Show apps list` -> `App info`|
|Force stop application|`adb` -> `Show apps list` -> `Force stop`|
|Start application|`adb` -> `Show apps list` -> `Start application`|
|Clear data|`adb` -> `Show apps list` -> `Clear app data`|
|Uninstall|`adb` -> `Show apps list` -> `Uninstall app`|
|Uninstall but keep data and cache|`adb` -> `Show apps list` -> `Uninstall app` + `cmd`|
|Disable/Enable app|`adb` -> `Show apps list` -> `Disable app`/`Enable app`|
|Get apk file|`adb` -> `Show apps list` -> `Extract apk file`|
|Search for apk files|`apk`|
|Inspect apk minSdkVersion|`apk` -> select file -> `cmd`|
|Inspect apk maxSdkVersion|`apk` -> select file -> `option`|
|Inspect apk targetSdkVersion|`apk` -> select file -> `ctrl`|
|Analyze apk in Android Studio|`apk` -> select file -> `fn`|
|List apk files in current Finder|`apkf`|
|Open current selected apk file in workflow|with hotkey|
|List installed emulators|`avd`|
|Wipe emulator data|`avd` + `option`|
|Cold boot an emulator|`avd` + `ctrl`|
|List installed Genymotion emulators|`geny`|
</details>

Self script customization
-----
If there is some cool features you used a lot but not included in this workflow.
You can either add your step, code and link the flow together.
Or you can use "self script" feature to add customizable step for device operation or apk/app operation.

For example.
1. In workflow configuration, add `self_script_app_1` as key and `Open in F-Droid|Users/username/Documents/myscript/open_in_fdroid.py` as value.

2. Now open an apk or select an installed package on device, there will be a new option titled "Open in F-Droid".

3. Once selected, you local script `Users/username/Documents/myscript/open_in_fdroid.py` will be triggered with all existing workflow variables, especially package name in this example.

4. Ideally, F-Droid webpage of current application will be opened.

5. Unlike the first option to add you own step, the customized flow with self script will be persisted across this workflow updates.

If your self script produces a json data in the format of [script filter](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/), it will populate a alfred list after execution.

Please check [self_scripts](https://github.com/zjn0505/adb-alfred/tree/master/self_scripts) for references.


References
------
- [109021017/alfred-adb-workflow](https://github.com/109021017/alfred-adb-workflow)

- [nassendelft/alfred-android-adb](https://github.com/nassendelft/alfred-android-adb)
