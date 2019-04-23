import os
from toolchain import run_script
from commands import CMD_APP_INFO

package = os.getenv('package')

try:
	run_script(CMD_APP_INFO.format(package))
	print("App info of " + package + " shown")
except:
	print("Failed to show app info of " + package)