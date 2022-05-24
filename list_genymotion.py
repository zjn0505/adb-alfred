import subprocess
import sys
from workflow import Workflow
from toolchain import run_script


def list_genymotion():
    arg = wf.args[0].strip()
    shell_cmd = "/usr/local/bin/VBoxManage list vms -l | grep '^Name:\|Hardware UUID:\|Log folder:' | tr -s ' '"
    result = run_script(shell_cmd)
    array = result.strip().split('\n')

    size = len(array) // 3

    for item in range(size):
        index = item * 3
        location = array[index + 1]
        if "Genymotion" not in location:
            continue
        name = array[index][6:]
        uuid = array[index + 2][15:]
        it = wf.add_item(title=name, uid=uuid, arg=uuid, valid=True)
        m = it.add_modifier("cmd", uuid)

def main(wf):
    list_genymotion()
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger

    if wf.update_available:
        wf.add_item(u'New version available',
                    u'Action this item to install the update',
                    autocomplete=u'workflow:update')
    sys.exit(wf.run(main))
