import os

adb_path = os.getenv('adb_path')
serial = os.getenv('serial')
adbs = adb_path + ' -s ' + serial + ' '
adbshell = adbs + 'shell '

aapt_path = os.getenv('aapt_path')


# Reboot devices
CMD_REBOOT = adbshell + 'reboot {}'

# Debug layout
CMD_GET_DEBUG_LAYOUT = adbshell + 'getprop debug.layout'
CMD_SET_DEBUG_LAYOUT = adbshell + 'setprop debug.layout {} && ' + adbshell + 'service call activity 1599295570'

# Pointer location
CMD_GET_POINTER_LOCATION = adbshell + 'settings get system pointer_location'
CMD_SET_POINTER_LOCATION = adbshell + 'settings put system pointer_location {}'

# Show taps
CMD_GET_SHOW_TAPS = adbshell + 'content query --uri content://settings/system --projection name:value --where "name=\\\'show_touches\\\'"'
CMD_SET_SHOW_TAPS = adbshell + 'content insert --uri content://settings/system --bind name:s:show_touches --bind value:i:{}'

# GPU profile
CMD_GET_GPU_PROFILE = adbshell + 'getprop debug.hwui.profile'
CMD_SET_GPU_PROFILE = adbshell + 'setprop debug.hwui.profile {}'

# GPU overdraw
CMD_GET_GPU_OVERDRAW = adbshell + 'getprop debug.hwui.overdraw'
CMD_SET_GPU_OVERDRAW = adbshell + 'setprop debug.hwui.overdraw {}'

# Screen shot
CMD_SCREENCAP = adbshell + 'screencap -p sdcard/screenshot_{}.jpg'
CMD_PULL_TEMP_TO_DESKTOP = adbs + 'pull sdcard/screenshot_{0}.jpg {1}'
CMD_RM_TEMP = adbshell + 'rm sdcard/screenshot_{}.jpg'

# Open Settings
CMD_OPEN_SETTINGS = adbshell + 'am start -a {}'

# Demo mode
CMD_DEMO_MODE_STATUS = adbshell + 'settings get global sysui_demo_allowed'
CMD_DEMO_MODE_EXIT = adbshell + 'am broadcast -a com.android.systemui.demo -e command exit'
CMD_DEMO_MODE_DISABLE = adbshell + 'settings put global sysui_demo_allowed 0'
CMD_DEMO_MODE_ENABLE = adbshell + 'settings put global sysui_demo_allowed 1'
CMD_DEMO_MODE_ENTER = adbshell + 'am broadcast -a com.android.systemui.demo -e command enter'
CMD_DEMO_MODE_CLOCK = adbshell + 'am broadcast -a com.android.systemui.demo -e command clock -e hhmm 1200'
CMD_DEMO_MODE_BATTERY = adbshell + 'am broadcast -a com.android.systemui.demo -e command battery -e plugged false -e level 100'
CMD_DEMO_MODE_MOBILE = adbshell + 'am broadcast -a com.android.systemui.demo -e command network -e mobile show -e level 4 -e datatype false'
CMD_DEMO_MODE_WIFI = adbshell + 'am broadcast -a com.android.systemui.demo -e command network -e wifi show -e level 4 -e fully true'
CMD_DEMO_MODE_NOTIFICATION = adbshell + 'am broadcast -a com.android.systemui.demo -e command notifications -e visible false'

# ADB WiFi
CMD_GET_TCPIP = adbshell + 'getprop service.adb.tcp.port'
CMD_TCPIP = adbs + 'tcpip 5555'
CMD_ADB_CONNECT = adb_path + ' connect {}:5555'

# Custom command
CMD_CUSTOM_COMMAND = adbs + '{}'

# Execute input
CMD_CURRENT_FOCUS = adbshell + 'dumpsys window | grep mCurrentFocus'
CMD_CALL_STATUSBAR = adbshell + 'service call statusbar {}'
CMD_INPUT = adbshell + 'input {0} {1} {2}'
CMD_DOUBLE_INPUT = adbshell + "'input {0} {1} && input {0} {1}'"

# Force stop
CMD_FORCE_STOP = adbshell + 'am force-stop {}'

# App info
CMD_APP_INFO = adbshell + 'am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:{}'

# Launch app
CMD_LAUNCH_APP = adbshell + 'monkey -p {} -c android.intent.category.LAUNCHER 1'

# Clear data
CMD_CLEAR_DATA = adbshell + 'pm clear {}'

# Uninstall app
CMD_UNINSTALL_APP = adbshell + 'pm uninstall {0} {1}'

# Disable app
CMD_DISABLE_APP = adbshell + 'pm {0} {1}'

# Extract apk
CMD_SHOW_APK_PATH = adbshell + 'pm path {}'
CMD_PULL_APK_TO_DESKTOP = adbs + 'pull {0} ~/Desktop/{1}-{2}.apk'

# Install app
CMD_INSTALL_APP = adbs + 'install -r {0} {1}'

# List apps
CMD_LIST_APPS = adbshell + "'pm list packages -f' | grep package: | sed -e 's/.*=//' | sed 's/\r//g' | sort"

# Check keyboard
CMD_CHECK_KEYBOARD = adbshell + "dumpsys input_method | grep mInputShown | awk '{{print $4}}'"

# Dump package
CMD_DUMP_PACKAGE = adbshell + "dumpsys package {} | grep 'versionCode\|versionName\|enabled=\|android.intent.action.MAIN' | tail -r"

# Dump task stack
CMD_DUMP_STACK = adbshell + "dumpsys activity activities | grep 'Hist \|taskAffinity='"