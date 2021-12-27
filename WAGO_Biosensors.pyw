#!/usr/bin/env python3

wagoIP = "192.168.1.8"	# CHANGE THIS IF NEEDED! Find WAGO IP from WAGO Ethernet settings and use here.
valveActiveLow = True	# TRUE if WAGO unit sets coils LOW to enable. If unsure, leave alone (True)

virtual = False			# "Virtual" WAGO for debugging. Leave FALSE for using a real-world unit.



# UI sourced from outside files in addition to PyQt5 and Modbus for TCP WAGO communication
import sys, time, threading
from pymodbus.client.sync import ModbusTcpClient
from PyQt5 import QtCore, QtGui, QtWidgets


class WAGO_BiosensorsUI(QtWidgets.QMainWindow):
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


class Ui_MainWindow(object):
# PyQt5 UI create (autogenerated)
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(640, 480)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
		MainWindow.setSizePolicy(sizePolicy)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.pb7 = QtWidgets.QPushButton(self.centralwidget)
		self.pb7.setObjectName("pb7")
		self.gridLayout_3.addWidget(self.pb7, 7, 0, 1, 1)
		self.pb30 = QtWidgets.QPushButton(self.centralwidget)
		self.pb30.setObjectName("pb30")
		self.gridLayout_3.addWidget(self.pb30, 5, 3, 1, 1)
		self.pb13 = QtWidgets.QPushButton(self.centralwidget)
		self.pb13.setObjectName("pb13")
		self.gridLayout_3.addWidget(self.pb13, 4, 1, 1, 1)
		self.pb16 = QtWidgets.QPushButton(self.centralwidget)
		self.pb16.setObjectName("pb16")
		self.gridLayout_3.addWidget(self.pb16, 8, 1, 1, 1)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout_3.addItem(spacerItem, 1, 7, 1, 1)
		self.pb18 = QtWidgets.QPushButton(self.centralwidget)
		self.pb18.setObjectName("pb18")
		self.gridLayout_3.addWidget(self.pb18, 1, 2, 1, 1)
		self.pbConnect = QtWidgets.QPushButton(self.centralwidget)
		self.pbConnect.setObjectName("pbConnect")
		self.gridLayout_3.addWidget(self.pbConnect, 1, 6, 1, 1)
		self.pb6 = QtWidgets.QPushButton(self.centralwidget)
		self.pb6.setObjectName("pb6")
		self.gridLayout_3.addWidget(self.pb6, 5, 0, 1, 1)
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout_3.addItem(spacerItem1, 1, 5, 1, 1)
		self.pb11 = QtWidgets.QPushButton(self.centralwidget)
		self.pb11.setObjectName("pb11")
		self.gridLayout_3.addWidget(self.pb11, 2, 1, 1, 1)
		self.pb21 = QtWidgets.QPushButton(self.centralwidget)
		self.pb21.setObjectName("pb21")
		self.gridLayout_3.addWidget(self.pb21, 4, 2, 1, 1)
		self.pb10 = QtWidgets.QPushButton(self.centralwidget)
		self.pb10.setObjectName("pb10")
		self.gridLayout_3.addWidget(self.pb10, 1, 1, 1, 1)
		self.pb17 = QtWidgets.QPushButton(self.centralwidget)
		self.pb17.setObjectName("pb17")
		self.gridLayout_3.addWidget(self.pb17, 0, 2, 1, 1)
		self.pb9 = QtWidgets.QPushButton(self.centralwidget)
		self.pb9.setObjectName("pb9")
		self.gridLayout_3.addWidget(self.pb9, 0, 1, 1, 1)
		self.pb8 = QtWidgets.QPushButton(self.centralwidget)
		self.pb8.setObjectName("pb8")
		self.gridLayout_3.addWidget(self.pb8, 8, 0, 1, 1)
		self.pb31 = QtWidgets.QPushButton(self.centralwidget)
		self.pb31.setObjectName("pb31")
		self.gridLayout_3.addWidget(self.pb31, 7, 3, 1, 1)
		self.pb1 = QtWidgets.QPushButton(self.centralwidget)
		self.pb1.setObjectName("pb1")
		self.gridLayout_3.addWidget(self.pb1, 0, 0, 1, 1)
		self.pb12 = QtWidgets.QPushButton(self.centralwidget)
		self.pb12.setObjectName("pb12")
		self.gridLayout_3.addWidget(self.pb12, 3, 1, 1, 1)
		self.freqBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
		self.freqBox.setAlignment(QtCore.Qt.AlignCenter)
		self.freqBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
		self.freqBox.setDecimals(3)
		self.freqBox.setMaximum(1000000.0)
		self.freqBox.setObjectName("freqBox")
		self.gridLayout_3.addWidget(self.freqBox, 5, 6, 1, 1)
		self.pb5 = QtWidgets.QPushButton(self.centralwidget)
		self.pb5.setObjectName("pb5")
		self.gridLayout_3.addWidget(self.pb5, 4, 0, 1, 1)
		self.pb3 = QtWidgets.QPushButton(self.centralwidget)
		self.pb3.setObjectName("pb3")
		self.gridLayout_3.addWidget(self.pb3, 2, 0, 1, 1)
		self.pb32 = QtWidgets.QPushButton(self.centralwidget)
		self.pb32.setObjectName("pb32")
		self.gridLayout_3.addWidget(self.pb32, 8, 3, 1, 1)
		self.pb19 = QtWidgets.QPushButton(self.centralwidget)
		self.pb19.setObjectName("pb19")
		self.gridLayout_3.addWidget(self.pb19, 2, 2, 1, 1)
		self.pb25 = QtWidgets.QPushButton(self.centralwidget)
		self.pb25.setObjectName("pb25")
		self.gridLayout_3.addWidget(self.pb25, 0, 3, 1, 1)
		self.pb20 = QtWidgets.QPushButton(self.centralwidget)
		self.pb20.setObjectName("pb20")
		self.gridLayout_3.addWidget(self.pb20, 3, 2, 1, 1)
		self.pb24 = QtWidgets.QPushButton(self.centralwidget)
		self.pb24.setObjectName("pb24")
		self.gridLayout_3.addWidget(self.pb24, 8, 2, 1, 1)
		self.pb29 = QtWidgets.QPushButton(self.centralwidget)
		self.pb29.setObjectName("pb29")
		self.gridLayout_3.addWidget(self.pb29, 4, 3, 1, 1)
		self.pb26 = QtWidgets.QPushButton(self.centralwidget)
		self.pb26.setObjectName("pb26")
		self.gridLayout_3.addWidget(self.pb26, 1, 3, 1, 1)
		self.pb4 = QtWidgets.QPushButton(self.centralwidget)
		self.pb4.setObjectName("pb4")
		self.gridLayout_3.addWidget(self.pb4, 3, 0, 1, 1)
		self.pb15 = QtWidgets.QPushButton(self.centralwidget)
		self.pb15.setObjectName("pb15")
		self.gridLayout_3.addWidget(self.pb15, 7, 1, 1, 1)
		self.pb28 = QtWidgets.QPushButton(self.centralwidget)
		self.pb28.setObjectName("pb28")
		self.gridLayout_3.addWidget(self.pb28, 3, 3, 1, 1)
		self.pb14 = QtWidgets.QPushButton(self.centralwidget)
		self.pb14.setObjectName("pb14")
		self.gridLayout_3.addWidget(self.pb14, 5, 1, 1, 1)
		self.pbCloseAll = QtWidgets.QPushButton(self.centralwidget)
		self.pbCloseAll.setObjectName("pbCloseAll")
		self.gridLayout_3.addWidget(self.pbCloseAll, 2, 6, 1, 1)
		self.pb27 = QtWidgets.QPushButton(self.centralwidget)
		self.pb27.setObjectName("pb27")
		self.gridLayout_3.addWidget(self.pb27, 2, 3, 1, 1)
		self.pb22 = QtWidgets.QPushButton(self.centralwidget)
		self.pb22.setObjectName("pb22")
		self.gridLayout_3.addWidget(self.pb22, 5, 2, 1, 1)
		self.pb23 = QtWidgets.QPushButton(self.centralwidget)
		self.pb23.setObjectName("pb23")
		self.gridLayout_3.addWidget(self.pb23, 7, 2, 1, 1)
		self.pbStop1 = QtWidgets.QPushButton(self.centralwidget)
		self.pbStop1.setObjectName("pbStop1")
		self.gridLayout_3.addWidget(self.pbStop1, 4, 6, 1, 1)
		self.pb2 = QtWidgets.QPushButton(self.centralwidget)
		self.pb2.setObjectName("pb2")
		self.gridLayout_3.addWidget(self.pb2, 1, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
		self.label.setSizePolicy(sizePolicy)
		self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
		self.label.setObjectName("label")
		self.gridLayout_3.addWidget(self.label, 7, 5, 1, 3)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "WAGO Biosensors"))
		self.pb7.setText(_translate("MainWindow", "Valve 7"))
		self.pb30.setText(_translate("MainWindow", "Valve 30"))
		self.pb13.setText(_translate("MainWindow", "Valve 13"))
		self.pb16.setText(_translate("MainWindow", "Valve 16"))
		self.pb18.setText(_translate("MainWindow", "Valve 18"))
		self.pbConnect.setText(_translate("MainWindow", "Connect WAGO"))
		self.pb6.setText(_translate("MainWindow", "Valve 6"))
		self.pb11.setText(_translate("MainWindow", "Valve 11"))
		self.pb21.setText(_translate("MainWindow", "Valve 21"))
		self.pb10.setText(_translate("MainWindow", "Valve 10"))
		self.pb17.setText(_translate("MainWindow", "Valve 17"))
		self.pb9.setText(_translate("MainWindow", "Valve 9"))
		self.pb8.setText(_translate("MainWindow", "Valve 8"))
		self.pb31.setText(_translate("MainWindow", "Valve 31"))
		self.pb1.setText(_translate("MainWindow", "Valve 1"))
		self.pb12.setText(_translate("MainWindow", "Valve 12"))
		self.pb5.setText(_translate("MainWindow", "Valve 5"))
		self.pb3.setText(_translate("MainWindow", "Valve 3"))
		self.pb32.setText(_translate("MainWindow", "Valve 32"))
		self.pb19.setText(_translate("MainWindow", "Valve 19"))
		self.pb25.setText(_translate("MainWindow", "Valve 25"))
		self.pb20.setText(_translate("MainWindow", "Valve 20"))
		self.pb24.setText(_translate("MainWindow", "Valve 24"))
		self.pb29.setText(_translate("MainWindow", "Valve 29"))
		self.pb26.setText(_translate("MainWindow", "Valve 26"))
		self.pb4.setText(_translate("MainWindow", "Valve 4"))
		self.pb15.setText(_translate("MainWindow", "Valve 15"))
		self.pb28.setText(_translate("MainWindow", "Valve 28"))
		self.pb14.setText(_translate("MainWindow", "Valve 14"))
		self.pbCloseAll.setText(_translate("MainWindow", "Close All Valves"))
		self.pb27.setText(_translate("MainWindow", "Valve 27"))
		self.pb22.setText(_translate("MainWindow", "Valve 22"))
		self.pb23.setText(_translate("MainWindow", "Valve 23"))
		self.pbStop1.setText(_translate("MainWindow", "STOP Valve 1"))
		self.pb2.setText(_translate("MainWindow", "Valve 2"))
		self.label.setText(_translate("MainWindow", "Valve 1 Freq (toggles/minute)"))



def main():
# Create PyQt5 Window UI and run it
	qapp = QtWidgets.QApplication(sys.argv)
	form = WAGO_BiosensorsUI()
	form.show()
	sys.exit(qapp.exec_())

if __name__ == "__main__":
	main()
