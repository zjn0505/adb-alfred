from toolchain import run_script
from commands import CMD_GET_SHOW_TAPS
from commands import CMD_SET_SHOW_TAPS

try:
	result = run_script(CMD_GET_SHOW_TAPS)

	isOn = (result[-1:] == '1')
	
	shell_cmd = CMD_SET_SHOW_TAPS.format(("1", "0")[isOn])
	
	run_script(shell_cmd)

	print("Show taps is " + ("ON", "OFF")[isOn])
except:
	print("Failed to toggle show taps")