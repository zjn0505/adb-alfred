import os
from toolchain import run_script
from commands import CMD_OPEN_SETTINGS

action = os.getenv('action')
shell_cmd = CMD_OPEN_SETTINGS.format(action)

try:
	run_script(shell_cmd)
except:
	print("Failed to open settings")