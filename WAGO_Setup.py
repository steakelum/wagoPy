#!/usr/bin/env python3

import subprocess, sys

print("Installing required libraries:\n")
subprocess.check_call([sys.executable, "-m", "pip", "install", "pyqt5"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "pymodbus"])
input("\nSetup complete. You may now close this window.\n")
