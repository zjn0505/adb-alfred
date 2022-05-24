import os
from toolchain import run_script
from commands import CMD_GET_DEBUG_LAYOUT
from commands import CMD_SET_DEBUG_LAYOUT

isOff = (os.getenv("function") == "debug_off")

try:
	result = run_script(CMD_GET_DEBUG_LAYOUT)

	isOn = ('off', 'on')[result.lower() != 'on' and not isOff]

	shell_cmd = CMD_SET_DEBUG_LAYOUT.format(isOn)

	result = run_script(shell_cmd)

	print("Debug layout is " + isOn)
except:
	print("Failed to toggle debug layout")