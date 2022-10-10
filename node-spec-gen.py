import platform
from sys import version_info
from time import strftime, localtime
from os.path import abspath, dirname

logger_file = "{}\\LOG-{}.txt".format(dirname(abspath(__file__)), strftime("%m-%d-%Y_%H-%M-%S", localtime()))
info_to_log = []

def log(string_to_file:str=None, quit_logging:bool=False):
    global info_to_log
    if string_to_file is not None:
        print(string_to_file)
        info_to_log.append(string_to_file+"\n")
    if quit_logging is True:
        f = open(logger_file, "w+")
        f.write("".join(info_to_log))
        f.close()
        print("LOG FILE SAVED TO: {}".format(logger_file))

log("System Platform Type: {}".format(platform.platform()))
log("Referenced Python Version: {}.{}.{}".format(version_info.major, version_info.minor, version_info.micro))
try:
    import tkinter
    log("Tkinter Import Successful")
except Exception as e:
    log("Tkinter Import Error:\n{}".format(e))

try:
    from serial.tools import list_ports
    log("Serial Lib Import Successful")
except Exception as e:
    log("ERROR: Unable to Import Serial Lib\n{}\nCannot continue with System Analysis.\nPlease Install serial Ex.\n\npip install serial\n".format(e), True)
    quit()

input("Please connect Node to your computer via USB\nPress [enter] to continue... ")
log("Performing Port Analysis...")
target_dev = []
ports = list(list_ports.comports())
log("USB Connections Found: {}".format(len(ports)))
for port in ports:
    log("###### {} ######".format(port.device))
    log("Device: %s" % port.device)
    log("Name: %s" % port.name)
    log("Description: %s" % port.description)
    log("HWID: %s" % port.hwid)
    log("VID: %s" % port.vid)
    log("PID: %s" % port.pid)
    log("Serial Number: %s" % port.serial_number)
    log("Location: %s" % port.location)
    log("Manufacturer: %s" % port.manufacturer)
    log("Product: %s" % port.product)
    log("Interface: %s" % port.interface)
    log("################\n")
    if str(port.vid) == "6790" and str(port.pid) == "29987":
        if port.hwid.split(":")[1].split("=")[1] == "1A86":
            target_dev.append(port)

if len(target_dev) == 0:
    log("Node not found", True)
    quit()
elif len(target_dev) > 1:
    log("Too many conflicting serial devices plugged in\nPlease try again after disconnecting all devices except Node", True)
    quit()
elif len(target_dev) == 1:
    port = target_dev[0]
    log("Node Found on port: {}\n".format(target_dev[0].device))
else:
    log("Unexpected Serial Result\nHalting Program", True)
    quit()

log(quit_logging=True)
