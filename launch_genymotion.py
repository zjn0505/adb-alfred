import subprocess
import sys
from workflow import Workflow
from toolchain import run_script


def launch_genymotion():
    arg = wf.args[0].strip()
    shell_cmd = "/Applications/Genymotion.app/Contents/MacOS/player.app/Contents/MacOS/player --vm-name '{0}'".format(arg)
    run_script(shell_cmd)

def main(wf):
    launch_genymotion()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
