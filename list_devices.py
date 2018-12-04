import subprocess
import os
import sys
import re
import pickle
from workflow import Workflow3, ICON_INFO
from workflow.background import run_in_background, is_running
from item import Item

GITHUB_SLUG = 'zjn0505/adb-alfred'
VERSION = open(os.path.join(os.path.dirname(__file__),
                            'version')).read().strip()
 
adb_path = os.getenv('adb_path')

regexIp = "((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\.)){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))"

regexIpInput = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){0,3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])?$"

regexConnect = "^connect .*"

def get_property(name=None):
    infos = subprocess.check_output(
            adb_path + " -s " + name + " shell getprop | grep 'ro.build.version.release]\|ro.build.version.sdk]\|ro.product.manufacturer]\|ro.product.model]' | awk -F'[][]' -v n=2 '{ print $(2*n) }'",
            stderr=subprocess.STDOUT,
            shell=True)
    infos = infos.rstrip().split('\n')
    return infos

def get_device_items(arg, devices):
    items = []
    wifiDevices = []
    
    for device in devices:
        if not device:
            continue

        values = device.split(' ')
        name = values[0]
        it = None
        model = ""
        subtitle = ""
        title = ""
        valid = False
        if values[1] == 'offline':
            title = name + " [OFFLINE]"
        elif values[1] == 'connecting':
            title = name + " [CONNECTING]"
        else:
            title = name
            infos = get_property(name)
            if not infos or len(infos) < 3:
                continue
            manufacturer = infos[2].title()
            model = infos[3].title()
            valid = True
            subtitle = "%s - %s - Android %s, API %s" % (manufacturer, model, infos[0], infos[1])

        it = Item(title=title, autocomplete=name, valid=valid, arg=name, subtitle=subtitle)
        it.setvar('status', values[1])
        if valid:
            it.setvar('device_api', infos[1])
        it.setvar('name', model)
        it.setvar('serial', values[0])

        items.append(it)
        if it and re.match(regexIp + ":5555", name):
            log.debug("add " + name)

            # if name ends 5555, add to wifiDevices.
            wifiDevices.append(it)

    return items, wifiDevices

def list_devices(args):

    arg = args[0] if args else ''

    devices = subprocess.check_output(
            adb_path + " devices -l | sed -n '1!p' | tr -s ' '",
            stderr=subprocess.STDOUT,
            shell=True)
    devices = devices.rstrip().split('\n')

    items, wifiDevices = get_device_items(arg, devices)
    if wifiDevices:
        run_in_background("update_wifi_history",
                           ['/usr/bin/python',
                            wf.workflowfile('update_wifi_history.py'), 'add', pickle.dumps(wifiDevices)])
        log.error("Save history wifi devices : count : {0}".format(len(wifiDevices)))
    
    for item in items:
        name = item.get('serial')
        log.debug(arg + " " + name)
        if arg == '' or arg.lower() in name.lower():
            it = wf.add_item(title=item.title, autocomplete=('', item.autocomplete)[item.valid], valid=item.valid, arg=item.arg, subtitle=item.subtitle)
            it.setvar('status', item.get("status"))
            if item.valid:
                it.setvar('device_api', item.get('device_api'))
            it.setvar('name', item.get('name'))


    # CONNECT
    if arg and ("connect ".startswith(arg.lower()) or re.match(regexConnect, arg)):
        localIp = subprocess.check_output('ifconfig | grep -A 1 "en" | grep broadcast | cut -d " " -f 2 | tr "\\n" " "',
            stderr=subprocess.STDOUT,
            shell=True)
        # log.debug(localIp)

        targetIp = arg[8:]
        # log.debug(targetIp)
        if not targetIp or re.match(regexIpInput, targetIp):
            subtitle = "adb connect " + targetIp if targetIp else ''
            valid = True if re.match(regexIp, targetIp) else False
            it = wf.add_item(title="Connect over WiFi", valid = valid, arg="adb_connect", autocomplete="connect ", subtitle=subtitle)
            it.setvar("ip", targetIp)

        history = wf.stored_data("wifi_history")
        
        if history:
            log.error(history)
            historyWifiDevices = pickle.loads(history)
            log.debug(historyWifiDevices)
            currentDevices = []
            for item in items:
                log.debug("current item title " + item.title)
                currentDevices.append(item.title.strip())

            for historyWifiDevice in historyWifiDevices:
                # if not historyWifiDevice.title in currentDevices:
                log.debug("history item title " + historyWifiDevice.title)
                it = wf.add_item(title="Connect over WiFi", valid = valid, arg="adb_connect", autocomplete="connect ", subtitle=historyWifiDevice.title)
                it.setvar("ip", historyWifiDevice.title)
                it.add_modifier('cmd', 'Remove connection history with {0}'.format(historyWifiDevice.title), arg='adb_connect_remove')
    
    # DISCONNECT
    if wifiDevices:
        log.debug(wifiDevices[0].title)

    if arg and ("disconnect ".startswith(arg.lower()) or re.match("^disconnect .*", arg)):
        targetIp = arg[11:]
        
        if wifiDevices:
            for wifiDevice in wifiDevices:
                it = wf.add_item(title="Disconnect from WiFi", valid = True, arg="adb_disconnect", autocomplete="disconnect ", subtitle=wifiDevice.title)
                it.setvar("ip", wifiDevice.title)
        elif targetIp:
            it = wf.add_item(title="Disconnect from WiFi", valid = True, arg="adb_disconnect", autocomplete="disconnect ", subtitle="adb disconnect " + targetIp)
            it.setvar("ip", targetIp)

    if arg and ("restart".startswith(arg.lower()) 
        or "kill-server".startswith(arg.lower())
        or "start-server".startswith(arg.lower())) or len(items) == 0: 
        wf.add_item(title="Restart adb", valid =True, arg="restart_adb")

def main(wf):
    if not adb_path:
        wf.warn_empty(title="adb not found", subtitle="Please config 'adb_path' in workflow settings")
    else:
        list_devices(wf.args)
    wf.send_feedback()

if __name__ == '__main__':
    update_settings = {'github_slug': GITHUB_SLUG, 'version': VERSION}
    wf = Workflow3(update_settings=update_settings)
    log = wf.logger

    if wf.update_available:
        wf.add_item(u'New version available',
                    u'Action this item to install the update',
                    autocomplete=u'workflow:update',
                    icon=ICON_INFO)
    sys.exit(wf.run(main))
