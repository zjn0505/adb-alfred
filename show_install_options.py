import subprocess
import os
import sys
import re
import shlex
from workflow import Workflow, ICON_INFO, ICON_NOTE, ICON_ERROR, ICON_WARNING
from toolchain import run_script
from workflow.background import is_running, run_in_background
import hashlib

adb_path = os.getenv('adb_path')
aapt_path = os.getenv('aapt_path')
serial = os.getenv('serial')
apkFileOrFolder = os.getenv('apkFile')
deviceApi = os.getenv('device_api')
apksigner_path = os.getenv("apksigner_path")

needsTestFlag = False
needsDowngradeFlag = False
hasDangerousPermission = False
validApkByApiCheck = True
isDebuggable = False

dangerousPermissions = [
    "android.permission.READ_CALENDAR",
    "android.permission.WRITE_CALENDAR",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "android.permission.PROCESS_OUTGOING_CALLS",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_PHONE_STATE",
    "android.permission.READ_PHONE_NUMBERS",
    "android.permission.CALL_PHONE",
    "android.permission.ANSWER_PHONE_CALLS",
    "android.permission.ADD_VOICEMAIL",
    "android.permission.USE_SIP",
    "android.permission.BODY_SENSORS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_SMS",
    "android.permission.RECEIVE_WAP_PUSH",
    "android.permission.RECEIVE_MMS",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.SYSTEM_ALERT_WINDOW",
    "android.permission.WRITE_SETTINGS"
]

def showApkInstallItems():

    global needsTestFlag
    global needsDowngradeFlag
    global hasDangerousPermission
    global validApkByApiCheck
    global isDebuggable

    arg = wf.args[0].strip()

    apkPath = shlex.quote(apkFileOrFolder)
    log.debug("Path {0}".format(apkPath))
    apk = None
    if not aapt_path:
        head, tail = os.path.split(apkPath)
        wf.add_item(title=tail, subtitle=apkPath, copytext=tail, arg=apkPath, valid=True)
        wf.add_item(title="aapt not found", subtitle="Please config 'aapt_path' in workflow settings for richer APK info", valid=False, icon=ICON_WARNING)
        if not apksigner_path:
            wf.add_item(title="apksigner not found", subtitle="Please config 'apksigner_path' in workflow settings for richer APK info", valid=False, icon=ICON_WARNING)
    else:
        cmd_dump_badging = r"{0} dump badging {1} |  grep 'package:\|application-label:\|dkVersion:\|uses-permission:\|application-debuggable\|testOnly='".format(aapt_path, apkPath)
        cmd_list_all = "{0} list -a {1} |  grep 'sharedUserId'".format(aapt_path, apkPath)
        result_dump = run_script(cmd_dump_badging)
        is_system_app = False
        try: 
            is_system_app = run_script(cmd_list_all).find("android.uid.system") > 0
        except:
            log.debug("Failed to dump sharedUserId")
        log.debug("result dump " + result_dump)
        log.debug("Is system app " + str(is_system_app))

        if result_dump:
            log.debug("Show results")
            log.debug(result_dump)
            infos = result_dump.rstrip().split('\n')
            if infos:
                apk = {}
                permissions = []
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
                    elif info.startswith("testOnly="):
                        needsTestFlag = True
                    elif serial and info.startswith("application-debuggable"): # no need to check debuggable if no device selected
                        isDebuggable = True
                    elif info.strip().startswith("uses-permission:"):
                        permissions.append(info.strip()[23:-1])

                if set(permissions) & set(dangerousPermissions):
                    log.debug(set(permissions) & set(dangerousPermissions))
                    hasDangerousPermission = True

                if "label" not in apk:
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

                    if deviceApi and "min" in apk and int(deviceApi) < apk["min"]:
                        validApkByApiCheck = False
                    if deviceApi and "max" in apk and int(deviceApi) > apk["max"]:
                        validApkByApiCheck = False

                    currentApkResult = ""
                    currentVersionCode = ""

                    if serial:
                        shell_cmd = r"{0} -s {1} shell dumpsys package {2} | grep 'versionCode\|versionName' | awk '{{print $1}}'".format(adb_path, serial, apk["packName"])

                        try:
                            currentApkResult = run_script(shell_cmd)
                        except subprocess.CalledProcessError as e:
                            log.debug(e)

                    if currentApkResult:
                        infos = currentApkResult.rstrip().split('\n')
                        log.debug(infos)
                        currentVersionCode = infos[0][12:].strip()
                        if int(currentVersionCode) > int(apk["versionCode"].strip()):
                            needsDowngradeFlag = True
                    subtitle = apk["packName"]
                    if is_system_app:
                        subtitle = apk["packName"] + " ⚠️ sharedUserId=\"android.uid.system\" ⚠️"

                    it = wf.add_item(title="{0} - {1}({2})".format(apk['label'], apk["versionName"], apk["versionCode"]), subtitle=subtitle, copytext=apk["packName"], arg=apkFileOrFolder, valid=validApkByApiCheck)
                    it.setvar('apkFile', [apkFileOrFolder])
                    
                    installOptions = ""
                    if "t" in arg:
                        installOptions = installOptions + "t"
                    
                    if "d" in arg:
                        installOptions = installOptions + "d"

                    if "g" in arg:
                        installOptions = installOptions + "g"
                        
                    if "b" in arg:
                        installOptions = installOptions + "b"

                    it.setvar('option', installOptions)

                    if "min" in apk:
                        it.add_modifier('cmd', "minSdkVersion {0}".format(apk["min"]))
                    
                    if "max" in apk:
                        it.add_modifier('alt', "maxSdkVersion {0}".format(apk["max"]))
                    else:
                        it.add_modifier('alt', "maxSdkVersion not set")

                    if "target" in apk:
                        it.add_modifier('ctrl', "targetSdkVersion {0}".format(apk["target"]))

                    if not apksigner_path:
                        wf.add_item(title="apksigner not found", subtitle="Please config 'apksigner_path' in workflow settings for richer APK info", valid=False, icon=ICON_WARNING)
                        
                    if currentVersionCode:    
                        it = wf.add_item(title="Current version - {0}({1})".format(infos[1][12:].strip(), currentVersionCode), valid=False)
                        mod = it.add_modifier('cmd', subtitle='Uninstall currently installed version first, then install selected apk file', valid=True)
                        mod.setvar("function", "uninstall_app")
                        mod.setvar("package", apk["packName"])

                        wf.setvar("pack_name", apk["packName"])
                        wf.setvar("version_code", apk["versionCode"])
                        wf.setvar("version_name", apk["versionName"])
                        wf.setvar("app_name", apk['label'])

                    if deviceApi and "min" in apk and int(deviceApi) < apk["min"]:
                        wf.add_item(title="Incompatiable device", subtitle="current device api level is {1}, lower than apk minSdkVersion {0}, ".format(deviceApi, apk["min"]), icon=ICON_ERROR, valid=False)
                    if deviceApi and "max" in apk and int(deviceApi) > apk["max"]:
                        wf.add_item(title="Incompatiable device", subtitle="current device api level is {1}, higher than apk maxSdkVersion {0}, ".format(deviceApi, apk["max"]), icon=ICON_ERROR, valid=False)


    return apk

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
    global needsTestFlag
    global needsDowngradeFlag
    global hasDangerousPermission
    global validApkByApiCheck
    global isDebuggable

    arg = wf.args[0].strip()
    log.debug(arg)
    apk = None
    fileCount = 1

    if os.path.isdir(apkFileOrFolder):
        if os.getenv('focused_app') != None:
            wf.warn_empty(title="Can't open a folder with hotkey, try apk files.")

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
        apk = showApkInstallItems()

    if fileCount == 0:
        wf.warn_empty(title="No APK files find under current path", subtitle=apkFileOrFolder)
    elif validApkByApiCheck:
        installOptions = []

        if "t" not in arg and needsTestFlag:
            wf.add_item(title="Add 't' to allow test APK to be installed", subtitle="This apk is test only", icon=ICON_WARNING, valid=False)
        elif "t" in arg and needsTestFlag:
            installOptions.append("t")
        
        # Since API 24 Android 7.0 downgrade no longer works unless apk is debuggable
        if "d" not in arg and (not serial or (needsDowngradeFlag and ((int(deviceApi) < 24) or isDebuggable))):
            wf.add_item(title="Add 'd' to allow version downgrade", icon=(ICON_WARNING, ICON_INFO)[not serial], valid=False)
        elif "d" in arg and (not serial or (needsDowngradeFlag and ((int(deviceApi) < 24) or isDebuggable))):
            installOptions.append("d")
        elif serial and int(deviceApi) >= 24 and not isDebuggable and needsDowngradeFlag:
            wf.add_item(title="Can't do downgrade installation", icon=ICON_ERROR, valid=False)

        # Only after API 23 Android 6.0, arg 'g' can be used for grant permission
        if  "g" not in arg and (not serial or int(deviceApi) > 22) and hasDangerousPermission:
            wf.add_item(title="Add 'g' to grant all permissions", icon=ICON_INFO, valid=False)
        elif 'g' in arg and (not serial or int(deviceApi) > 22) and hasDangerousPermission:
            installOptions.append("g")
            
        # Only after API 34 Android 14, arg 'l' can be used to bypass low target sdk block, https://developer.android.com/about/versions/14/behavior-changes-all#minimum-target-api-level
        if  "b" not in arg and (not serial or int(deviceApi) >= 34) and apk["target"] < 23:
            wf.add_item(title="Add 'b' to bypass low target sdk block", icon=ICON_INFO, valid=False)
        elif 'b' in arg and (not serial or int(deviceApi) >= 34) and apk["target"] < 23:
            installOptions.append("b")

        wf.setvar("option", installOptions)

        # add "-" to apksigner path will disable signature check
        if (apksigner_path != None and apksigner_path != "" and (not apksigner_path.startswith("-")) and apk != None):
            log.debug("Apksigner path " + apksigner_path)

            hash = hashlib.md5(apkFileOrFolder.encode("utf-8")).hexdigest()
            result = wf.cached_data('apk_print_cert' + hash, max_age=0)

            if not wf.cached_data_fresh('apk_print_cert' + hash, max_age=30):
                run_in_background('apk_dump', ['/usr/bin/python3',
                                    wf.workflowfile('apk_print_cert.py'), hash])

            log.debug("Cert Result || " + result+ " ||")

            if result:
                log.debug(result)
                infos = result.rstrip().split('\n')
                v1Verified = False
                v2Verified = False
                v3Verified = False
                v4Verified = None
                error = []
                signer = []

                reg = re.compile(r"^Signer #(\d+) certificate (.*):(.*)")

                for info in infos:
                    if info.startswith("Verified using v1 scheme") and info.endswith("true"):
                        v1Verified = True
                    elif info.startswith("Verified using v2 scheme") and info.endswith("true"):
                        v2Verified = True
                    elif info.startswith("Verified using v3 scheme") and info.endswith("true"):
                        v3Verified = True
                    elif info.startswith("Verified using v4 scheme"):
                        v4Verified = info.endswith("true")
                    elif info.startswith("ERROR"):
                        error.append(info)

                    a = reg.search(info)
                    if a != None and len(a.groups()) == 3:
                        i = int(a.group(1))
                        key = a.group(2)
                        value = a.group(3)
                        log.debug("KEYKEY " + key + " !!")
                        if key == "DN":
                            signer.append({})
                            signer[i-1]["DN"] = a.group(3)
                        elif "SHA-256 digest" in key:
                            log.debug(a.group(3))
                            signer[i-1]["SHA256"] = a.group(3)
                        elif "SHA-1 digest" in key:
                            signer[i-1]["SHA1"] = a.group(3)
                        elif "MD5 digest" in key:
                            signer[i-1]["MD5"] = a.group(3)
                
                title = "Signature " + infos[0]
                if infos[0] == "Verifies":
                    title = "Signature verified"
                if v4Verified != None:
                    subtitle = "Scheme V1 {0}, V2 {1}, V3 {2} V4 {3}".format(v1Verified, v2Verified, v3Verified, v4Verified)
                else:
                    subtitle = "Scheme V1 {0}, V2 {1}, V3 {2}".format(v1Verified, v2Verified, v3Verified)
                if result.endswith("True") == True:
                    log.error("Cert verified")
                    wf.add_item(title=title, subtitle=subtitle, icon=ICON_INFO, valid=False)
                else:
                    log.error("Cert not verified")
                    if len(error) > 0:
                        subtitle = error[0]
                    wf.add_item(title=title, subtitle=subtitle, icon=ICON_ERROR, valid=False, copytext=subtitle)
                    log.error(infos)
                log.debug(signer)
                for i in range(len(signer)):
                    item = signer[i]

                    sha256 = "SHA-256:{0}".format(item["SHA256"])
                    sha1 = "SHA-1:{0}".format(item["SHA1"])
                    md5 = "MD5:{0}".format(item["MD5"])
                    title = "Signer #{0} {1}".format(i, md5)
                    if sha1:
                        it = wf.add_item(title=title, subtitle=item["DN"], icon=ICON_INFO, valid=False, copytext=sha1)
                        if sha1:
                            it.add_modifier('cmd', subtitle=sha1, valid=False)
                        if sha256:
                            it.add_modifier('alt', subtitle=sha256, valid=False)

        if os.getenv("from_shortcut"):
            idx = 1
            while idx > 0:
                config = os.getenv('self_script_app_%d' % idx)
                if config:
                    title = config.split("|")[0]
                    path = config.split("|")[1]
                    it = wf.add_item(title=title,
                                subtitle="with script: %s" % path,
                                arg=path,
                                valid=True)
                    if apk and apk["packName"]:
                        it.setvar("package", apk["packName"])
                    it.setvar("self_script_app", config)
                    mod = it.add_modifier("cmd", subtitle="apply cmd modifier")
                    mod.setvar("mod", "cmd")
                    mod = it.add_modifier("alt", subtitle="apply alt modifier")
                    mod.setvar("mod", "alt")
                    mod = it.add_modifier("ctrl", subtitle="apply ctrl modifier")
                    mod.setvar("mod", "ctrl")
                    mod = it.add_modifier("fn", subtitle="apply fn modifier")
                    mod.setvar("mod", "fn")
                    mod = it.add_modifier("shift", subtitle="apply shift modifier")
                    mod.setvar("mod", "shift")
                    idx = idx + 1
                else:
                    idx = -1

        if is_running('apk_dump'):
            wf.rerun = 1
            if result:
                wf.add_item('Updating APK certs...', subtitle="Please wait a bit for the results", icon=ICON_NOTE)
            else:
                wf.add_item('Checking APK certs...', subtitle="Please wait a bit for the results", icon=ICON_NOTE)
                    
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
