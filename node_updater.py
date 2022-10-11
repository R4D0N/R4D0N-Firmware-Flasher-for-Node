import hashlib
import sys
import os
import platform
from time import sleep
import subprocess
#checks to confirm minimum requirements
if sys.version_info.major != 3:
    print("You must install python 3.x to run this script.")
    print('If you have installed python 3.x use\n\npython3 "%s"' % os.path.basename(__file__))
    print("\nHalting Program")
    quit()

if platform.platform().startswith("darwin") is not True:
    print("This script is not compatible with the current OS installed.\nHalting Program.")
    #REMOVE THIS
    #quit()

def tkinter_compat():
    if sys.version_info.minor < 9:
        print("ATTENTION!!!\nYou are using Python {}.{}.{} which can be unpredictable when selecting files.".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
        print("It is better to use Python 3.9.x for stability reasons.")
        choice = input("Do you wish to proceed at your own risk? (y/n) ")
        if choice.lower() == "n":
            print("Halting Program")
            quit()
        elif choice.lower() == "y":
            print("")
            return
        else:
            print("Invalid Selection...\nHalting Program")
            quit()
from tkinter.filedialog import askopenfilename, askdirectory

#########################
# Non-default libraries #
#########################
req_restart = False
try:
    from serial.tools import list_ports
except ImportError as i:
    print("{} module not found, installing...".format(i.name))
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', i.name])
    print("You will have to restart the program...")
    req_restart = True
try:
    import esptool
except ImportError as i:
    print("{} module not found, installing...".format(i.name))
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', i.name])
    print("You will have to restart the program...")
    req_restart = True

if req_restart == True:
    print("Please Relaunch Node Firmware Updater")
    quit()

def node_locating(silent_stat=True):
    target_dev = []
    ports = list(list_ports.comports())
    for port in ports:
        if str(port.vid) == "6790" and str(port.pid) == "29987":
            if port.hwid.split(":")[1].split("=")[1] == "1A86":
                target_dev.append(port)

    if len(target_dev) == 0:
        print("Node not found")
        quit()
    elif len(target_dev) > 1:
        print("Too many serial devices plugged in\nPlease try again after disconnecting all devices except Node")
        quit()
    elif len(target_dev) == 1:
        port = target_dev[0]
        print("Node Found on port: {}\n".format(target_dev[0].device))
        if silent_stat is False:
            print("###### {} ######".format(port.device))
            print("Device: %s" % port.device)
            print("Name: %s" % port.name)
            print("Description: %s" % port.description)
            print("HWID: %s" % port.hwid)
            print("VID: %s" % port.vid)
            print("PID: %s" % port.pid)
            print("Serial Number: %s" % port.serial_number)
            print("Location: %s" % port.location)
            print("Manufacturer: %s" % port.manufacturer)
            print("Product: %s" % port.product)
            print("Interface: %s" % port.interface)
            print("################\n")
        return port.device
    else:
        print("Unexpected Serial Result\nHalting Program")
        quit()

def firmware_selection():
    print("Please Select Node Firmware to Flash...\n")
    dialog = askopenfilename(title="Select Node Firmware to Flash", initialdir=os.path.dirname(os.path.abspath(__file__)),defaultextension='.bin', filetypes=[("BIN Files", '*.bin')])
    if not dialog:
        print("No Firmware Selected.\nHalting Program")
        quit()
    else:
        f = open(dialog, "rb").read()
        m = hashlib.md5(f)
        firmware_hash = m.hexdigest()

        approved_hashes = []
        ah = open("firmware_checksums", "r").readlines()
        for hash in ah:
            approved_hashes.append(hash.strip().split("#")[0])

        if firmware_hash in approved_hashes:
            return dialog
        else:
            print("{} is not a valid firmware file.\nHalting Program")
            quit()

def webpage_selection():
    dialog = askdirectory(title="Select Node Webpage Folder")
    if not dialog:
        print("No Webpage Folder Selected.\nHalting Program")
        quit()
    else:
        if "index.htm" not in os.listdir(dialog):
            print("No index.htm located in {}\nHalting Program".format(dialog))
            quit()
        else:
            return dialog


if __name__ == "__main__":
    args = sys.argv[1:]
    run_type = 0
    if len(args) != 0:
        if "-h" in args or "--help" in args:
            help_menu = [
                "{} Help\n".format(sys.argv[0]),
                "-h, --help\n",
                "   Retrieve help for usage of {}\n".format(sys.argv[0]),
                "   Example: python {} --help\n\n".format(sys.argv[0]),

                "-f, --flash\n",
                "   Run the script in Live mode and flash the Fiberpunk Node\n",
                "   Example: python {} --flash\n".format(sys.argv[0])
                ]
            print("".join(help_menu))
            quit()

        elif "-f" in args or "--flash" in args:
            run_type = 1

        else:
            print("Invalid argument.\nSee `python {} -h` for details.".format(sys.argv[0]))
            quit()

    required_info = {"Port":None, "Firmware":None, "Webpage":None}
    tkinter_compat()

    required_info["Port"] = node_locating(silent_stat=False)
    required_info["Firmware"] = os.path.basename(firmware_selection())
    required_info["Webpage"] = "./webpage"#webpage_selection()

    print("\nPreparing to Flash Node Firmware...\nDO NOT UNPLUG DEVICE UNTIL COMPLETE")
    sleep(1)
    
    command = ["--chip", "esp32", "--baud", "921600", "--port", required_info["Port"], "--before", "default_reset", "--after", "hard_reset", 
    "write_flash", "-z", "--flash_mode", "dio", "--flash_freq", "80m", "--fresh_size", "detect", "0xe000", "boot_app0.bin", 
    "0x1000", "bootloader_qio_80m.bin", "0x8000", "default.bin", "0x10000", required_info["Firmware"]]

    print('Using command %s' % ' '.join(command))
    try:
        if run_type == 1:
            esptool.main(command)
        else:
            print("Updater running in test mode - Flash Aborted")
    except Exception as e:
        print("Flashing Error Occurred:\n↳  {}".format(e))
        quit()
    print("Flashing of Firmware Complete\n")
    print("Generating Spiff BIN file...")
    try:
        os.system('python spiffsgen.py 1507328 {} spifs.bin'.format(required_info["Webpage"]))
    except:
        print("Unable to generate spifs.bin\nHalting Program")
        quit()
    
    print("Spiff BIN file Successfully generated!\n")
    print("Flashing Webpage BIN file...")
    command = ["--chip", "esp32", "--baud", "921600", "--port", required_info["Port"], "--before", "default_reset", "--after", "hard_reset", "write_flash", "-z",
    "--flash_mode", "dio", "--flash_freq", "80m", "--fresh_size", "detect", "2686976", "spifs.bin"]
    try:
        if run_type == 1:
            esptool.main(command)
        else:
            print("Updater running in test mode - Flash Aborted")
    except Exception as e:
        print("Flashing Error Occurred:\n↳  {}".format(e))
        quit()
    
    if run_type == 1:
        print("\n\nNODE UPDATE COMPLETE!!!")
    else:
        print("\n\nNODE TEST COMPLETE!!!")
