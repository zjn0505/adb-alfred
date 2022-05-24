import os
from toolchain import run_script

adb_path = os.getenv('adb_path')
ip = os.getenv('ip')
shell_cmd = '{0} disconnect {1}'.format(adb_path, ip)

try:
	result = run_script(shell_cmd)
	print("Executed: adb disconnect " + ip)
except:
	print("Failed to execute: adb disconnect " + ip)