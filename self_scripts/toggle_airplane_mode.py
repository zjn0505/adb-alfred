#-*- coding:UTF-8 -*-
import sys
import os
import subprocess

adb_path = os.getenv('adb_path')
serial = os.getenv('serial')

cmd =  "adb shell settings get global airplane_mode_on"

# adb shell settings put global airplane_mode_on 1
# adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true
cmd = "{0} -s {1} shell settings get global airplane_mode_on".format(adb_path, serial)

result = subprocess.check_output(cmd, 
            stderr=subprocess.STDOUT,
            shell=True).strip()

mode = "0"
state = "false"
if result == "0":
    mode = "1"
    state = "true"

cmd = "{0} -s {1} shell settings put global airplane_mode_on {2} \
&& {0} -s {1} shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state {3}".format(adb_path, serial, mode, state)

sys.stderr.write(cmd)
result = subprocess.check_output(cmd, 
    stderr=subprocess.STDOUT,
    shell=True).strip()
    
print(result)