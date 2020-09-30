#-*- coding:UTF-8 -*-
import sys
import os
import subprocess
import json


adb_path = os.getenv('adb_path')
serial = os.getenv('serial')

cmd = "{0} -s {1} shell ime list -s".format(adb_path, serial)

sys.stderr.write(cmd)
result = subprocess.check_output(cmd, 
    stderr=subprocess.STDOUT,
    shell=True).strip().decode('utf-8')

imes = result.rstrip().split('\n')
items = []
for ime in imes:
    ime = ime.strip()
    package, classN = ime.split('/')
    sys.stderr.write(ime)
    sys.stderr.write("\n")
    item = {
        "uid " : ime,
        "title": package,
        "subtitle": classN,
        "arg": ime,
        "autocomplete": package,
        "text": {
            "copy": ime
        }
    }
    items.append(item)

print(json.dumps({"items": items}))