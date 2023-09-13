import subprocess
import os
import sys
from workflow import Workflow, ICON_INFO
from toolchain import run_script
from commands import CMD_DUMP_PACKAGE
import commands
 
packName = os.getenv('package')

def main(wf):

    shell_cmd = CMD_DUMP_PACKAGE.format(packName)

    result = None
    infos= None
    versionName = ""
    enabled = True
    userId = None
    versionCopyText = ""
    # Package info
    try:
        result = run_script(shell_cmd)
    except subprocess.CalledProcessError as e:
        log.debug(e)
    if result:
        result = result[result.rfind("enabled="):]
        infos = result.rstrip().split('\n')
        log.debug(infos)

        userIdInfo = [x.strip() for x in infos if x.strip().startswith("userId=")]
        log.debug(userIdInfo)
        if len(userIdInfo) == 1:
            userId = userIdInfo[0][7:]
        
        versionName = infos[1].strip()[12:]
        versionCode = infos[2].strip()[12:]
        if userId != None:
            versionCode = versionCode + " userId={0}".format(userId) 
        it = wf.add_item(title=packName,
                        subtitle="{0}({1})".format(versionName, versionCode),
                        valid=False,
                        copytext=packName,
                        icon=ICON_INFO)
        versionCopyText = it.subtitle
    if infos:
        appInfo = infos[0].strip()
        enabled = (appInfo[appInfo.find("enabled=") + 8] != '2')
        log.debug("enabled ? {0}".format(enabled))

    # App info
    title = "App info"
    it = wf.add_item(title=title,
                subtitle="Open app info page",
                arg="app_info",
                copytext=versionCopyText,
                valid=True)
    it.add_modifier("cmd", subtitle="cmd + C to copy app info")
    
    if (infos and enabled):
        # Force stop
        title = "Force stop"
        wf.add_item(title=title,
                    arg="force_stop",
                    valid=True) 

    if (infos and len(infos) > 4 and enabled):
        # Start app
        title = "Start application"
        wf.add_item(title=title,
                    arg="start_app",
                    copytext=commands.CMD_LAUNCH_APP.format(packName),
                    valid=True)

    # Clear data
    title = "Clear app data"
    wf.add_item(title=title,
                arg="clear_app_data",
                copytext=commands.CMD_CLEAR_DATA.format(packName),
                valid=True)

    # Uninstall
    title = "Uninstall app"
    it = wf.add_item(title=title,
                arg="uninstall_app",
                subtitle="`cmd` to keep data and cache",
                copytext=commands.CMD_UNINSTALL_APP.format(packName, ""),
                valid=True)

    mod = it.add_modifier("cmd", subtitle="keep the data and cache directories")
    mod.setvar("mod", "keep_data")

    if infos:    
        # Disable/Enable app

        title = ("Enable app", "Disable app")[enabled]
        it = wf.add_item(title=title,
            arg="dis_enable_app",
            copytext=commands.CMD_DISABLE_APP.format(("enable", "disable")[enabled], packName),
            valid=True)
        
        it.setvar("enabled", enabled)
        if enabled:
            mod = it.add_modifier("cmd", subtitle="disable for current user")
            mod.setvar("mod", "disable_for_current_user")

    # Reset AppOps
    title = "Reset AppOps"
    it = wf.add_item(title=title,
                arg="reset_appops",
                subtitle="Reset permissions to default. Will not work if exec too often.",
                copytext=commands.CMD_RESET_APPOPS.format(packName),
                valid=True)

    # Get apk file
    title = "Extract apk file"
    it = wf.add_item(title=title,
                arg="extract_apk",
                copytext=commands.CMD_SHOW_APK_PATH.format(packName),
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
