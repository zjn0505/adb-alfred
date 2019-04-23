import os
import pipes
from toolchain import run_script
from commands import CMD_CURRENT_FOCUS
from commands import CMD_CALL_STATUSBAR
from commands import CMD_INPUT

cmd = os.getenv('function')
text = os.getenv('key')
mod = os.getenv('mod')

if cmd=="text":
	text = pipes.quote(text.replace(" ", "%s"))

shell_cmd = ""

if cmd == "STATUS_BAR":
	result = run_script(CMD_CURRENT_FOCUS)

	expanded = "StatusBar" in result
	
	shell_cmd = CMD_CALL_STATUSBAR.format(("1", "2")[expanded])
elif cmd == "KEYBOARD":
	shell_cmd = CMD_INPUT.format(cmd, mod, text)
else:
	shell_cmd = CMD_INPUT.format(cmd, ("", "--longpress")[mod=="cmd"], text)

try:
	run_script(shell_cmd)

	print("Executed: " + cmd)
except:
	print("Failed to execute: adb "+cmd)