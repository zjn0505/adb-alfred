import sys
import os
from workflow import Workflow3

def main(wf):

    name = os.getenv("his_tag")
    index = os.getenv("index")

    lastFuncs = wf.cached_data('last_func:' + name, max_age=0)

    if lastFuncs and len(lastFuncs) > 0:
        
        if index:
            lastFuncs.pop(int(index))
        else:
            lastFuncs = []
        wf.cache_data('last_func:' + name, lastFuncs)

        wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))