import os
import sys
import re
import pickle
from workflow import Workflow3
from item import Item
import subprocess

adb_path = os.getenv('adb_path')

def main(wf):
    operation = sys.argv[1]

    if operation == 'add':

        items = pickle.loads(sys.argv[2])

        historyWifiDevices = []
        history = wf.stored_data("wifi_history")
        if history:
            historyWifiDevices = pickle.loads(history)

        for item in items:
            itemInDB = False
        
            for historyWifiDevice in historyWifiDevices:
                if item.title == historyWifiDevice.title and item.subtitle == historyWifiDevice.subtitle:
                    itemInDB = True
                    break

            if not itemInDB and not "[OFFLINE]" in item.title:


                cmd_ip = adb_path + ' -s ' + item.variables['serial'] + " shell ip -f inet addr show wlan0 | grep inet | tr -s ' ' |  awk '{print $2}'"
                ip = subprocess.check_output(cmd_ip,
                                       stderr=subprocess.STDOUT,
                                       shell=True)
                # historyWifiDevice.variables["ip"] = ip
                # historyWifiDevice.ip = ip

                # historyWifiDevice.variables["123123123"] = "123123123"
                if ip:
                    item.mask = ip.split('/')[1].split("\n")[0]
                historyWifiDevices.append(item)
                
        if historyWifiDevices:
            wf.store_data("wifi_history", pickle.dumps(historyWifiDevices))


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
