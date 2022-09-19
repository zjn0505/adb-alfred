import os
import sys
from workflow import Workflow
from toolchain import run_script
from commands import CMD_DUMP_STACK

mod = os.getenv('function')[11:]

class Activity():
    def __init__(self, name, package, affinity=None, pid=None):
        self.name = name
        self.package = package
        self.affinity = affinity
        self.pid = pid

    def setAffinity(self, affinity):
        self.affinity = affinity
        return self

    def setPid(self, pid):
        self.pid = pid
        return self

def main(wf):
    # try:
    result = run_script(CMD_DUMP_STACK)

    stackData = result.split("\n")
    log.debug("stackData")
    log.debug(stackData)

    if stackData:
        activityList = []
        for index in range(len(stackData)):
            data = stackData[index].strip()
            if index % 3 == 0:
                # Hist: * Hist #0: ActivityRecord{118a7ef u0 com.roboteam.teamy.china/com.roboteam.teamy.home.HomeActivity t1564}
                start = data.find(" u0 ") + 4
                activityData = data[start:data.find(" ", start)]
                packageName = activityData.split("/")[0]
                log.debug("activityData")
                log.debug(activityData)
                activityName = activityData.split("/")[1]
                if activityName.startswith("."):
                    activityName = packageName + activityName

                activityList.append(Activity(name=activityName, package=packageName))
            elif index % 3 == 1:
                # ProcessRecord:  app=ProcessRecord{8b2b5e1 1333:com.android.settings/1000}
                activityList[-1] = activityList[-1].setPid(stackData[index].strip()[26:].split(":")[0])
            elif index % 3 == 2:
                # taskAffinity:    taskAffinity=com.android.settings
                activityList[-1] = activityList[-1].setAffinity(stackData[index].strip()[13:])
        
        for item in activityList:
            if mod == "first_app" and item.package != activityList[0].package:
                continue
            elif mod == "first_stack" and item.affinity != activityList[0].affinity:
                continue
            simpleName = item.name.split('.')[-1]
            it = wf.add_item(title=item.name,
                subtitle='Affinity: ' + item.affinity + " Pid: " + item.pid,
                autocomplete=simpleName,
                match=simpleName,
                arg=item.name,
                copytext=item.name,
                valid=True)
            m = it.add_modifier("cmd", subtitle="Package: " + item.package)
            m.setvar("package", item.package)
            m = it.add_modifier("alt", subtitle="Uninstall: " + item.package, arg = item.package)
            m.setvar("package", item.package)
            m.setvar("func", "uninstall_app")
            m = it.add_modifier("ctrl", subtitle="Force stop: " + item.package, arg = item.package)
            m.setvar("package", item.package)
            m.setvar("func", "force_stop")
            m = it.add_modifier("fn", subtitle="Clear data: " + item.package, arg = item.package)
            m.setvar("package", item.package)
            m.setvar("func", "clear_app_data")
            m = it.add_modifier("shift", subtitle="Show app info: " + item.package, arg = item.package)
            m.setvar("package", item.package)
            m.setvar("func", "app_info")
            
    wf.send_feedback()
    # except Exception as e:
    #     log.debug("Error")
    #     log.error(e)


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))