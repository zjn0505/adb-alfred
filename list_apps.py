import subprocess
import os
import sys
import re
from workflow import Workflow3

adb_path = os.getenv('adb_path')
serial = os.getenv('serial')

def main(wf):
    arg = wf.args[0].strip()
    apps = subprocess.check_output(
            "{0} -s {1} shell 'pm list packages -f' | grep package: | sed -e 's/.*=//' | sed 's/\r//g' | sort".format(adb_path, serial),
            stderr=subprocess.STDOUT,
            shell=True)
    apps = apps.rstrip().split('\n')

    for app in apps:
        if arg is '' or arg in app:
            wf.add_item(title=app,
                    arg=app,
                    valid=True)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))