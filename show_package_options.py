import subprocess
import os
import sys
from workflow import Workflow3, ICON_INFO
 
adb_path = os.getenv('adb_path')
serial = os.getenv('serial')
packName = os.getenv('package')

def main(wf):

    shell_cmd = "{0} -s {1} shell dumpsys package {2} | grep 'versionCode\|versionName' | awk '{{print $1}}'".format(adb_path, serial, packName)

    result = None

    # Package info
    try:
        result = subprocess.check_output(shell_cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        log.debug(e)
    if result:
        infos = result.rstrip().split('\n')
        log.debug(infos)
        it = wf.add_item(title=packName, subtitle="{0}({1})".format(infos[1][12:], infos[0].strip()[12:]), valid=False, icon=ICON_INFO)

    # Force stop
    title = "Force stop"
    wf.add_item(title=title,
                arg="force_stop",
                valid=True) 

    # Start app
    title = "Start application"
    wf.add_item(title=title,
                arg="start_app",
                valid=True)

    # Clear data
    title = "Clear app data"
    wf.add_item(title=title,
                arg="clear_app_data",
                valid=True)

    # Uninstall
    title = "Uninstall app"
    it = wf.add_item(title=title,
                arg="uninstall_app",
                subtitle="`cmd` to keep data and cache",
                valid=True)
                
    mod = it.add_modifier("cmd", subtitle="keep the data and cache directories")
    mod.setvar("mod", "keep_data")

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
