import subprocess
import os
import sys
import re
import pipes
from workflow import Workflow3, ICON_WARNING, ICON_INFO, ICON_ERROR, web
 
reload(sys)
sys.setdefaultencoding("utf-8")

adb_path = os.getenv('adb_path')
aapt_path = os.getenv('aapt_path')
serial = os.getenv('serial')
apkFileOrFolder = pipes.quote(os.getenv('apkFile'))
deviceApi = os.getenv('device_api')

def showApkInstallItems():

    arg = wf.args[0].strip()

    if not aapt_path:
        head, tail = os.path.split(apkFileOrFolder)
        wf.add_item(title=tail, subtitle=apkFileOrFolder, copytext=tail, arg=apkFileOrFolder, valid=True)
        wf.add_item(title="aapt not found", subtitle="Please config 'aapt_path' in workflow settings for richer APK info", valid=False, icon=ICON_WARNING)
    else:

        result = subprocess.check_output("{0} dump badging {1} |  grep 'package:\|application-label:\|dkVersion:'".format(aapt_path, apkFileOrFolder), 
            stderr=subprocess.STDOUT,
            shell=True)

        if result:
            log.debug(result)
            infos = result.rstrip().split('\n')
            if infos:
                apk = {}
                for info in infos:
                    if info.startswith("package:"):
                        apk["package"] = info
                    elif info.startswith("sdkVersion:"):
                        apk["min"] = int(info.split("'")[1])
                    elif info.startswith("maxSdkVersion:"):
                        apk["max"] = int(info.split("'")[1])
                    elif info.startswith("targetSdkVersion:"):
                        apk["target"] = int(info.split("'")[1])
                    elif info.startswith("application-label:"):
                        apk["label"] = info.split("'")[1]
                
                if not apk.has_key('label'):
                    apk["label"] = ""

                log.debug(apk)

                info0 = apk['package'].split(' ')

                if len(info0) > 3:
                    
                    for info in info0:
                        if info.startswith("name="):
                            apk["packName"] = info.split("'")[1]
                        elif info.startswith("versionCode="):
                            apk["versionCode"] = info.split("'")[1]
                        elif info.startswith("versionName="):
                            apk["versionName"] = info.split("'")[1]

                    it = wf.add_item(title="{0} - {1}({2})".format(apk['label'], apk["versionName"], apk["versionCode"]), subtitle=apk["packName"], copytext=apk["packName"], arg=apkFileOrFolder, valid=True)
                    it.setvar('apkFile', [apkFileOrFolder])
                    
                    installOptions = ""
                    if "t" in arg:
                        installOptions = installOptions + "t"
                    
                    if "d" in arg:
                        installOptions = installOptions + "d"

                    if "g" in arg:
                        installOptions = installOptions + "g"

                    it.setvar('option', installOptions)

                    if apk.has_key('min'):
                        it.add_modifier('cmd', "minSdkVersion {0}".format(apk["min"]))
                    
                    if apk.has_key('max'):
                        it.add_modifier('alt', "maxSdkVersion {0}".format(apk["max"]))

                    if apk.has_key('target'):
                        it.add_modifier('ctrl', "targetSdkVersion {0}".format(apk["target"]))

                    if deviceApi and apk.has_key("min") and deviceApi < apk["min"]:
                        wf.add_item(title="Incompatiable device", subtitle="current device api level is {1}, lower than apk minSdkVersion {0}, ".format(deviceApi, apk["min"]), icon=ICON_ERROR, valid=False)
                    if deviceApi and apk.has_key("max") and deviceApi > apk["maxs"]:
                        wf.add_item(title="Incompatiable device", subtitle="current device api level is {1}, higher than apk maxSdkVersion {0}, ".format(deviceApi, apk["max"]), icon=ICON_ERROR, valid=False)

                    if serial:
                        shell_cmd = "{0} -s {1} shell dumpsys package {2} | grep 'versionCode\|versionName' | awk '{{print $1}}'".format(adb_path, serial, apk["packName"])

                        try:
                            result = subprocess.check_output(shell_cmd, stderr=subprocess.STDOUT, shell=True)
                        except subprocess.CalledProcessError as e:
                            log.debug(e)
                        if result:
                            infos = result.rstrip().split('\n')
                            log.debug(infos)
                            it = wf.add_item(title="Current version - {0}({1})".format(infos[1][12:], infos[0][12:]), valid=False)
                            mod = it.add_modifier('cmd', subtitle='Uninstall currently installed version first, then install selected apk file', valid=True)
                            mod.setvar("function", "uninstall_app")
                            mod.setvar("package", apk["packName"])

                        wf.setvar("pack_name", apk["packName"])
                        wf.setvar("version_code", apk["versionCode"])
                        wf.setvar("version_name", apk["versionName"])
                        wf.setvar("app_name", apk['label'])


def showFolerInstallItems():
    arg = wf.args[0].strip()
    apkFilesAll = []
    apkFileDirect = []
    for subdir, dirs, files in os.walk(apkFileOrFolder):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".apk"):
                if subdir == apkFileOrFolder:
                    apkFileDirect.append(filepath)
                apkFilesAll.append(filepath)
    
    return apkFilesAll, apkFileDirect
    
def main(wf):
    arg = wf.args[0].strip()
    log.debug(arg)

    fileCount = 1
    if os.path.isdir(apkFileOrFolder):
        apkFileAll, apkFileDirect = showFolerInstallItems()
        fileCount = len(apkFileAll)
        directFileCount = len(apkFileDirect)
        if fileCount > 0:
            if directFileCount == 0 or directFileCount == fileCount:
                it = wf.add_item(title="{0} APK {1} to be installed".format(fileCount, ("files", "file")[fileCount == 1]), subtitle=apkFileOrFolder, arg=apkFileOrFolder, valid=True)
                it.setvar('apkFile', apkFileAll)
            else:
                it = wf.add_item(title="{0} APK files to be installed, {1} of them in sub-directory".format(fileCount, fileCount - directFileCount),
                            subtitle=apkFileOrFolder, arg=apkFileOrFolder, valid=True)
                it.setvar('apkFile', apkFileAll)
                mod = it.add_modifier('cmd', subtitle='only install apks under root directory', valid=True)
                mod.setvar('apkFile', apkFileDirect)
    else:
        showApkInstallItems()

    if fileCount == 0:
        wf.warn_empty(title="No APK files find under current path", subtitle=apkFileOrFolder)
    elif serial:
        installOptions = []
        if "t" not in arg:
            wf.add_item(title="Add 't' to allow test APK to be installed", icon=ICON_INFO, valid=False)
        else:
            installOptions.append("t")
        
        if "d" not in arg:
            wf.add_item(title="Add 'd' to allow version code downgrade", icon=ICON_INFO, valid=False)
        else:
            installOptions.append("d")
        log.error("deviceApi")
        log.error(deviceApi)
        if  "g" not in arg and int(deviceApi) > 22:
            wf.add_item(title="Add 'g' to grant all permissions listed in the app manifest", icon=ICON_INFO, valid=False)
        elif 'g' in arg and int(deviceApi) > 22:
            installOptions.append("g")
        wf.setvar("option", installOptions)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
