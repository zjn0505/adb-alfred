import os
from toolchain import run_script
from commands import CMD_FORCE_STOP

package = os.getenv('package')

try:
	run_script(CMD_FORCE_STOP.format(package))
	print("Force stop " + package + " succeed")
except:
	print("Force stop " + package + " failed")