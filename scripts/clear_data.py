import os
from toolchain import run_script
from commands import CMD_CLEAR_DATA

package = os.getenv('package')

try:
	run_script(CMD_CLEAR_DATA.format(package))
	print("Data clear " + package + " succeed")
except:
	print("Data clear " + package + " failed")