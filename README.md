# R4D0N Firmware Flasher For Node
[![CodeQL](https://github.com/R4D0N/R4D0N-Firmware-Flasher-for-Node/workflows/CodeQL/badge.svg)](https://github.com/R4D0N/R4D0N-Firmware-Flasher-for-Node/actions/workflows/codeql.yml)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/R4D0N/R4D0N-Firmware-Flasher-for-Node)
![GitHub issues](https://img.shields.io/github/issues-raw/R4D0N/R4D0N-Firmware-Flasher-for-Node)
![python version](https://img.shields.io/badge/python-%20%3E%3D3.7-blue?style=flat&logo=python)
![GitHub last commit](https://img.shields.io/github/last-commit/R4D0N/R4D0N-Firmware-Flasher-For-Node)

This tool allows Non-Windows users to flash their Fiberpunk Nodes with the newest firmware.
This tool works on Windows as well, but the Fiberpunk Devs have a released a binary that does the same job with a GUI.

**Disclaimer:** This project is not associated with the Fiberpunk Team, and all Trademarks for the Node and related products belong to them.

## Installation Instructions
1. Download the latest release and extract the archive into the folder containing the bin files from Fiberpunk. 
2. Open a CLI in the firmware directory and install the required dependencies Ex. `pip3 install -r requirements.txt`

## Usage Instructions
### For Help
You can use the `-h` or `--help` flag 

Ex. `python3 node_updater.py -h`

### Semi-Graphical Interface
`python3 updater_gui.py`

### For Compatibility Testing
You can run the updater in test mode Ex. `python3 node_updater.py`

### To Install Firmware
1. Run the updater in live mode using the `-f` or `--flash` flag 
   
    Ex. `python3 node-updater.py -f`


2. Follow the instructions listed on the prompt

---


<sub>**By using this software, you accept the risks and waive all rights for lawsuits.**</sub>
