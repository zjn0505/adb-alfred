import os
import sys
from workflow import Workflow
from toolchain import run_script
from commands import CMD_DUMP_STACK

mod = os.getenv('function')[11:]

class Activity():
    def __init__(self, name, package, affinity=None):
        self.name = name
        self.package = package
        self.affinity = affinity

    def setAffinity(self, affinity):
        self.affinity = affinity
        return self

def main(wf):
    try:
        result = run_script(CMD_DUMP_STACK)

        stackData = result.split("\n")
        log.debug(stackData)

        if stackData:
            activityList = []
            for index in range(len(stackData)):
                data = stackData[index].strip()
                if index % 2 == 0:
                    start = data.find(" u0 ") + 4
                    activityData = data[start:data.find(" ", start)]
                    packageName = activityData.split("/")[0]
                    activityName = activityData.split("/")[1]
                    if activityName.startswith("."):
                        activityName = packageName + activityName

                    activityList.append(Activity(name=activityName, package=packageName))
                else:
                    activityList[-1] = activityList[-1].setAffinity(stackData[index].strip()[13:])
            
            for item in activityList:
                if mod == "first_app" and item.package != activityList[0].package:
                    continue
                elif mod == "first_stack" and item.affinity != activityList[0].affinity:
                    continue
                simpleName = item.name.split('.')[-1]
                it = wf.add_item(title=item.name,
                    subtitle='Affinity: ' + item.affinity,
                    autocomplete=simpleName,
                    match=simpleName,
                    arg=item.name,
                    copytext=item.name,
                    valid=True)
                m = it.add_modifier("cmd", subtitle="Package: " + item.package)
                m.setvar("package", item.package)
                
        wf.send_feedback()
    except Exception as e:
        log.debug("Error")
        log.error(e)


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))