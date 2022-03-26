import os
import sys
import re
import pickle
import ipaddress
from toolchain import run_script
from workflow import Workflow3
from workflow.background import run_in_background, is_running
from item import Item
import hashlib

GITHUB_SLUG = 'zjn0505/adb-alfred'
VERSION = open(os.path.join(os.path.dirname(__file__),
                            '../version')).read().strip()
 
adb_path = os.getenv('adb_path')

regexIp = "^((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\.)){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))"

regexIpInput = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){0,3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])?(:|:5|:55|:555|:5555)?$"

regexConnect = "^connect .*"

def get_property(name=None):
    infos = run_script(adb_path + " -s " + name + " shell getprop | grep 'ro.build.version.release]\|ro.build.version.sdk]\|ro.product.manufacturer]\|ro.product.model\|ro.build.display.id]\|ro.build.version.incremental]' | awk -F'[][]' -v n=2 '{ print $(2*n) }'")
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
        mod_alt = ""
        if values[1] == 'offline':
            title = name + " [OFFLINE]"
        elif values[1] == 'connecting':
            title = name + " [CONNECTING]"
        else:
            title = name
            infos = get_property(name)
            if not infos or len(infos) < 6:
                continue
            manufacturer = infos[4].title()
            model = infos[5].title()
            valid = True
            subtitle = "%s - %s - Android %s, API %s" % (manufacturer, model, infos[2], infos[3])
            mod_alt = "%s - %s" % (infos[0], infos[1])

        it = Item(title=title, autocomplete=name, valid=valid, arg=name, subtitle=subtitle)
        it.setvar('status', values[1])
        if valid:
            it.setvar('device_api', infos[3])
        it.setvar('name', model)
        it.setvar('serial', values[0])
        it.setvar('build_number', mod_alt)
        
        items.append(it)
        if it and re.match(regexIp + ":5555", name):
            log.debug("add " + name)

            # if name ends 5555, add to wifiDevices.
            wifiDevices.append(it)

    return items, wifiDevices

def list_devices(args):

    arg = args[0] if args else ''

    devices = run_script(adb_path + " devices -l | sed -n '1!p' | tr -s ' '")
    devices = devices.rstrip().split('\n')

    items, wifiDevices = get_device_items(arg, devices)

    if wifiDevices:
        run_in_background("update_wifi_history",
                           ['/usr/bin/python3',
                            wf.workflowfile('scripts/update_wifi_history.py'), 'add', pickle.dumps(wifiDevices)])
        log.error("Save history wifi devices : count : {0}".format(len(wifiDevices)))
    
    for item in items:
        name = item.get('serial')
        log.debug(arg + " " + name)
        if arg == '' or arg.lower() in name.lower():
            it = wf.add_item(title=item.title, uid=item.title, autocomplete=('', item.autocomplete)[item.valid], valid=item.valid, arg=item.arg, subtitle=item.subtitle)
            it.setvar('status', item.get("status"))
            it.setvar('full_info', item.subtitle)
            if item.valid:
                it.setvar('device_api', item.get('device_api'))
            it.setvar("serial", name)
            it.setvar('name', item.get('name'))
            if item.subtitle and not re.match(regexIp + ":5555", name):
                cmd_ip = adb_path + ' -s ' + name + " shell ip -f inet addr show wlan0 | grep inet | tr -s ' ' |  awk '{print $2}'"
                ip = run_script(cmd_ip)
                if '/' in ip and re.match(regexIp, ip.split('/')[0]):
                    it.setvar("ip", ip.strip('\n'))
                    it.add_modifier("cmd", subtitle=ip)
            if item.get("build_number"):
                it.add_modifier("alt", subtitle=item.get("build_number"))

            # last func
            if name.startswith("emulator-"):
                name = hashlib.md5(item.subtitle).hexdigest()
            it.setvar("his_tag", name)
            lastFuncs = wf.cached_data('last_func:' + name, max_age=0)
            if lastFuncs and len(lastFuncs) > 0:
                log.debug(lastFuncs)
                last_func = lastFuncs[len(lastFuncs) - 1]
                mod = it.add_modifier("ctrl", subtitle="run last command {}".format(last_func))
                mod.setvar("last_func", last_func)
                mod = it.add_modifier("fn", subtitle="show command history", arg="cmd_history")
                mod.setvar("function", "cmd_history")
                if len(lastFuncs) > 1:
                    second_last_func = lastFuncs[len(lastFuncs) - 2]
                    mod = it.add_modifier("shift", subtitle="run 2nd last command {}".format(second_last_func))
                    mod.setvar("last_func", second_last_func)

    # CONNECT
    if arg and ("connect ".startswith(arg.lower()) or re.match(regexConnect, arg)):
        localIpWithMask = run_script('ifconfig | grep -A 1 "en" | grep broadcast | cut -d " " -f 2,4 | tr "\\n" " "')

        localIp = localIpWithMask.split(" ")[0]
        rawMask = localIpWithMask.split(" ")[1].count("f") * 4
    
        targetIp = arg[8:]
        
        if localIp:
            log.debug("history " + localIp)
            history = wf.stored_data("wifi_history_py3")
            log.debug(history)
            
            counter = 0
            valid = True if re.match("^" + regexIp + "(:|:5|:55|:555|:5555)?$", targetIp) else False

            if valid:
                subtitle = "adb connect " + targetIp if targetIp else ''
                it = wf.add_item(title="Connect over WiFi", valid = valid, arg="adb_connect", subtitle=subtitle)
                m = it.add_modifier('cmd', subtitle="Remove all connection histories", arg='adb_connect_remove')
                m.setvar('extra', "all")
                it.setvar("ip", targetIp.strip('\n'))
        
            if history:
                historyWifiDevices = pickle.loads(history)
                currentDevices = []
                for item in items:
                    currentDevices.append(item.title.strip())
                
                for historyWifiDevice in historyWifiDevices:
                    if not historyWifiDevice.title in currentDevices:
                        deviceIp = historyWifiDevice.title.split(":")[0]
                        same_network = False
                        if hasattr(historyWifiDevice, 'mask') and historyWifiDevice.mask:
                            same_network = ipaddress.ip_network(u'%s/%d' % (localIp, rawMask), False) == ipaddress.ip_network(u'%s/%s' % (deviceIp, historyWifiDevice.mask), False)
                        else:
                            same_network = ipaddress.ip_network(u'%s/%d' % (localIp, rawMask), False) == ipaddress.ip_network(u'%s/%d' % (deviceIp, rawMask), False)

                        if not same_network:
                            continue
                        if arg and historyWifiDevice.title.find(targetIp) == -1:
                            continue

                        log.debug("history item title " + historyWifiDevice.title)
                        
                        title = "Connect over WiFi"
                        if historyWifiDevice.subtitle:
                            title = "Connect " + historyWifiDevice.subtitle.split('- ', 1)[1].split(', ', 1)[0] + " over WiFi"

                        it = wf.add_item(title=title, valid = True, arg="adb_connect", autocomplete="connect " + historyWifiDevice.title, subtitle=historyWifiDevice.title, uid=(historyWifiDevice.title, "")[valid])
                        it.setvar("ip", historyWifiDevice.title)
                        it.add_modifier('cmd', 'Remove connection history with {0}'.format(historyWifiDevice.title), arg='adb_connect_remove')
                        it.add_modifier('alt', historyWifiDevice.subtitle)
                        counter += 1

            if not valid and counter == 0:
                if (not targetIp or re.match(regexIpInput, targetIp)):
                    subtitle = "adb connect " + targetIp if targetIp else ''
                    if not targetIp:
                        it = wf.add_item(title="Connect over WiFi", valid = False, arg="adb_connect", autocomplete="connect ", subtitle=subtitle)
                    else:
                        it = wf.add_item(title="Connect over WiFi", valid = False, arg="adb_connect", subtitle=subtitle)
    
    # DISCONNECT
    if wifiDevices:
        log.debug(wifiDevices[0].title)

    if arg and ("disconnect ".startswith(arg.lower()) or re.match("^disconnect .*", arg)):
        targetIp = arg[11:]
        
        if wifiDevices:
            for wifiDevice in wifiDevices:
                it = wf.add_item(title="Disconnect from WiFi", uid=wifiDevice.title, valid = True, arg="adb_disconnect", autocomplete="disconnect ", subtitle=wifiDevice.title)
                ip = wifiDevice.title
                if  "[OFFLINE]" in ip:
                    ip = ip.split(" ")[0]

                it.setvar("ip", ip)
        elif targetIp:
            it = wf.add_item(title="Disconnect from WiFi", uid="adb_disconnect", valid = True, arg="adb_disconnect", autocomplete="disconnect ", subtitle="adb disconnect " + targetIp)
            it.setvar("ip", targetIp)

    if arg and ("restart".startswith(arg.lower()) 
        or "kill-server".startswith(arg.lower())
        or "start-server".startswith(arg.lower())) or (
            len(items) == 0 and (len(arg) == 0 or (not arg.lower().startswith("connect") and not arg.lower().startswith("disconnect")))): 
        wf.add_item(title="Restart adb", valid =True, arg="restart_adb", uid="restart_adb")

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
    log.debug("Hello from adb")
    if wf.update_available:
        wf.add_item(u'New version available',
                    u'Action this item to install the update',
                    autocomplete=u'workflow:update')
    sys.exit(wf.run(main))
