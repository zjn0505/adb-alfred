import os
from toolchain import run_script
from toolchain import call_script

from commands import CMD_SCREENCAP
from commands import CMD_PULL_TEMP_TO_DESKTOP
from commands import CMD_RM_TEMP

datetime = os.getenv('time')

mod = os.getenv('function')[11:]

shell_cmd_1 = CMD_SCREENCAP.format(datetime)
shell_cmd_2 = CMD_PULL_TEMP_TO_DESKTOP.format(datetime, ("/tmp/", "~/Desktop/")[mod == "to_desktop"])
shell_cmd_3 = CMD_RM_TEMP.format(datetime)
import sys
sys.stderr.write("\n {} \n".format(mod))
try:
    run_script(shell_cmd_1)
    run_script(shell_cmd_2)
    run_script(shell_cmd_3)

    local_path = ""
    if mod and mod == "to_desktop":
        local_path = "~/Desktop/screenshot_{0}.jpg".format(datetime)
    else:
        local_path = "/tmp/screenshot_{0}.jpg".format(datetime)
	
    if mod and mod == "to_clipboard":
        if call_script(['which', 'osascript']) == 0:
            shell_cmd_4 = "osascript -e 'on run args' -e 'set thisFile to item 1 of args' -e 'set the clipboard to (read thisFile as JPEG picture)' -e return -e end {0}".format(local_path)
            run_script(shell_cmd_4)
        elif call_script(['which', 'xclip']) == 0:
            run_script("xclip -selection clipboard -t image/jpg -i {0}".format(local_path))
            run_script("rm {0}".format(local_path))
        print("Screenshot captured to clipboard")
    else:
        print("Screenshot captured to desktop")
except:
	print("Failed to capture screenshot")