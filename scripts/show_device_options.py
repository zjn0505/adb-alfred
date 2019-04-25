import subprocess
import os
import sys
import re
from workflow import Workflow3
 
adb_path = os.getenv('adb_path')
serial = os.getenv('serial')
api = os.getenv('device_api')
ip = os.getenv("ip")

def wordMatch(arg, sentence): 
    words = arg.lower().split(" ")
    sentenceComponents = sentence.lower().split(" ")
    for word in words:
        included = False
        for sentenceComponent in sentenceComponents:
            if word in sentenceComponent:
                included = True
                break
        if not included:
            return False
    return True

def main(wf):

    isWifiDevice = re.match(".*:5555$", serial)
    isEmulator = re.match("emulator-55[5-8][02468]", serial)
    arg = wf.args[0].strip()
    log.debug(arg)
    addAll = False
    if arg == '':
        addAll = True

    itemCount = 0

    # SHOW INSTALLED PACKAGES
    title = "Show apps list"
    
    if addAll or (wordMatch(arg, title + " start launch uninstall force stop clear info") and not arg.startswith("ins")):
        func = ""
        if "start" in arg.lower() or "launch" in arg.lower():
            title = "Select app to launch"
            func = "start_app"
        elif "uninstall" in arg.lower():
            title = "Select app to uninstall"
            func = "uninstall_app"
        elif "force" in arg.lower() or "stop" in arg.lower():
            title = "Select app to force stop"
            func = "force_stop"
        elif "clear" in arg.lower():
            title = "Select app to clear data"
            func = "clear_app_data"
        elif "info" in arg.lower():
            title = "Select app to show app info"
            func = "app_info"
        it = wf.add_item(title=title,
                    uid="list_app",
                    arg="list_app",
                    valid=True)
        it.setvar("func", func)
        if func == "":
            m = it.add_modifier('cmd', "Select app to launch")
            m.setvar("func", "start_app")

            m = it.add_modifier('alt', "Select app to uninstall")
            m.setvar("func", "uninstall_app")

            m = it.add_modifier('ctrl', "Select app to force stop")
            m.setvar("func", "force_stop")

            m = it.add_modifier('fn', "Select app to clear data")
            m.setvar("func", "clear_app_data")

            m = it.add_modifier('shift', "Select app to show app info")
            m.setvar("func", "app_info")
        itemCount += 1

    # INSTALL APK
    title = "Install apk"
    
    if addAll or wordMatch(arg, title):
        wf.add_item(title=title,
                    uid="install_apk",
                    arg="install_apk",
                    subtitle="install apk or apks",
                    valid=True)
        itemCount += 1

    # SCREENSHOT
    title = "Take screenshot"
    
    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="screenshot",
                    arg="screenshot",
                    subtitle="take a screenshot and copy to clipboard, `cmd` to copy to desktop",
                    valid=True)
        m = it.add_modifier('cmd', 'take a screenshot and copy to desktop')
        m.setvar("mod", "cmd")
        itemCount += 1

    # OPEN SETTINGS
    title = "Open settings"
    
    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="open_settings",
                    arg="open_settings",
                    subtitle="'cmd' - Dev Tool, 'alt' - WiFi, 'ctrl' - App, 'fn' - Date, 'shift' - Accessibility",
                    valid=True)
        it.setvar("action", "android.settings.SETTINGS")
        m = it.add_modifier('cmd', 'Open Developer Settings')
        m.setvar('action', 'com.android.settings.APPLICATION_DEVELOPMENT_SETTINGS')
        m = it.add_modifier('alt', 'Open WiFi Settings')
        m.setvar('action', 'android.settings.WIFI_SETTINGS')
        m = it.add_modifier('fn', 'Open Date Settings')
        m.setvar('action', 'android.settings.DATE_SETTINGS')
        m = it.add_modifier('shift', 'Open Accessibility Settings')
        m.setvar('action', 'android.settings.ACCESSIBILITY_SETTINGS')
        m = it.add_modifier('ctrl', 'Open Application Settings')
        m.setvar('action', 'android.settings.APPLICATION_SETTINGS:')
        itemCount += 1

    # TOGGLE DEBUG LAYOUT
    title = "Toggle debug layout"
    
    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="debug_layout",
                    arg="debug_layout",
                    valid=True)
        itemCount += 1

        m = it.add_modifier('cmd', 'Toggle pointer location', arg="pointer_location")

        m = it.add_modifier('alt', 'Toggle show taps', arg="show_taps")

        m = it.add_modifier('ctrl', 'Toggle GPU profile', arg="gpu_profile")

        m = it.add_modifier('fn', 'Toggle GPU overdraw', arg="gpu_overdraw")


    # DEMO MODE
    if api and int(api) >= 23:
        title = "Toggle demo mode"
        
        if addAll or wordMatch(arg, title):
            wf.add_item(title=title,
                        uid="demo_mode",
                        arg="demo_mode",
                        valid=True)
            itemCount += 1

    # REBOOT SYSTEM
    title = "Reboot system"

    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="adb_reboot",
                    arg="adb_reboot",
                    subtitle="'cmd' - Bootloader, 'alt' - Recovery, 'ctrl' - Sideload",
                    valid=True)
        itemCount += 1
        it.setvar('mod', '')
        m = it.add_modifier('cmd', 'Bootloader')
        m.setvar('mod', 'bootloader')
        m = it.add_modifier('alt', 'Recovery')
        m.setvar('mod', 'recovery')
        m = it.add_modifier('ctrl', 'Sideload')
        m.setvar('mod', 'sideload')

    # CONNECT OVER WIFI
    if not isWifiDevice and not isEmulator and ip:
        title = "Connect over Wi-Fi"
        
        if addAll or wordMatch(arg, title):
            wf.add_item(title=title,
                        subtitle=ip,
                        uid="debug_wifi",
                        arg="debug_wifi",
                        valid=True)
            itemCount += 1

    # KEY INPUT
    title = "Keyevent input"

    if addAll or wordMatch(arg, title):
        wf.add_item(title=title,
                    uid="keyevent_input",
                    arg="keyevent_input",
                    valid=True)
        itemCount += 1
        
    # DUMP STACK
    title = "Dump task stacks"

    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="dump_stack",
                    arg="dump_stack",
                    valid=True)
        itemCount += 1
        it.setvar('mod', '')
        m = it.add_modifier('cmd', 'Dump the first application')
        m.setvar('mod', 'first_app')
        m = it.add_modifier('alt', 'Dump the first stack')
        m.setvar('mod', 'first_stack')

    # CUSTOM ACTION
    if itemCount == 0:
        it = wf.add_item(title="Execute custom command for " + serial,
                        subtitle="adb " + arg,
                        arg="<adb>" + arg,
                        valid=True)
        it.setvar('mod', 'none')
        m = it.add_modifier('cmd', 'Run without opening terminal')
        m.setvar('mod', 'cmd')
        it.setvar('cmd', arg)
        m.setvar('cmd', arg)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
