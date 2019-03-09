import subprocess
import os
import sys
from workflow import Workflow3, ICON_INFO
 
adb_path = os.getenv('adb_path')
serial = os.getenv('serial')
packName = os.getenv('package')

def main(wf):

    shell_cmd = "{0} -s {1} shell dumpsys package {2} | grep 'versionCode\|versionName\|enabled=' | awk 'NR!=3{{print $1}}NR==3{{print $7}}'".format(adb_path, serial, packName)

    result = None
    infos= None
    versionName = ""
    # Package info
    try:
        result = subprocess.check_output(shell_cmd, stderr=subprocess.STDOUT, shell=True)
        log.debug(result)
    except subprocess.CalledProcessError as e:
        log.debug(e)
    if result:
        infos = result.rstrip().split('\n')
        log.debug(infos)
        versionName = infos[1][12:]
        it = wf.add_item(title=packName,
                        subtitle="{0}({1})".format(versionName, infos[0].strip()[12:]),
                        valid=False,
                        copytext=packName,
                        icon=ICON_INFO)

    # App info
    title = "App info"
    wf.add_item(title=title,
                subtitle="Open app info page",
                arg="app_info",
                valid=True) 

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

    if infos:
        enabled = (infos[2][8:] != '2')
        log.debug("enabled ? {0}".format(enabled))
        
        # Disable/Enable app

        title = ("Enable app", "Disable app")[enabled]
        it = wf.add_item(title=title,
            arg="dis_enable_app",
            valid=True)
        
        it.setvar("enabled", enabled)


    # Get apk file
    title = "Extract apk file"
    it = wf.add_item(title=title,
                arg="extract_apk",
                valid=True)
    if versionName:
        it.setvar("pretty_version", versionName)
                
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
