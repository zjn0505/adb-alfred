import os
import sys
from workflow import Workflow
from toolchain import run_script
from commands import CMD_DUMP_NOTIFICATION

mod = os.getenv('function')[18:]

class Notification():
    def __init__(self, package, seen=False, title=None, subtitle=None, channelId=None, channelName=None, key=None):
        self.seen = seen
        self.package = package
        self.title = title
        self.subtitle = subtitle
        self.channelId = channelId
        self.channelName = channelName
        self.key = key

    def setSeen(self, seen):
        self.seen = seen
        return self

    def setTitle(self, title):
        self.title = title
        return self

    def setSubtitle(self, subtitle):
        self.subtitle = subtitle
        return self

    def setChannelId(self, channelId):
        self.channelId = channelId
        return self

    def setChannelName(self, channelName):
        self.channelName = channelName
        return self

    def setKey(self, key):
        self.key = key
        return self
        
    def __str__(self):
        return f"Notification package is {self.package}, title is {self.title}, subtitle is {self.subtitle}, seen is {self.seen}"

def main(wf):
    log.debug("hi")
    result = run_script(CMD_DUMP_NOTIFICATION)

    notificationDumpData = result.split("\n")
    # log.debug("stackData")
    # log.debug(stackData)

    if notificationDumpData:
        notifications = []
        log.debug("Start")
        for index in range(len(notificationDumpData)):
            data = notificationDumpData[index].strip()
            if data.find("NotificationRecord(") >= 0:
                # NotificationRecord(0x06e57ae4: pkg=xyz.jienan.xkcd.debug user=UserHandle{0} id=2131362072 
                start = data.find(": pkg=") + 6
                packageName = data[start:data.find(" ", start)]
                log.debug(packageName)
                notifications.append(Notification(package=packageName))
            elif data.find("seen=") >= 0:
                # seen=true
                if data.find("seen=true") >= 0:
                    log.debug("seen")
                    notifications[-1] = notifications[-1].setSeen(True)
            elif data.find("android.title=String ") >= 0:
                notifications[-1] = notifications[-1].setTitle(data[22:-1])
            elif data.find("android.title=SpannableString ") >= 0:
                notifications[-1] = notifications[-1].setTitle(data[31:-1])
                
            elif data.find("android.text=String (") >= 0:
                notifications[-1] = notifications[-1].setSubtitle(data[21:-1])
            elif data.find("android.text=SpannableString (") >= 0:
                notifications[-1] = notifications[-1].setSubtitle(data[30:-1])

            elif data.find("effectiveNotificationChannel=NotificationChannel{mId=") >= 0:
                start = 53
                channelId = data[54:data.find("',", start)]
                notifications[-1] = notifications[-1].setChannelId(channelId)
                start = data.find("mName=") + 6
                channelName = data[start:data.find(", mDescription", start)]
                notifications[-1] = notifications[-1].setChannelName(channelName)
            elif data.startswith("key="):
                key = data[4:]
                notifications[-1] = notifications[-1].setKey(key)
            elif data.startswith("Enqueued Notification List:"):
                return
        
        for item in notifications:
            log.debug(item)
            if mod == "exclude_empty" and item.title == None and item.subtitle == None:
                continue
            it = wf.add_item(title=item.title,
                subtitle=item.subtitle,
                autocomplete=item.package,
                match=item.title,
                arg=item.title,
                copytext=item.package,
                valid=True)

            m = it.add_modifier("cmd", subtitle="Package: " + item.package)
            m.setvar("package", item.package)
            if item.channelId and item.channelName:
                m = it.add_modifier("alt", subtitle="Channel 🆔: " + item.channelId + " 🏷️: " + item.channelName, arg = item.package)
                m.setvar("channel", item.channelId)
            if item.key:
                m = it.add_modifier("ctrl", subtitle="Key: " + item.key, arg = item.package)
                m.setvar("key", item.key)
            
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))