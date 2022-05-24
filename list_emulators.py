import subprocess
import os
import sys
from workflow import Workflow
from toolchain import run_script
 
adb_path = os.getenv('adb_path')
emulator_path = os.getenv('emulator_path')

def list_emulators():
    arg = wf.args[0].strip()
    shell_cmd = '{0} -list-avds'.format(emulator_path)
    result = run_script(shell_cmd)
    emulators = result.rstrip().split('\n')
    for emulator in emulators:
        it = wf.add_item(title=emulator, uid=emulator, arg=emulator, valid=True)
        it.setvar("func", "")
        m = it.add_modifier('ctrl', "Start a cold boot")
        m.setvar("func", "-no-snapshot-load")
        m = it.add_modifier('alt', "Wipe emulator data")
        m.setvar("func", "-wipe-data")

def main(wf):
    if not emulator_path:
        wf.warn_empty(title="emulator env not found", subtitle="Please config 'emulator_path' in workflow settings")
    else:
        list_emulators()
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger

    if wf.update_available:
        wf.add_item(u'New version available',
                    u'Action this item to install the update',
                    autocomplete=u'workflow:update')
    sys.exit(wf.run(main))
