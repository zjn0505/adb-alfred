import os
import sys
from toolchain import run_script

emulator_path = os.getenv('emulator_path')


shell_cmd = "{0} -avd {1}".format(emulator_path, sys.argv[1])

result = run_script(shell_cmd)