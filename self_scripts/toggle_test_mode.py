#-*- coding:UTF-8 -*-
import sys
import os
import subprocess

adb_path = os.getenv('adb_path')
serial = os.getenv('serial')

get_window_animation_scale_cmd = "{0} -s {1} shell settings get global window_animation_scale".format(adb_path, serial)
get_transition_animation_scale_cmd = "{0} -s {1} shell settings get global transition_animation_scale".format(adb_path, serial)
get_animator_duration_scale_cmd = "{0} -s {1} shell settings get global animator_duration_scale".format(adb_path, serial)

get_cmds = [get_window_animation_scale_cmd, get_transition_animation_scale_cmd, get_animator_duration_scale_cmd]

for cmd in get_cmds:  
  result = subprocess.check_output(cmd, 
              stderr=subprocess.STDOUT,
              shell=True).strip()
  mode = "0.0"
  state = "false"
  if result == "0.0":
      mode = "1.0"
      state = "true"

put_window_animation_scale_cmd = "{0} -s {1} shell settings put global window_animation_scale {2}".format(adb_path, serial, mode)
put_transition_animation_scale_cmd = "{0} -s {1} shell settings put global transition_animation_scale {2}".format(adb_path, serial, mode)
put_animator_duration_scale_cmd = "{0} -s {1} shell settings put global animator_duration_scale {2}".format(adb_path, serial, mode)

put_cmds = [put_window_animation_scale_cmd, put_transition_animation_scale_cmd, put_animator_duration_scale_cmd]

for cmd in put_cmds:  
  sys.stderr.write(cmd)
  result = subprocess.check_output(cmd, 
      stderr=subprocess.STDOUT,
      shell=True).strip()
      
  print(result)
