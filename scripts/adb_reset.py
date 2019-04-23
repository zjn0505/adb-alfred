import os
from toolchain import run_script

adb_path = os.getenv('adb_path')

response = run_script('{0} kill-server && {1} start-server'.format(adb_path, adb_path))

if 'daemon started successfully' in response:
    print('adb successfully restarted')
else:
    print('Failed to restart adb')