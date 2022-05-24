import os
from toolchain import run_script
from commands import CMD_UNINSTALL_APP

package = os.getenv('package')

param = ""
if os.getenv('mod') == "keep_data":
	param = "-k"

try:
	run_script(CMD_UNINSTALL_APP.format(param, package))
	print("Uninstall app " + package + " succeed")
except:
	print("Uninstall app " + package + " failed")