# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_wagoUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
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