#!/usr/bin/env python3

wagoIP = "192.168.1.8"	# CHANGE THIS IF NEEDED! Find WAGO IP from WAGO Ethernet settings and use here.
valveActiveLow = True	# TRUE if WAGO unit sets coils LOW to enable. If unsure, leave alone (True)

virtual = False			# "Virtual" WAGO for debugging. Leave FALSE for using a real-world unit.



# UI sourced from outside files in addition to PyQt5 and Modbus for TCP WAGO communication
import sys, time, threading, PyQt5, PyQt5.QtWidgets
from pymodbus.client.sync import ModbusTcpClient
from _wagoUI import Ui_MainWindow


class WAGO_BiosensorsUI(PyQt5.QtWidgets.QMainWindow):
# Class for main window and program

	def __init__(self):
		# Initialize WAGO PLC via Modbus
		self.wago = WagoPLC(wagoIP, 32, valveActiveLow, virtual)	# assume 32 valves since the UI has 32

		# Setup QT UI from external UI file and make small adjustments
		super(WAGO_BiosensorsUI, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.statusbar.showMessage(f"No WAGO Connected! ({self.wago.ip})")
		self.setFixedSize(self.size())

		# Tracker for if valve 1 clock is enabled. On/off denoted by odd/even
		# This way if multiple clocks should appear the old one should auto terminate
		self.valve1EnabledCount = 0 	

		# Track buttons in UI for clicking
		self.valveButtons = [self.ui.pb1, self.ui.pb2, self.ui.pb3, self.ui.pb4, self.ui.pb5, self.ui.pb6, self.ui.pb7, self.ui.pb8,
				self.ui.pb9, self.ui.pb10, self.ui.pb11, self.ui.pb12, self.ui.pb13, self.ui.pb14, self.ui.pb15, self.ui.pb16,
				self.ui.pb17, self.ui.pb18, self.ui.pb19, self.ui.pb20, self.ui.pb21, self.ui.pb22, self.ui.pb23, self.ui.pb24,
				self.ui.pb25, self.ui.pb26, self.ui.pb27, self.ui.pb28, self.ui.pb29, self.ui.pb30, self.ui.pb31, self.ui.pb32]

		# Add click action to each valve button and also extra buttons
		for index, button in enumerate(self.valveButtons):
			button.clicked.connect(lambda ch, i=index: self.valveButtonClick(i))
		self.ui.pbCloseAll.clicked.connect(self.closeAll)
		self.ui.pbConnect.clicked.connect(self.connectWAGO)
		self.ui.pbStop1.clicked.connect(self.stopValve1)
		
		# Add action to freq change box and set initial frequency
		self.ui.freqBox.valueChanged.connect(self.setValve1Freq)
		self.ui.freqBox.setValue(5)


		# Try to automatically connect WAGO. 
		self.connectWAGO()

		
		
	def connectWAGO(self):
		# Attempt WAGO connection
		self.wago.connect()			
		
		if self.wago.modbus != None:
			# If successful, say so and disable further connection attempts.
			self.ui.statusbar.showMessage(f"WAGO Connected! ({'VIRT ' if self.wago.virtual else ''}{self.wago.ip})")
			self.ui.pbConnect.setEnabled(False)

			# Also close valves on unit.
			self.wago.resetValves()	
		else:
			# Issue with connecting
			self.ui.statusbar.showMessage(f"Can't connect to WAGO ({self.wago.ip})! Check IP and connections, then try again.")


	def valveButtonClick(self, buttonIndex):
		# One of the 32 valve buttons is clicked
		print(f"Click button {buttonIndex}")

		if self.wago.modbus == None:
			# WAGO not connected, so don't do anything
			return	

		if buttonIndex == 0:
			# Special case for valve 1 - enable clock
			if (self.valve1EnabledCount % 2) == 0:
				# Even denotes off - make a new thread daemon with the clock function
				# Also increment pre-thread-start to avoid quick thread exit
				new_thread = threading.Thread(target = self.FreqThread,
									args = (self.valve1Freq, (self.valve1EnabledCount + 1), ), daemon = True)
				self.valve1EnabledCount += 1
				new_thread.start()
			else:
				# Stop thread (increment counter) then set valve 0 closed
				self.valve1EnabledCount += 1
				self.wago.setValve(0, self.wago.VALVE_CLOSED)
				
		else:
			# For valves 2-32 just toggle the valve
			self.wago.toggleValve(buttonIndex)

		# Show enabled valves by toggling bold text - only enabled if 1) thread count matches or 2) valve is open
		isBold = ( (self.valve1EnabledCount%2) == 1) if (buttonIndex == 0) else self.wago.isValveOpen(buttonIndex)
		font = self.valveButtons[buttonIndex].property("font")	# set font BOLD if valve open
		font.setBold(isBold)
		self.valveButtons[buttonIndex].setFont(font)


	def closeAll(self):
		# Close all valves (button): go through valves, if enabled, disable by "clicking" button
		if (self.valve1EnabledCount%2) == 1:
			self.valveButtonClick(0)

		for valve in range(1,self.wago.numcoils):
			if self.wago.isValveOpen(valve):
				self.valveButtonClick(valve)


	def FreqThread(self, freq, this_id):
		# Clock function for valve 1 auto toggle, runs in background
		if freq == 0:
			# User can treat valve 0 as normal by setting freq to 0
			self.wago.toggleValve(0)
			return

		stime = time.time()
		while True:
			# Loop indefinitely - first check if thread should even run before trying to toggle
			if this_id != self.valve1EnabledCount:
				print(f"Valve 1 thread ending ({this_id}, {self.valve1EnabledCount})")
				return

			# Otherwise check if time has passed toggle time and update if necessary then toggle
			now = time.time()
			if now > (stime + (60/freq)):
				stime += (60/freq)
				self.wago.toggleValve(0)


	def setValve1Freq(self):
		# Change frequency of valve 1 after first closing it
		if (self.valve1EnabledCount%2) == 1:
			self.valveButtonClick(0)
		self.valve1Freq = self.ui.freqBox.value()
		print(f"Set valve 1 freq to {self.valve1Freq}/min")


	def stopValve1(self):
		# Emergency stop button to quickly shut valve 1
		if (self.valve1EnabledCount%2) == 1:
			self.valveButtonClick(0)


class WagoPLC:
# Wago Modbus client object

	def __init__(self, ip, coils, actLow, virtual):
		self.ip = ip
		self.modbus = None
		self.virtual = virtual

		self.coils = [actLow]*coils
		self.numcoils = coils

		self.VALVE_OPEN = not actLow
		self.VALVE_CLOSED = actLow


	def connect(self):
		client = ModbusTcpClient(self.ip)

		if not self.virtual:
			connected = client.connect()
		else:
			connected = True

		if (not connected):
			print(f"Could not connect to WAGO at IP {self.ip}! Double-check IP address and connections.")
			return

		self.modbus = client


	def resetValves(self):
		for i in range(self.numcoils):
			self.setValve(i, self.VALVE_CLOSED)


	def setValve(self, coil, value):
		if self.modbus == None:
			print("WAGO not connected!")
			return

		if not self.virtual:
			self.modbus.write_coil(coil, value)
		else:
			print(f"VIRT coil set {coil} to {'open' if value == self.VALVE_OPEN else 'closed'}")
		self.coils[coil] = value


	def isValveOpen(self, coil):
		return self.coils[coil] == self.VALVE_OPEN


	def toggleValve(self, coil):
		self.setValve(coil, not self.coils[coil])


def main():
# Create PyQt5 Window UI and run it
	qapp = PyQt5.QtWidgets.QApplication(sys.argv)
	form = WAGO_BiosensorsUI()
	form.show()
	sys.exit(qapp.exec_())

if __name__ == "__main__":
	main()
