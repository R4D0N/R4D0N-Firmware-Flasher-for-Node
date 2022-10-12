# Node Firmware Flasher For Mac
This tool allows Mac users to flash their Fiberpunk Nodes with the newest firmware

**Disclaimer:** This project is not associated with the Fiberpunk Team, and all Trademarks for the Node and related products belong to them.

## Installation Instructions
1. Download the latest release and extract the archive into the folder containing the bin files from Fiberpunk. 
2. Open a CLI in the firmware directory and install the required dependencies Ex. `pip3 install -r requirements.txt`

## Usage Instructions
### For Help
You can use the `-h` or `--help` flag 

Ex. `python3 node_updater.py -h`

### For Compatibility Testing
You can run the updater in test mode Ex. `python3 node_updater.py`

### To Install Firmware
1. Run the updater in live mode using the `-f` or `--flash` flag 
   
    Ex. `python3 node-updater.py -f`


2. Follow the instructions listed on the prompt

## [node_spec_gen.py](node-spec-gen.py)
This file ***will not*** modify the Node in any way. This script is designed to collect information about the host computer's ability to run the flashing software.


## [node_updater.py](node_updater.py)
This file is currently untested in a live environment and could do damage to your Node. Use at your own risk.

---


<sub>**By using this software, you accept the risks and waive all rights for lawsuits.**</sub>
