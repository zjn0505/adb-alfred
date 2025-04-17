import os
import shlex
import sys
from toolchain import run_script
from commands import CMD_INSTALL_APP

apkFiles = os.getenv('apkFile').split("\t")
options = os.getenv('option')

optionArg = ""
if options:
	for option in options:
		if option and option.strip():
			if option == "b":
				optionArg = optionArg + " --bypass-low-target-sdk-block"
			else:
				optionArg = optionArg + " -" + option

try:
	if apkFiles:
		totalFiles = len(apkFiles)
		installResults = 0
		sys.stderr.write("Step 1 {0}, {1}\n".format(totalFiles, optionArg))
		for apkFile in apkFiles:
			sys.stderr.write("Step 2" + "\n")
			if not apkFile:
				continue
			result = run_script(CMD_INSTALL_APP.format(optionArg, (shlex.quote(apkFile), apkFile)[apkFile.startswith('\"') or apkFile.startswith("\'")]))
			if "Failure [" not in result and "Error:" not in result:
				installResults = installResults + 1
			sys.stderr.write(result + "\n")
	if installResults == totalFiles:
		print("Install app succeed")
	else:
		print("Install app failed, {0}/{1} failed".format(totalFiles - installResults, totalFiles))
except:
	print("Install app failed")