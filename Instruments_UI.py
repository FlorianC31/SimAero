# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Instruments.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1656, 917)
        self.anenometre = QtWidgets.QFrame(Form)
        self.anenometre.setGeometry(QtCore.QRect(90, 80, 320, 371))
        self.anenometre.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.anenometre.setFrameShadow(QtWidgets.QFrame.Raised)
        self.anenometre.setObjectName("anenometre")
        self.anemometre_cadran = QtWidgets.QLabel(self.anenometre)
        self.anemometre_cadran.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.anemometre_cadran.setText("")
        self.anemometre_cadran.setPixmap(QtGui.QPixmap("../Ressources/anémomètre ai.png"))
        self.anemometre_cadran.setObjectName("anemometre_cadran")
        self.anemometre_aiguille = QtWidgets.QLabel(self.anenometre)
        self.anemometre_aiguille.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.anemometre_aiguille.setText("")
        self.anemometre_aiguille.setPixmap(QtGui.QPixmap("../Ressources/aiguille.png"))
        self.anemometre_aiguille.setAlignment(QtCore.Qt.AlignCenter)
        self.anemometre_aiguille.setObjectName("anemometre_aiguille")
        self.anemometre_label = QtWidgets.QLabel(self.anenometre)
        self.anemometre_label.setGeometry(QtCore.QRect(0, 320, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.anemometre_label.setFont(font)
        self.anemometre_label.setAlignment(QtCore.Qt.AlignCenter)
        self.anemometre_label.setObjectName("anemometre_label")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(170, 480, 360, 22))
        self.horizontalSlider.setMinimum(-180)
        self.horizontalSlider.setMaximum(180)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.altimetre = QtWidgets.QFrame(Form)
        self.altimetre.setGeometry(QtCore.QRect(460, 80, 320, 371))
        self.altimetre.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.altimetre.setFrameShadow(QtWidgets.QFrame.Raised)
        self.altimetre.setObjectName("altimetre")
        self.altimetre_cadran = QtWidgets.QLabel(self.altimetre)
        self.altimetre_cadran.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.altimetre_cadran.setText("")
        self.altimetre_cadran.setPixmap(QtGui.QPixmap("../Ressources/altimetre.png"))
        self.altimetre_cadran.setObjectName("altimetre_cadran")
        self.altimetre_aiguille1 = QtWidgets.QLabel(self.altimetre)
        self.altimetre_aiguille1.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.altimetre_aiguille1.setText("")
        self.altimetre_aiguille1.setPixmap(QtGui.QPixmap("../Ressources/aiguille.png"))
        self.altimetre_aiguille1.setAlignment(QtCore.Qt.AlignCenter)
        self.altimetre_aiguille1.setObjectName("altimetre_aiguille1")
        self.altimetre_label = QtWidgets.QLabel(self.altimetre)
        self.altimetre_label.setGeometry(QtCore.QRect(0, 320, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.altimetre_label.setFont(font)
        self.altimetre_label.setAlignment(QtCore.Qt.AlignCenter)
        self.altimetre_label.setObjectName("altimetre_label")
        self.altimetre_aiguille2 = QtWidgets.QLabel(self.altimetre)
        self.altimetre_aiguille2.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.altimetre_aiguille2.setText("")
        self.altimetre_aiguille2.setPixmap(QtGui.QPixmap("../Ressources/aiguille_small.png"))
        self.altimetre_aiguille2.setAlignment(QtCore.Qt.AlignCenter)
        self.altimetre_aiguille2.setObjectName("altimetre_aiguille2")
        self.altimetre_cadran.raise_()
        self.altimetre_label.raise_()
        self.altimetre_aiguille2.raise_()
        self.altimetre_aiguille1.raise_()
        self.variometre = QtWidgets.QFrame(Form)
        self.variometre.setGeometry(QtCore.QRect(820, 80, 320, 371))
        self.variometre.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.variometre.setFrameShadow(QtWidgets.QFrame.Raised)
        self.variometre.setObjectName("variometre")
        self.variometre_cadran = QtWidgets.QLabel(self.variometre)
        self.variometre_cadran.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.variometre_cadran.setText("")
        self.variometre_cadran.setPixmap(QtGui.QPixmap("../Ressources/variometre.png"))
        self.variometre_cadran.setObjectName("variometre_cadran")
        self.variometre_aiguille = QtWidgets.QLabel(self.variometre)
        self.variometre_aiguille.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.variometre_aiguille.setText("")
        self.variometre_aiguille.setPixmap(QtGui.QPixmap("../Ressources/aiguille.png"))
        self.variometre_aiguille.setAlignment(QtCore.Qt.AlignCenter)
        self.variometre_aiguille.setObjectName("variometre_aiguille")
        self.variometre_label = QtWidgets.QLabel(self.variometre)
        self.variometre_label.setGeometry(QtCore.QRect(0, 320, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.variometre_label.setFont(font)
        self.variometre_label.setAlignment(QtCore.Qt.AlignCenter)
        self.variometre_label.setObjectName("variometre_label")
        self.horizon = QtWidgets.QFrame(Form)
        self.horizon.setGeometry(QtCore.QRect(1180, 80, 320, 371))
        self.horizon.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.horizon.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizon.setObjectName("horizon")
        self.horizon_cadran = QtWidgets.QLabel(self.horizon)
        self.horizon_cadran.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.horizon_cadran.setText("")
        self.horizon_cadran.setPixmap(QtGui.QPixmap("../Ressources/horizon_cadran.png"))
        self.horizon_cadran.setObjectName("horizon_cadran")
        self.horizon_angle = QtWidgets.QLabel(self.horizon)
        self.horizon_angle.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.horizon_angle.setText("")
        self.horizon_angle.setPixmap(QtGui.QPixmap("../Ressources/horizon_angle.png"))
        self.horizon_angle.setAlignment(QtCore.Qt.AlignCenter)
        self.horizon_angle.setObjectName("horizon_angle")
        self.horizon_label = QtWidgets.QLabel(self.horizon)
        self.horizon_label.setGeometry(QtCore.QRect(0, 320, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.horizon_label.setFont(font)
        self.horizon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizon_label.setObjectName("horizon_label")
        self.horizon_fond_container = QtWidgets.QFrame(self.horizon)
        self.horizon_fond_container.setGeometry(QtCore.QRect(50, 50, 220, 220))
        self.horizon_fond_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.horizon_fond_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizon_fond_container.setObjectName("horizon_fond_container")
        self.horizon_fond = QtWidgets.QLabel(self.horizon_fond_container)
        self.horizon_fond.setGeometry(QtCore.QRect(-210, -210, 640, 640))
        self.horizon_fond.setText("")
        self.horizon_fond.setPixmap(QtGui.QPixmap("../Ressources/horizon_fond.png"))
        self.horizon_fond.setAlignment(QtCore.Qt.AlignCenter)
        self.horizon_fond.setObjectName("horizon_fond")
        self.horizon_label.raise_()
        self.horizon_fond_container.raise_()
        self.horizon_angle.raise_()
        self.horizon_cadran.raise_()
        self.verticalSlider = QtWidgets.QSlider(Form)
        self.verticalSlider.setGeometry(QtCore.QRect(170, 530, 22, 160))
        self.verticalSlider.setMinimum(-90)
        self.verticalSlider.setMaximum(90)
        self.verticalSlider.setProperty("value", 0)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.FPS = QtWidgets.QLabel(Form)
        self.FPS.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.FPS.setObjectName("FPS")
        self.iterID = QtWidgets.QLabel(Form)
        self.iterID.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.iterID.setObjectName("iterID")
        self.NextButton = QtWidgets.QPushButton(Form)
        self.NextButton.setGeometry(QtCore.QRect(50, 550, 75, 23))
        self.NextButton.setObjectName("NextButton")
        self.View2DContainer = QtWidgets.QFrame(Form)
        self.View2DContainer.setGeometry(QtCore.QRect(600, 500, 967, 400))
        self.View2DContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.View2DContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.View2DContainer.setObjectName("View2DContainer")
        self.View2DPicture = QtWidgets.QLabel(self.View2DContainer)
        self.View2DPicture.setGeometry(QtCore.QRect(0, 0, 967, 400))
        self.View2DPicture.setText("")
        self.View2DPicture.setPixmap(QtGui.QPixmap("../Ressources/Cessna2.png"))
        self.View2DPicture.setObjectName("View2DPicture")
        self.FlightParams = QtWidgets.QLabel(Form)
        self.FlightParams.setGeometry(QtCore.QRect(270, 520, 261, 311))
        self.FlightParams.setText("")
        self.FlightParams.setObjectName("FlightParams")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.anemometre_label.setText(_translate("Form", "Speed : 86 Kt"))
        self.altimetre_label.setText(_translate("Form", "Speed : 86 Kt"))
        self.variometre_label.setText(_translate("Form", "Speed : 86 Kt"))
        self.horizon_label.setText(_translate("Form", "Speed : 86 Kt"))
        self.FPS.setText(_translate("Form", "FPS"))
        self.iterID.setText(_translate("Form", "TextLabel"))
        self.NextButton.setText(_translate("Form", "Next iter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
