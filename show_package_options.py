import subprocess
import os
import sys
from workflow import Workflow, ICON_INFO
from toolchain import run_script
from commands import CMD_DUMP_PACKAGE
 
packName = os.getenv('package')

def main(wf):

    shell_cmd = CMD_DUMP_PACKAGE.format(packName)

    result = None
    infos= None
    versionName = ""
    enabled = True
    # Package info
    try:
        result = run_script(shell_cmd)
    except subprocess.CalledProcessError as e:
        log.debug(e)
    if result:
        result = result[result.rfind("enabled="):]
        infos = result.rstrip().split('\n')
        log.debug(infos)
        versionName = infos[1].strip()[12:]
        versionCode = infos[2].strip()[12:]
        it = wf.add_item(title=packName,
                        subtitle="{0}({1})".format(versionName, versionCode),
                        valid=False,
                        copytext=packName,
                        icon=ICON_INFO)
    if infos:
        appInfo = infos[0].strip()
        enabled = (appInfo[appInfo.find("enabled=") + 8] != '2')
        log.debug("enabled ? {0}".format(enabled))

    # App info
    title = "App info"
    wf.add_item(title=title,
                subtitle="Open app info page",
                arg="app_info",
                valid=True) 
    
    if (infos and enabled):
        # Force stop
        title = "Force stop"
        wf.add_item(title=title,
                    arg="force_stop",
                    valid=True) 

    if (infos and len(infos) > 3 and enabled):
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
        # Disable/Enable app

        title = ("Enable app", "Disable app")[enabled]
        it = wf.add_item(title=title,
            arg="dis_enable_app",
            valid=True)
        
        it.setvar("enabled", enabled)
        if enabled:
            mod = it.add_modifier("cmd", subtitle="disable for current user")
            mod.setvar("mod", "disable_for_current_user")


    # Get apk file
    title = "Extract apk file"
    it = wf.add_item(title=title,
                arg="extract_apk",
                valid=True)
    if versionName:
        it.setvar("pretty_version", versionName)

    idx = 1
    while idx > 0:
        config = os.getenv('self_script_app_%d' % idx)
        if config:
            title = config.split("|")[0]
            path = config.split("|")[1]
            it = wf.add_item(title=title,
                        subtitle="with script: %s" % path,
                        arg="self_script_app_%d" % idx,
                        valid=True)
            it.setvar("self_script_app", config)
            mod = it.add_modifier("cmd", subtitle="apply cmd modifier")
            mod.setvar("mod", "cmd")
            mod = it.add_modifier("alt", subtitle="apply alt modifier")
            mod.setvar("mod", "alt")
            mod = it.add_modifier("ctrl", subtitle="apply ctrl modifier")
            mod.setvar("mod", "ctrl")
            mod = it.add_modifier("fn", subtitle="apply fn modifier")
            mod.setvar("mod", "fn")
            mod = it.add_modifier("shift", subtitle="apply shift modifier")
            mod.setvar("mod", "shift")

            idx = idx + 1
        else:
            idx = -1

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
