#-*- coding:UTF-8 -*-
import sys
import os
import subprocess

adb_path = os.getenv('adb_path')
serial = os.getenv('serial')

enable_gesture_nav_cmd = "{0} -s {1} shell cmd overlay enable com.android.internal.systemui.navbar.gestural".format(adb_path, serial)

disable_gesture_nav_cmd = "{0} -s {1} shell cmd overlay disable com.android.internal.systemui.navbar.gestural".format(adb_path, serial)

get_gesture_nav_cmd = "{0} -s {1} shell cmd overlay list com.android.internal.systemui.navbar.gestural".format(adb_path, serial)

result = subprocess.check_output(get_gesture_nav_cmd, 
            stderr=subprocess.STDOUT,
            shell=True).strip().decode()
toggle_cmd = enable_gesture_nav_cmd
if result.__contains__("x"):
    toggle_cmd = disable_gesture_nav_cmd

sys.stderr.write(toggle_cmd)

result = subprocess.check_output(toggle_cmd, 
    stderr=subprocess.STDOUT,
    shell=True).strip().decode()
      
print(result)
