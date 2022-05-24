import os
from toolchain import run_script
from commands import CMD_DISABLE_APP

package = os.getenv('package')
enabled = os.getenv('enabled')
mod = os.getenv('mod')

try:
	if enabled == '1' and mod == 'disable_for_current_user':
		run_script(CMD_DISABLE_APP.format("disable-user --user 0", package))
	else:
		run_script(CMD_DISABLE_APP.format(("enable", "disable")[enabled=='1'], package))
	print(("Enable", "Disable")[enabled=='1'] + " app " + package + " succeed")
except:
	print(("Enable", "Disable")[enabled=='1'] + " app " + package + " failed")