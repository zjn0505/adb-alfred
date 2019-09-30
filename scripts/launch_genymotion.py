import subprocess
import sys
from workflow import Workflow3, ICON_INFO


def launch_genymotion():
    arg = wf.args[0].strip()
    shell_cmd = "/Applications/Genymotion.app/Contents/MacOS/player.app/Contents/MacOS/player --vm-name '{0}'".format(arg)
    sys.stderr.write(shell_cmd + "\n")
    result = subprocess.check_output(shell_cmd,
                    stderr=subprocess.STDOUT,
                    shell=True)
    sys.stderr.write(result + "\n")

def main(wf):
    launch_genymotion()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
