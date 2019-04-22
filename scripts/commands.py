import os

adb_path = os.getenv('adb_path')
serial = os.getenv('serial')
adbs = adb_path + ' -s ' + serial + ' '
adbshell = adbs + 'shell '


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

# Screen shot
CMD_SCREENCAP = adbshell + 'screencap -p sdcard/screenshot_{}.jpg'
CMD_PULL_TEMP_TO_DESKTOP = adbs + 'pull sdcard/screenshot_{0}.jpg {1}'
CMD_RM_TEMP = adbshell + 'rm sdcard/screenshot_{}.jpg'