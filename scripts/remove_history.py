import os
import sys
import pickle
from workflow import Workflow3

ip = os.getenv('ip')
extra = os.getenv('extra')

def main(wf):

	historyWifiDevices = []
	history = wf.stored_data("wifi_history")
	if history:
		historyWifiDevices = pickle.loads(history)
		if extra == "all":
			historyWifiDevices = []
		elif historyWifiDevices:
			for historyWifiDevice in historyWifiDevices:
				if historyWifiDevice.title == ip:
					historyWifiDevices.remove(historyWifiDevice)
					break
		wf.store_data("wifi_history", pickle.dumps(historyWifiDevices))
		print("Connection history removed")

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))