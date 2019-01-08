import subprocess
import os
import sys
import re
import pickle
import ipaddress
from workflow import Workflow3, ICON_INFO
from workflow.background import run_in_background, is_running
from item import Item
 
adb_path = os.getenv('adb_path')
emulator_path = os.getenv('emulator_path')

def list_emulators():
    arg = wf.args[0].strip()
    shell_cmd = '{0} -list-avds'.format(emulator_path)
    sys.stderr.write(shell_cmd + "\n")
    result = subprocess.check_output(shell_cmd,
                    stderr=subprocess.STDOUT,
                    shell=True)
    emulators = result.rstrip().split('\n')
    for emulator in emulators:
        wf.add_item(title=emulator, uid=emulator, arg=emulator, valid=True)

def main(wf):
    if not emulator_path:
        wf.warn_empty(title="emulator env not found", subtitle="Please config 'emulator_path' in workflow settings")
    else:
        list_emulators()
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger

    if wf.update_available:
        wf.add_item(u'New version available',
                    u'Action this item to install the update',
                    autocomplete=u'workflow:update',
                    icon=ICON_INFO)
    sys.exit(wf.run(main))
