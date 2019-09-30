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
    
    the_dir = subprocess.check_output(["osascript", "scripts/getFinder.applescript"])
    the_dir = the_dir.strip()
    log.debug("dir {}".format(the_dir))
    arr = os.listdir(the_dir.encode("utf-8"))

    log.debug("length {0}".format(len(arg)))
    for file in arr:
        if file.endswith(".apk"):
            fileUtf = file.decode("utf-8")
            if len(arg) > 0 and (arg.lower() not in fileUtf.lower()):
                continue
            log.debug("File " + fileUtf)
            fullPath = os.path.join(the_dir, file)
            # log.debug(fullPath)
            wf.add_item(title=file, subtitle=fullPath, uid=file, arg=fullPath, valid=True)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
