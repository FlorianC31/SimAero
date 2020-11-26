# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Instruments.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtGui, QtWidgets, QtCore
from Instruments_UI import Ui_Form
import sys
from math import radians,cos,sin
from Painter import Painter


def ms2kt(speed):
    return speed*1.94384


def m2ft(distance):
    return distance*3.28084


def interpoleLinear(x1,x2,y1,y2):
    a=(y1-y2)/(x1-x2)
    b=y1-a*x1
    return a,b

def interpole(data,value):
    if value<data[0][0]:
        return 0
    else:
        for i in range(len(data)-1):
            if data[i+1][0]>=value:
                a,b=interpoleLinear(data[i][0],data[i+1][0],data[i][1],data[i+1][1])
                return a*value+b
        return data[len(data)-1][1]
                





class Instruments(Ui_Form):
    def __init__(self,Vol):
        super(Instruments, self).__init__()
        self.InstruWidget = QtWidgets.QWidget()   
        self.setupUi(self.InstruWidget)
        
        layout = QtWidgets.QVBoxLayout(self.View2DContainer)
        '''self.painter=Painter(Vol)
        self.painter.show()
        layout.addWidget(self.painter)'''
        
        
        

        
        self.InstruWidget.show()
        
        self.aiguille=QtGui.QPixmap("../Ressources/aiguille.png")
        self.aiguille2=QtGui.QPixmap("../Ressources/aiguille_small.png")
        self.HAngle=QtGui.QPixmap("../Ressources/horizon_angle.png")
        self.HFond=QtGui.QPixmap("../Ressources/horizon_fond.png")
        
        self.horizontalSlider.valueChanged.connect(self.valuechange)
        self.verticalSlider.valueChanged.connect(self.valuechange)
        self.Vol=Vol
        
        self.NextButton.clicked.connect(lambda:self.Vol.Iteration())
        
        
    

        
    def setSpeed(self,speed):
        
        speed=ms2kt(speed)
        
        data=[]
        data.append((25,0))
        data.append((40,31))
        data.append((50,50.5))
        data.append((60,73))
        data.append((70,94))
        data.append((80,117))
        data.append((90,139))
        data.append((100,164))
        data.append((110,185))
        data.append((120,205))
        data.append((130,221))
        data.append((140,236))
        data.append((150,252))
        data.append((160,267))
        data.append((170,278.5))
        data.append((180,291))
        data.append((190,303))
        data.append((200,318))


        angle=interpole(data,speed)
        
        transform=QtGui.QTransform()
        transform.rotate(angle)
        newPixMap=self.aiguille.transformed(transform)
        self.anemometre_aiguille.setPixmap(newPixMap)
        
        
        self.anemometre_label.setText(QtCore.QCoreApplication.translate("Form", str(round(speed,0)) + "Kt"))
        
    def setAltitude(self,altitude):
        altitude=m2ft(altitude)
        
        angle1=(altitude/1000*360)
        transform=QtGui.QTransform()        
        transform.rotate(angle1)
        newPixMap=self.aiguille.transformed(transform)
        self.altimetre_aiguille1.setPixmap(newPixMap)
        
        angle2=(altitude/10000*360)
        transform2=QtGui.QTransform()
        transform2.rotate(angle2)
        newPixMap=self.aiguille2.transformed(transform2)
        self.altimetre_aiguille2.setPixmap(newPixMap)
        
        self.altimetre_label.setText(QtCore.QCoreApplication.translate("Form", str(round(altitude,0)) + " Ft"))
        
        
    def setVario(self,vario):
        vario=m2ft(vario)*60
        
        angle=270+170*min(max(vario/2000,-1),1)
        
        transform=QtGui.QTransform()
        transform.rotate(angle)
        newPixMap=self.aiguille.transformed(transform)
        self.variometre_aiguille.setPixmap(newPixMap)
        
        
        self.variometre_label.setText(QtCore.QCoreApplication.translate("Form", str(round(vario,0)) + " Ft/min "))
        
        
    def setHorizon(self,assiette,inclinaison):
        transform=QtGui.QTransform()
        transform.rotate(-inclinaison)
        newPixMap1=self.HAngle.transformed(transform)
        newPixMap2=self.HFond.transformed(transform)        
        self.horizon_angle.setPixmap(newPixMap1)     
        self.horizon_fond.setPixmap(newPixMap2)
        
        scale=1.5
        init=(self.horizon_fond_container.size().width()-self.horizon_fond.size().width())/2
        dx=assiette*sin(radians(inclinaison))*scale
        dy=assiette*cos(radians(inclinaison))*scale
        
        
        
        self.horizon_fond.move(init+dx,init+dy)
        
        self.horizon_label.setText(QtCore.QCoreApplication.translate("Form", "Inclinaison: " + str(round(inclinaison,0)) + " ° / Assiette: "+ str(round(assiette,0)) + " ° "))
        
        
        
        
    def valuechange(self):
        inclinaison = self.horizontalSlider.value()
        assiette = self.verticalSlider.value()        
        self.setHorizon(assiette,inclinaison)
        
        
    def setFPS(self,fps,iterID):
        self.FPS.setText(QtCore.QCoreApplication.translate("Form", str(round(fps,0))))
        self.iterID.setText(QtCore.QCoreApplication.translate("Form", str(iterID)))



    def showFlightParams(self,Vol):
        params='Fx =' + str(round(Vol.Avion.GlobalTensor.Force[0],1))+'N \n'
        params+='Fz =' + str(round(Vol.Avion.GlobalTensor.Force[2],1))+'N \n'
        params+='My =' + str(round(Vol.Avion.GlobalTensor.Moment[1],1))+'N.m \n'
        params+='Alpha =' + str(round(Vol.Avion.Incidence['XZ'],3))+'° \n'
        params+='V =' + str(round(Vol.Avion.Vitesse['Aero'],1))+'m/s \n'
        
        
        self.FlightParams.setText(QtCore.QCoreApplication.translate("Form", params))


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    Instruments=Instruments('')
    Instruments.setSpeed(80)
    sys.exit(app.exec_())
