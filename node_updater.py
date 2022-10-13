from hashlib import md5
from sys import version_info, argv
from os import path, listdir
from platform import platform
from time import sleep
from spiffsgen import main as spiffmain

#Imported for dependancy checking
from pkg_resources import get_distribution, DistributionNotFound

#Compatibility Checks
def version_check():
    if version_info.major != 3:
        print("You must install python 3.x to run this script.")
        print('If you have installed python 3.x use\n\npython3 "%s"' % path.basename(__file__))
        print("\nHalting Program")
        quit()

def platform_check(safety=True):
    if platform().startswith("darwin") is not True:
        print("This script is not compatible with the current OS installed.")
        if safety == True:
            print("Halting Program.")
            quit()
        else:
            print("Platform Check Warning, Program will continue.\n")

def tkinter_check():
    if version_info.minor < 9:
        print("Warning: You are using Python {}.{}.{} which can be unpredictable when selecting files.".format(version_info.major, version_info.minor, version_info.micro))
        print("It is better to use Python 3.9.x for stability reasons.")
        choice = input("Do you wish to proceed at your own risk? (y/n) ")
        if choice.lower() == "n":
            print("Halting Program")
            quit()
        elif choice.lower() == "y":
            print("")
            return
        else:
            print("Invalid Selection...")
            tkinter_check()
            quit()

#Arg Handler
def arg_handler(program, args):
    run_type = 0
    if len(args) != 0:
        if "-h" in args or "--help" in args:
            help_menu = [
                "{} Help\n".format(argv[0]),
                "-h, --help\n",
                "   Retrieve help for usage of {}\n".format(program),
                "   Example: python {} --help\n\n".format(program),

                "-f, --flash\n",
                "   Run the script in Live mode and flash the Fiberpunk Node\n",
                "   Example: python {} --flash\n".format(program)
                ]
            print("".join(help_menu))
            quit()

        elif "-f" in args or "--flash" in args:
            run_type = 1

        else:
            print("Invalid argument.\nSee `python {} -h` for details.".format(program))
            quit()
    return run_type

#Operating Functions
def node_locating(verbose=True):
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
        if verbose is True:
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
    dialog = askopenfilename(title="Select Node Firmware to Flash", initialdir=path.dirname(path.abspath(__file__)),defaultextension='.bin', filetypes=[("BIN Files", '*.bin')])
    if not dialog:
        print("No Firmware Selected.\nHalting Program")
        quit()
    else:
        f = open(dialog, "rb").read()
        m = md5(f)
        firmware_hash = m.hexdigest()

        approved_hashes = []
        ah = open("firmware_checksums", "r").readlines()
        for hash in ah:
            approved_hashes.append(hash.strip().split("#")[0])

        if firmware_hash in approved_hashes:
            return dialog
        else:
            print("{} is not a valid firmware file.\nHalting Program".format(path.basename(dialog)))
            quit()

def webpage_selection(): #Unused (Might use in later versions)
    dialog = askdirectory(title="Select Node Webpage Folder")
    if not dialog:
        print("No Webpage Folder Selected.\nHalting Program")
        quit()
    else:
        if "index.htm" not in listdir(dialog):
            print("No index.htm located in {}\nHalting Program".format(dialog))
            quit()
        else:
            return dialog


def main():
    run_type = arg_handler(argv[0], argv[1:]) #return 0 for testing, 1 for live (To Flash Firmware)

    required_info = {"Port":None, "Firmware":None, "Webpage":None}

    required_info["Port"] = node_locating(switchboard["node_locating"])
    required_info["Firmware"] = path.basename(firmware_selection())
    required_info["Webpage"] = "webpage"

    print("\nPreparing to Flash Node\nDO NOT UNPLUG DEVICE UNTIL COMPLETE")
    sleep(2) #Sleeping so user can read warning
    
    # SPIFF GENERATION
    print("Generating Spiff BIN file (Step 1/3)")
    try:
        spiffmain(['1507328', required_info["Webpage"], 'spifs.bin'])
    except Exception as e:
        print("Unable to generate spifs.bin due to:\n{}\nHalting Program".format(e))
        quit()   
    print("Spiff BIN file Successfully generated!\n")

    # MAIN FIRMWARE FLASHING
    print("Flashing Node Main Firmware (Step 2/3)")
    command = ["--chip", "esp32", "--baud", "921600", "--port", required_info["Port"], "--before", "default_reset", "--after", "hard_reset", 
    "write_flash", "-z", "--flash_mode", "dio", "--flash_freq", "80m", "--fresh_size", "detect", "0xe000", "boot_app0.bin", 
    "0x1000", "bootloader_qio_80m.bin", "0x8000", "default.bin", "0x10000", required_info["Firmware"]]

    if switchboard["list_flash_info"] is True:
        print('Using command %s' % ' '.join(command))
    try:
        if run_type == 1:
            esptool.main(command)
        else:
            print("Updater running in test mode - Flash Aborted")
    except Exception as e:
        print("Flashing Error Occurred:\n↳  {}".format(e))
        quit()
    print("Flashing of Main Firmware Complete\nDO NOT UNPLUG DEVICE")
    sleep(2) #Sleeping so user can read Success

    # WEBPAGE FLASHING
    print("Flashing Webpage BIN file (Stage 3/3)")
    command = ["--chip", "esp32", "--baud", "921600", "--port", required_info["Port"], "--before", "default_reset", "--after", "hard_reset", "write_flash", "-z",
    "--flash_mode", "dio", "--flash_freq", "80m", "--fresh_size", "detect", "2686976", "spifs.bin"]

    if switchboard["list_flash_info"] is True:
        print('Using command %s' % ' '.join(command))
    try:
        if run_type == 1:
            esptool.main(command)
        else:
            print("Updater running in test mode - Flash Aborted")
    except Exception as e:
        print("Flashing Error Occurred:\n↳  {}".format(e))
        quit()
    
    if run_type == 1:
        print("\n\nNODE UPDATE COMPLETE!!!\nIt is safe to unplug the Node")
    else:
        print("\n\nNODE TEST COMPLETE!!!\nIt is safe to unplug the Node")



if __name__ == "__main__":
    logo_payload = open("RFFN_Logo.txt", "r").read()
    print(logo_payload)

    #Default Switchboard {"platform_check":True, "node_locating":False, "list_installed":False, "list_flash_info":False}
    switchboard = {"platform_check":True, "node_locating":False, "list_installed":False, "list_flash_info":False}
    """
    "platform_check" Switchboard bool is if the program should quit on non-compatible OS
    "node_locating" Switchboard bool is if the program should verbosely list port info
    "list_installed" Switchboard bool is if the program should list installed dependancies
    "list_flash_info" Switchboard bool is if the program should print the flashing payload
    """

    #Version Check
    version_check()
    #Tkinter Check
    tkinter_check()
    #Platform Check <- Discontinued to allow for all OS
    #platform_check(switchboard["platform_check"])

    ##DEPENDANCY CHECKING
    reqs = []
    for line in open("requirements.txt", "r").readlines():
        reqs.append(line.strip())
    success_import = True
    for package in reqs:
        try:
            dist = get_distribution(package)
            if switchboard["list_installed"] is True:
                print('{} ({}) is installed'.format(dist.key, dist.version))
        except DistributionNotFound:
            print('{} is NOT installed'.format(package))
            success = False
    if success_import is False:
        print("Missing the above dependancies. Please install them before running this script")
        quit()
    print("")
    #Import Non-Core Libs post
    try:
        from tkinter.filedialog import askopenfilename, askdirectory
        from serial.tools import list_ports
        import esptool
    except Exception as e:
        print("Attempted Library Import\nProcess Failed:\n{}".format(e))
        quit()

    main()
