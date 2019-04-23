import sys
from workflow import Workflow3
from toolchain import run_script
from commands import CMD_LIST_APPS

def main(wf):
    arg = wf.args[0].strip()
    apps = run_script(CMD_LIST_APPS)
    apps = apps.rstrip().split('\n')

    for app in apps:
        if arg is '' or arg in app:
            wf.add_item(title=app,
                    uid=app,
                    arg=app,
                    valid=True)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))