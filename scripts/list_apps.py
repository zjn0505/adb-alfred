import sys
from workflow import Workflow3
from toolchain import run_script
from commands import CMD_LIST_APPS

def main(wf):
    arg = wf.args[0].strip()
    apps = run_script(CMD_LIST_APPS)
    apps = apps.rstrip().split('\n')

    log.debug(arg)
    for app in apps:
        if arg is '' or any(x.isupper() for x in arg) and arg in app or arg.islower() and arg in app.lower():
            wf.add_item(title=app,
                    uid=app,
                    arg=app,
                    copytext=app,
                    valid=True)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))