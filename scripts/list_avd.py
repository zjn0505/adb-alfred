import os
import sys
from toolchain import run_script

emulator_path = os.getenv('emulator_path')
func = os.getenv("func")

shell_cmd = "{0} -avd {1} {2}".format(emulator_path, sys.argv[1], func)

if func is None:
  shell_cmd = "{0} -avd {1}".format(emulator_path, sys.argv[1])

result = run_script(shell_cmd)
