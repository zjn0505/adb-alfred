import os
from toolchain import run_script
from commands import CMD_LAUNCH_APP

package = os.getenv('package')

try:
	run_script(CMD_LAUNCH_APP.format(package))
	print("Launch app " + package + " succeed")
except:
	print("Launch app " + package + " failed")