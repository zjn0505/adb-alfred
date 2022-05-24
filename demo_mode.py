import os
from toolchain import run_script
from commands import CMD_DEMO_MODE_STATUS
from commands import CMD_DEMO_MODE_EXIT
from commands import CMD_DEMO_MODE_DISABLE
from commands import CMD_DEMO_MODE_ENABLE
from commands import CMD_DEMO_MODE_ENTER
from commands import CMD_DEMO_MODE_CLOCK
from commands import CMD_DEMO_MODE_BATTERY
from commands import CMD_DEMO_MODE_MOBILE
from commands import CMD_DEMO_MODE_WIFI
from commands import CMD_DEMO_MODE_NOTIFICATION

import sys

try:
	result = run_script(CMD_DEMO_MODE_STATUS)
	
	if result == 'null\n' or int(result) != 0:
		sys.stderr.write("Turn demo mode off")

		run_script(CMD_DEMO_MODE_EXIT)
		run_script(CMD_DEMO_MODE_DISABLE)
	else:
		sys.stderr.write("Turn demo mode on")

		run_script(CMD_DEMO_MODE_ENABLE)
		run_script(CMD_DEMO_MODE_ENTER)
		run_script(CMD_DEMO_MODE_CLOCK)
		run_script(CMD_DEMO_MODE_BATTERY)
		run_script(CMD_DEMO_MODE_MOBILE)
		run_script(CMD_DEMO_MODE_WIFI)
		run_script(CMD_DEMO_MODE_NOTIFICATION)
except:
	print("Failed to toggle demo mode")