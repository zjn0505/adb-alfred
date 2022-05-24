import os
import sys
from toolchain import run_script
from commands import CMD_GET_POINTER_LOCATION
from commands import CMD_SET_POINTER_LOCATION

isOff = (os.getenv("function") == "debug_off")

try:
	result = run_script(CMD_GET_POINTER_LOCATION)

	isOn = (result == '1') or isOff

	sys.stderr.write("Pointer location is " + ("OFF", "ON")[isOn])

	shell_cmd = CMD_SET_POINTER_LOCATION.format(("1", "0")[isOn])

	run_script(shell_cmd)

	print("Pointer location is " + ("ON", "OFF")[isOn])
except:
	print("Failed to toggle pointer location")