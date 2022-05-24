import os
from toolchain import run_script
from commands import CMD_REBOOT

# `function` could be `adb_reboot:bootloader` 
cmd = os.getenv('function')[11:]

shell_cmd= CMD_REBOOT.format(cmd)

try:
    run_script(shell_cmd)
    print("Reboot device succeed")
except:
	print("Reboot device failed")