import os
import sys
from toolchain import run_script
from commands import CMD_CUSTOM_COMMAND

cmd = os.getenv('cmd')

try:
	run_script(CMD_CUSTOM_COMMAND.format(cmd))

	print("Executed: " + cmd)
except:
	print("Failed to execute: adb " + cmd)