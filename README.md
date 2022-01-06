# wagoPy
Simple WAGO interface using PyQt5. Supports up to 32 valves that can be independently toggled. Valve 1 is automatically clocked when enabled by the user-defined frequency (valve toggles per minute). Additionally Valve 1 can be indefinitely toggled by setting the frequency to 0.
Quick access buttons exist to instantly stop and close Valve 1, or to automatically close all valves.

WAGO connection will attempt to be automatically made at predefined IP (192.168.1.8) within the script, which can be easily changed if WAGO is on different IP address, by editing the script file with a text editor. If wiring issues exist, a connection can be established after fixing by clicking "Connect WAGO".

## Usage
Python 3 is required, latest version is recommended (https://www.python.org/downloads/).
First install packages via running `WAGO_Setup.py` or `python -m pip install pyqt5 pymodbus`.
After, the main script  `WAGO_Biosensors.pyw` can be ran either in console or by double-clicking.
