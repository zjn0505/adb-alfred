import subprocess
import os
import sys

def run_script(cmd):
	sys.stderr.write("\n Execute command: " + cmd + "\n")
	result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).strip()
	sys.stderr.write("\n Result: " + result + "\n")
	return result

def call_script(cmd):
	FNULL = open(os.devnull, 'w')
	result = subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
	return result