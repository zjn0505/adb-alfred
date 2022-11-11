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
        
    def __str__(self):
        return f"Activity name {self.name}, package is {self.package}, affinity is {self.affinity}, pid is {self.pid}"

def main(wf):
    # try:
    result = run_script(CMD_DUMP_STACK)

    stackData = result.split("\n")
    # log.debug("stackData")
    # log.debug(stackData)

    if stackData:
        activityList = []
        log.debug("Start")
        for index in range(len(stackData)):
            data = stackData[index].strip()
            if data.find("* Hist #") >= 0:
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
            elif data.find("app=ProcessRecord") >= 0:
                # ProcessRecord:  app=ProcessRecord{8b2b5e1 1333:com.android.settings/1000}
                log.debug("ProcessRecord")
                log.debug(data)
                activityList[-1] = activityList[-1].setPid(data[26:].split(":")[0])
            elif data.find("taskAffinity=") >= 0:
                # taskAffinity:    taskAffinity=com.android.settings
                log.debug("taskAffinity")
                log.debug(data)
                activityList[-1] = activityList[-1].setAffinity(data[13:])
        
        for item in activityList:
            log.debug(item)
            if mod == "first_app" and item.package != activityList[0].package:
                continue
            elif mod == "first_stack" and item.affinity != activityList[0].affinity:
                continue
            simpleName = item.name.split('.')[-1]

            subtitle = ""
            if item.pid == None:
                subtitle = 'Affinity: ' + item.affinity
            else:
                subtitle = 'Affinity: ' + item.affinity + " Pid: " + item.pid

            it = wf.add_item(title=item.name,
                subtitle=subtitle,
                autocomplete=simpleName,
                match=item.name,
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