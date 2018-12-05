import os
import sys
import re
import pickle
from workflow import Workflow3
from item import Item

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
                historyWifiDevices.append(item)
                
        if historyWifiDevices:
            wf.store_data("wifi_history", pickle.dumps(historyWifiDevices))


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
