import sys
from workflow import Workflow
from toolchain import run_script
from commands import CMD_LIST_APPS
import os

func = os.getenv("func")


def main(wf):
    arg = wf.args[0].strip()
    apps = run_script(CMD_LIST_APPS)
    apps = apps.rstrip().split('\n')

    log.debug(arg)
    for app in apps:
        if arg is '' or any(x.isupper() for x in arg) and arg in app or arg.islower() and arg in app.lower():
            it = wf.add_item(title=app,
                    uid=app,
                    arg=app,
                    copytext=app,
                    valid=True)

            if func == '':
                m = it.add_modifier('cmd', "Launch")
                m.setvar("func", "start_app")

                m = it.add_modifier('alt', "Uninstall")
                m.setvar("func", "uninstall_app")

                m = it.add_modifier('ctrl', "Force stop")
                m.setvar("func", "force_stop")

                m = it.add_modifier('fn', "Clear data")
                m.setvar("func", "clear_app_data")

                m = it.add_modifier('shift', "Show app info")
                m.setvar("func", "app_info")


    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))