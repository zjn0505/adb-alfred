import os
from toolchain import run_script
from commands import CMD_OPEN_SETTINGS

action = os.getenv('function')[14:]

if action == "":
	action = "android.settings.SETTINGS"
elif action == "developer_options":
	action = "com.android.settings.APPLICATION_DEVELOPMENT_SETTINGS"
elif action == "date":
	action = "android.settings.DATE_SETTINGS"
elif action == "wifi":
	action = "android.settings.WIFI_SETTINGS"
elif action == "accessibility":
	action = "android.settings.ACCESSIBILITY_SETTINGS"
elif action == "application":
	action = "android.settings.APPLICATION_SETTINGS"

shell_cmd = CMD_OPEN_SETTINGS.format(action)

try:
	run_script(shell_cmd)
except:
	print("Failed to open settings")