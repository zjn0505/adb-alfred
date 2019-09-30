import subprocess
import os
import sys
from workflow import Workflow3
from item import Item

def main(wf):
    arg = ""
    if wf.args:
        arg = wf.args[0].strip()
        log.debug(arg)
    
    the_dir = subprocess.check_output(["osascript", "scripts/getFinder.applescript"]).strip().decode("utf-8")

    log.debug("dir")
    log.debug(the_dir)
    arr = os.listdir(the_dir)

    log.debug("length {0}".format(len(arg)))
    log.debug("file length {0}".format(len(arr)))
    for file in arr:
        if file.endswith(".apk"):
            log.debug(file)
            if len(arg) > 0 and (arg.lower() not in file.lower()):
                continue
            fullPath = os.path.join(the_dir, file)
            wf.add_item(title=file, subtitle=fullPath, uid=file, arg=fullPath, valid=True)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
