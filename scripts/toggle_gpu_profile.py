import sys
from toolchain import run_script
from commands import CMD_GET_GPU_PROFILE
from commands import CMD_SET_GPU_PROFILE

try:
	result = run_script(CMD_GET_GPU_PROFILE)

	isOn = (result == 'visual_bars')
	sys.stderr.write("GPU profile is " + ("OFF", "ON")[isOn])

	shell_cmd = CMD_SET_GPU_PROFILE.format(("visual_bars", "false")[isOn])

	run_script(shell_cmd)

	print("GPU profile is " + ("ON", "OFF")[isOn])
except:
	print("Failed to toggle GPU profile")