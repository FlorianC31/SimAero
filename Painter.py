# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 07:31:33 2020

@author: Florian
"""



from PyQt5 import QtGui, QtWidgets, QtCore
from math import atan2, cos, sin, radians

class Painter(QtWidgets.QWidget):
    def __init__(self,Vol):
        super().__init__()
        self.Vol=Vol

    def paintEvent(self, event):
        self.painter = QtGui.QPainter(self)
        self.painter.setPen(QtCore.Qt.red)

        self.painter.setPen(QtGui.QPen(QtCore.Qt.yellow, 2, QtCore.Qt.DashLine))
        self.painter.drawLine(67, 202, 811+67, 202)
        
        colorList=[QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.green, QtCore.Qt.yellow, QtCore.Qt.magenta]

        '''
        for Tensor in self.Vol.Avion.ViewTensor:
            color=colorList[self.Vol.Avion.ViewTensor.index(Tensor)]
            self.DrawTensor(Tensor,color)'''
        #print("ViewTensor")
        #print(self.Vol.Avion.ViewTensor)
        #print('')
        #if len(self.Vol.Avion.ViewTensor)>0:
        #    self.DrawTensor(self.Vol.Avion.ViewTensor[4])
            #print(Tensor.Position[0],Tensor.Position[2])
        
        
    def DrawTensor(self,Tensor,color):
        scale=0.01
        
        x1,y1=self.transform(Tensor.Position[0],Tensor.Position[2])
        x2=x1+scale*Tensor.Force[0]
        y2=y1-scale*Tensor.Force[2]
        
        self.DrawArrow(x1, y1, x2, y2,color)
        
        
    def transform(self,x1,y1):
        print(x1,y1)
        scale=811/8.28   # 889pixels <=> 8.28m
        # Position of origin point
        xo=67
        yo=202
        x2=xo+x1*scale
        y2=yo-y1*scale
        print(x2,y2)
        return x2,y2
        
        
    def DrawArrow(self,x1,y1,x2,y2,color):
        alpha=radians(20)   # Head Arrow Angle
        l=15                # Head Arrow Length
        
        self.painter.setPen(QtGui.QPen(color, 4, QtCore.Qt.SolidLine))
        self.painter.drawLine(x1, y1, x2, y2)
        teta=atan2(y2-y1,x2-x1)
        
        x3=x2-l*cos(teta-alpha)
        y3=y2-l*sin(teta-alpha)
        self.painter.drawLine(x2, y2, x3, y3)
        
        x4=x2-l*cos(teta+alpha)
        y4=y2-l*sin(teta+alpha)
        self.painter.drawLine(x2, y2, x4, y4)
        
        
    def trigger_refresh(self):
        self.update()