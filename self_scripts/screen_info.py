# -*- coding:UTF-8 -*-
import sys
import os
import subprocess
import json

adb_path = os.getenv("adb_path")
serial = os.getenv("serial")


adb_cmd = "{0} -s {1} shell".format(adb_path, serial)

isEmulator = serial.startswith("emulator-")

prop = "ro.sf.lcd_density"

if isEmulator:
    prop = "qemu.sf.lcd_density"

get_screen_info = (
    "{0} dumpsys window | grep 'init=\|Configuration=';{0} getprop {1};{0} wm size;{0} wm density".format(adb_cmd, prop)
)

result = subprocess.check_output(get_screen_info, stderr=subprocess.STDOUT, shell=True).strip().decode()

results = result.rstrip().split('\n')
items = []
for index, screen_info in enumerate(results, start=1):
    screen_info = screen_info.strip()
    title = screen_info
    arg = screen_info
    if screen_info.startswith("init="):
        title = "Display"
        arg = adb_cmd + " dumpsys window | grep 'init='"
    elif screen_info.startswith("mGlobalConfiguration="):
        title = "Global Configuration"
        screen_info = screen_info[21:]
        arg = adb_cmd + " dumpsys window | grep 'Configuration='"
    elif screen_info.startswith("mCurConfiguration="):
        title = "Current Configuration"
        screen_info = screen_info[19:]
        arg = adb_cmd + " dumpsys window | grep 'Configuration='"
    elif index == 3 and title.isnumeric(): # Not very strict check
        title = prop
        arg = adb_cmd + " getprop " + prop
    elif screen_info.startswith("Physical size:"):
        title = "Physical size"
        screen_info = screen_info[15:]
        arg = adb_cmd + " wm density"
    elif screen_info.startswith("Override size:"):
        title = "Override size"
        screen_info = screen_info[15:]
        arg = adb_cmd + " wm density"
    elif screen_info.startswith("Physical density:"):
        title = "Physical density"
        screen_info = screen_info[18:]
        arg = adb_cmd + " wm density"
    elif screen_info.startswith("Override density:"):
        title = "Override density"
        screen_info = screen_info[18:]
        arg = adb_cmd + " wm density"
        

    item = {
        "title": title,
        "subtitle": screen_info,
        "arg": arg,
        "text": {
            "copy": screen_info
        }
    }
    items.append(item)

print(json.dumps({"items": items}))