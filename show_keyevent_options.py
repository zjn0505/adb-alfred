import re
import sys
from workflow import Workflow
from toolchain import run_script
from commands import CMD_CHECK_KEYBOARD


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

    arg = wf.args[0].strip()
    log.debug(arg)
    addAll = False
    if arg == '':
        addAll = True

    itemCount = 0
    wf.setvar("function", "keyevent")
    # Back
    title = "Back"
    
    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="KEYCODE_BACK",
                    arg="KEYCODE_BACK",
                    valid=True)
        it.setvar('mod', 'none')
        m = it.add_modifier('cmd', 'Long press ' + arg)
        m.setvar('mod', 'cmd')
        itemCount += 1

    # Home
    title = "Home"
    
    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="KEYCODE_HOME",
                    arg="KEYCODE_HOME",
                    valid=True)

        it.setvar('mod', 'none')
        m = it.add_modifier('cmd', 'Long press ' + arg)
        m.setvar('mod', 'cmd')
        itemCount += 1

    # APP SWITCH
    title = "App switch"
    
    if addAll or wordMatch(arg, title + " recent"):
        it = wf.add_item(title=title,
                    uid="KEYCODE_APP_SWITCH",
                    arg="KEYCODE_APP_SWITCH",
                    valid=True)
        it.setvar('mod', 'none')
        m = it.add_modifier('cmd', 'Long press ' + arg)
        m.setvar('mod', 'cmd')
        itemCount += 1

    # REBOOT SYSTEM
    title = "Power"

    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="KEYCODE_POWER",
                    arg="KEYCODE_POWER",
                    valid=True)

        it.setvar('mod', 'none')
        m = it.add_modifier('cmd', 'Long press ' + arg)
        m.setvar('mod', 'cmd')
        itemCount += 1

    # STATUS BAR
    title = "Status bar"

    if addAll or wordMatch(arg, title):
        it = wf.add_item(title=title,
                    uid="STATUS_BAR",
                    arg="STATUS_BAR",
                    subtitle="Toggle status bar menu",
                    valid=True)

        it.setvar("function", "STATUS_BAR")
        itemCount += 1

    # KEYBOARD
    title = "Hide keyboard"
    result = run_script(CMD_CHECK_KEYBOARD)
    if (addAll or wordMatch(arg, title)) and "true" in result:
        it = wf.add_item(title=title,
                    uid="KEYCODE_ESCAPE",
                    arg="KEYCODE_ESCAPE",
                    valid=True)

        it.setvar('mod', 'none')
        itemCount += 1

    # OTHER KEYEVENTS
    if re.match("keycode_\w*", arg.lower()):
        it = wf.add_item(title="Other keyevents",
                            subtitle="input keyevent " + arg.upper(),
                            arg=arg.upper(),
                            valid=True)

        it.setvar('mod', 'none')
        m = it.add_modifier('cmd', 'Long press ' + arg.upper())
        m.setvar('mod', 'cmd')
        itemCount += 1

    # INPUT TEXT
    if itemCount == 0:
        log.debug("arg :" + arg)
        it = wf.add_item(title="Input as text",
                        subtitle="input text " + arg,
                        arg=arg,
                        valid=True)
        it.setvar("function", "text")
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
