import os
import sys
import pipes
from workflow import Workflow
from toolchain import run_script
import subprocess

adb_path = os.getenv('adb_path')
apkFileOrFolder = os.getenv('apkFile')
aapt_path = os.getenv('aapt_path')
apksigner_path = os.getenv("apksigner_path")

def main(wf):

    hash = sys.argv[1]
    apkPath = pipes.quote(apkFileOrFolder)
    cmd = "{0} verify -v --print-certs {1}".format(apksigner_path, apkPath)
    
    result = ""
    verified = False
    try:
        result = run_script(cmd)
        verified = True
    except subprocess.CalledProcessError as exc:
        log.error("Not verified")
        result = exc.output.decode('utf8')

    log.warning(result)
    log.warning("result--end")

    wf.cache_data('apk_print_cert' + hash, result+ "\n{}".format(verified))


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))