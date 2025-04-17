import os
import shlex
from toolchain import run_script
from commands import CMD_CURRENT_FOCUS
from commands import CMD_CALL_STATUSBAR
from commands import CMD_INPUT, CMD_DOUBLE_INPUT

cmd = os.getenv('function')
text = os.getenv('key')
mod = os.getenv('mod')

if cmd == "text":
    text = shlex.quote(text.replace(" ", "%s"))

shell_cmd = ""

if cmd == "STATUS_BAR":
    result = run_script(CMD_CURRENT_FOCUS)

    expanded = "StatusBar" in result

    shell_cmd = CMD_CALL_STATUSBAR.format(("1", "2")[expanded])
elif cmd == "KEYBOARD":
    shell_cmd = CMD_INPUT.format(cmd, mod, text)
elif cmd == 'keyevent' and text == 'KEYCODE_BACK' and mod == 'alt':
    shell_cmd = CMD_DOUBLE_INPUT.format(cmd, text)
elif cmd.startswith('keyevent_input_'):
    shell_cmd = CMD_INPUT.format("keyevent", "", cmd[15:])
else:
    shell_cmd = CMD_INPUT.format(cmd, ("", "--longpress")[mod == "cmd"], text)

try:
    run_script(shell_cmd)

    print("Executed: " + cmd)
except:
    print("Failed to execute: adb "+cmd)
