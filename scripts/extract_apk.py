import os
from toolchain import run_script
from commands import CMD_SHOW_APK_PATH
from commands import CMD_PULL_APK_TO_DESKTOP

package = os.getenv('package')
prettyVersion = os.getenv('pretty_version')

try:
	result = run_script(CMD_SHOW_APK_PATH.format(package))
	if result and result.startswith("package:"):
		path = result[8:].strip()

		run_script(CMD_PULL_APK_TO_DESKTOP.format(path, package, prettyVersion))
		print("Apk extracted to desktop")
	else:
		print("Failed to extract apk")
except:
	print("Failed to extract apk")