import sys
import os
from workflow import Workflow

def main(wf):

    name = os.getenv("his_tag")
    lastFuncs = wf.cached_data('last_func:' + name, max_age=0)
    if lastFuncs and len(lastFuncs) > 0:
        lastFuncs.reverse()
        i = len(lastFuncs)
        for cmd in lastFuncs:
            i-=1
            it = wf.add_item(title=cmd,
                    arg=cmd,
                    match=cmd.replace(":", " ").replace("_", " ").replace(".", " "),
                    valid=True)
            it.setvar("last_func", cmd)
            it.setvar("function", cmd)
            it.setvar("index", i)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))