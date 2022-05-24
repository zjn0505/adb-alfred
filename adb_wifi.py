import os
import time
import pickle

from workflow.background import run_in_background, is_running
from item import Item
from workflow import Workflow
from toolchain import run_script
from commands import CMD_GET_TCPIP
from commands import CMD_TCPIP
from commands import CMD_ADB_CONNECT

ip = os.getenv("ip")

def connect():
	result = run_script(CMD_ADB_CONNECT.format(ip.split("/")[0]))
	if "connected to" in result:
		it = Item(title=result.strip().split("connected to ")[1], subtitle=os.getenv("full_info"), mask=ip.split("/")[1])
		wifiDevices = []
		wifiDevices.append(it)
		run_in_background("update_wifi_history", 
			['/usr/bin/python3', wf.workflowfile('update_wifi_history.py'), 'add', pickle.dumps(wifiDevices)])
	print("Executed: " + result)

def init():
	result = run_script(CMD_GET_TCPIP)
	if result != "5555":

		run_script(CMD_TCPIP)
		time.sleep(2)
		connect()
	
	if result:
		connect()

if __name__ == '__main__':
	if ip:
		wf = Workflow()
		init()