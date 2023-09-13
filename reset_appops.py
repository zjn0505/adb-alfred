import os
from toolchain import run_script
from commands import CMD_RESET_APPOPS

package = os.getenv('package')

try:
	run_script(CMD_RESET_APPOPS.format(package))
	print("AppOps reset " + package + " succeed")
except:
	print("AppOps reset " + package + " failed")