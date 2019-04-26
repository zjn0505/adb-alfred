import os
import sys
from toolchain import run_script
from commands import CMD_GET_GPU_OVERDRAW
from commands import CMD_SET_GPU_OVERDRAW

isOff = (os.getenv("function") == "debug_off")

try:
	result = run_script(CMD_GET_GPU_OVERDRAW)

	isOn = (result == 'show') or isOff
	sys.stderr.write("GPU overdraw is " + ("OFF", "ON")[isOn])

	shell_cmd = CMD_SET_GPU_OVERDRAW.format(("show", "false")[isOn])

	run_script(shell_cmd)

	print("GPU overdraw is " + ("ON", "OFF")[isOn])
except:
	print("Failed to toggle GPU overdraw")