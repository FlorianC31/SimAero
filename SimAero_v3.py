# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 20:46:19 2020

@author: Florian
"""


from Avion import Avion
from math import degrees, atan2
from matrix3D import Norm
from Instruments import Instruments
from PyQt5 import QtWidgets
import sys
from datetime import datetime
import time
import threading

sys.settrace

class Vol:
    def __init__(self, ParamInit, avion, CommandesVol, Instruments):

        # Param espace
        self.vitesse = ParamInit['vitesse']  # Repère Global
        self.vitRot = ParamInit['vitRot']
        self.position = ParamInit['position']
        self.angles = [ParamInit['inclinaison'], ParamInit['assiette'], ParamInit['course']]
        self.trajectoire = degrees(atan2(self.vitesse[2], self.vitesse[0]))  # Teta
        self.incidence = self.angles[1] - self.trajectoire  # Alpha = Beta - Teta
        self.course = 0

        # Param forces
        self.force = {}
        self.moment = 0
        self.Fmot = ParamInit['Fmot']
        self.gravity = 9.81  # m/s²
        self.Rho = 1.225  # kg/m³
        self.acceleration = [0, 0]
        self.accAngulaire = 0

        # Param Avion
        self.Avion = avion

        # Param Simu
        self.IterTime = 0.1  # s
        self.time = -self.IterTime

        self.Avion.ApplyCommandesVol(CommandesVol)


        self.Avion.GetInertia()

        self.Instruments = Instruments(self)

    def Iteration(self):

        # print('')
        # print(self.iterID)

        # Mechanical calculation
        self.Avion.GetGlobalTensor(self)
        self.Avion.GetAcceleration()

        # temp=self.vitRot[1]

        # Aircraft displacement
        for i in range(3):
            self.vitesse[i] += self.Avion.AccelerationLinear[i] * self.increment
            self.vitRot[i] += self.Avion.AccelerationRotation[i] * self.increment

            self.position[i] += self.vitesse[i] * self.increment
            self.angles[i] += degrees(self.vitRot[i] * self.increment)

        # print(self.iterID,temp,self.vitRot[1],self.Avion.AccelerationRotation[1],self.increment)

        # Update of instruments
        # print('Vitesse',self.vitesse,self.vitRot)
        # print('Position',self.position,self.angles)
        # print(iter,round(self.position[0],1),round(self.position[2],1),round(self.angles[1],2),round(Norm(self.vitesse),1))
        self.Instruments.setAltitude(self.position[2])
        self.Instruments.setVario(self.vitesse[2])
        self.Instruments.setSpeed(Norm(self.vitesse))
        self.Instruments.setHorizon(self.angles[1], self.angles[0])
        # self.Instruments.setIncidence(self.Avion.Incidence['XZ'])

        self.Instruments.showFlightParams(self)



    def PrintOutput(self):

        output = [self.iterID]
        for v in self.vitesse:
            output.append(v)

        for v in self.vitRot:
            output.append(v)

        for p in self.position:
            output.append(p)

        output.append(self.angles[1])
        output.append(self.Avion.GlobalTensor.Force[0])
        output.append(self.Avion.GlobalTensor.Force[2])
        output.append(self.Avion.GlobalTensor.Moment[1])
        output.append(Norm(self.vitesse) * 1.94384)
        output.append(self.position[2] * 3.28084)
        output.append(self.vitesse[2] * 3.28084 * 60)
        output.append(self.Avion.Incidence['XZ'])
        output.append(self.Avion.Vitesse['Avion'][0])
        output.append(self.Avion.Vitesse['Avion'][2])
        output.append(self.Avion.AccelerationRotation[1])
        output.append(self.vitRot[1])

        print(",".join(map(str, output)))
        # print(self.Avion.TotalMass,self.Avion.Inertia[0],self.Avion.Inertia[1],self.Avion.Inertia[2])




    def run(self,stop_event):
        self.running = True
        while self.running and not stop_event.isSet():
            # Calculation of iteration duration
            newTime = datetime.now()
            if self.lastTime != 0:
                timedelta = newTime - self.lastTime
                self.increment = timedelta.total_seconds() * self.acceleration
            self.Instruments.setFPS(1 / self.increment * self.acceleration, self.iterID)
            self.lastTime = newTime
            self.Iteration()
            self.iterID += 1
            maxFPS = 100
            #print(self.increment,1/maxFPS)
            if self.increment<1/maxFPS:
                time.sleep(1/maxFPS-self.increment)

    def start(self):

        self.increment = 0.1
        self.acceleration = 0.2
        self.lastTime = 0
        self.iterID = 0

        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.run, args=(self.stop_event,))
        self.c_thread.start()


if __name__ == '__main__':
    # Définition Cesna 172
    nouvelAvion = {}
    nouvelAvion['nom'] = "Cesna 172"
    nouvelAvion['masseVide'] = 779.0  # kg
    nouvelAvion['massMaxi'] = 1111.0  # kg
    nouvelAvion['puissanceMoteur'] = 160.0  # HP
    nouvelAvion['CoG'] = 2.0  # m
    nouvelAvion['FuseRadius'] = 0.6  # m

    nouvelAvion['ElmAero'] = {}

    nouvelAvion['ElmAero']['TrainAvant'] = {'Mass': 50, 'a': 1, 'b': 0.35, 'c': 0.3, 'x': 0.8, 'y': 0, 'z': -1.2,
                                            'Profil': 'Train', 'Plan': 'XYZ'}
    nouvelAvion['ElmAero']['TrainGauche'] = {'Mass': 50, 'a': 1, 'b': 0.35, 'c': 0.3, 'x': 2.7, 'y': -1, 'z': -1.2,
                                             'Profil': 'Train', 'Plan': 'XYZ'}
    nouvelAvion['ElmAero']['TrainDroite'] = {'Mass': 50, 'a': 1, 'b': 0.35, 'c': 0.3, 'x': 2.7, 'y': 1, 'z': -1.2,
                                             'Profil': 'Train', 'Plan': 'XYZ'}
    nouvelAvion['ElmAero']['Helice'] = {'Mass': 20, 'h': 0.2, 'r': 1, 'x': -0.1, 'y': 0, 'z': 0.15}
    nouvelAvion['ElmAero']['Moteur'] = {'Mass': 250, 'h': 1.2, 'r': 0.6, 'x': 0.6, 'y': 0, 'z': -0.2,
                                        'Profil': 'SecondStruct', 'Plan': 'XYZ'}
    nouvelAvion['ElmAero']['Cabine'] = {'Mass': 130, 'h': 2.8, 'r': 1, 'x': 2.6, 'y': 0, 'z': 0, 'Profil': 'PrimStruct',
                                        'Plan': 'XYZ'}
    nouvelAvion['ElmAero']['Queue'] = {'Mass': 109.751776412945, 'h': 4.28, 'r': 0.4, 'x': 6.14, 'y': 0, 'z': 0.2,
                                       'Profil': 'SecondStruct', 'Plan': 'XYZ'}
    nouvelAvion['ElmAero']['AileGaucheFlap'] = {'Mass': 22.4061696685606, 'a': 1.47272727272727, 'b': 2.5,
                                                'c': 0.119290909090909, 'x': 2.5, 'y': 1.25, 'z': 1,
                                                'Profil': 'NACA2412', 'Plan': 'XZ'}
    nouvelAvion['ElmAero']['AileGaucheAileron'] = {'Mass': 26.8874036022727, 'a': 1.47272727272727, 'b': 3,
                                                   'c': 0.119290909090909, 'x': 2.5, 'y': 4, 'z': 1,
                                                   'Profil': 'NACA2412', 'Plan': 'XZ'}
    nouvelAvion['ElmAero']['AileDroiteFlap'] = {'Mass': 22.4061696685606, 'a': 1.47272727272727, 'b': 2.5,
                                                'c': 0.119290909090909, 'x': 2.5, 'y': -1.25, 'z': 1,
                                                'Profil': 'NACA2412', 'Plan': 'XZ'}
    nouvelAvion['ElmAero']['AileDroiteAileron'] = {'Mass': 26.8874036022727, 'a': 1.47272727272727, 'b': 3,
                                                   'c': 0.119290909090909, 'x': 2.5, 'y': -4, 'z': 1,
                                                   'Profil': 'NACA2412', 'Plan': 'XZ'}
    nouvelAvion['ElmAero']['StabGauche'] = {'Mass': 7.23137696588584, 'a': 1, 'b': 1.75, 'c': 0.081, 'x': 7.78,
                                            'y': 0.875, 'z': 0, 'Profil': 'NACA0012', 'Plan': 'XZ'}
    nouvelAvion['ElmAero']['StabDroite'] = {'Mass': 7.23137696588584, 'a': 1, 'b': 1.75, 'c': 0.081, 'x': 7.78,
                                            'y': -0.875, 'z': 0, 'Profil': 'NACA0012', 'Plan': 'XZ'}
    nouvelAvion['ElmAero']['Gouverne'] = {'Mass': 6.19832311361643, 'a': 1, 'b': 0.081, 'c': 1.5, 'x': 7.78, 'y': 0,
                                          'z': 0.75, 'Profil': 'NACA0012', 'Plan': 'XY'}

    nouvelAvion['ElmAero']['FuelGauche'] = {'Mass': 86, 'a': 1.47272727272727, 'b': 5.5, 'c': 0.119290909090909,
                                            'x': 2.5, 'y': 2.75, 'z': 1}
    nouvelAvion['ElmAero']['FuelDroite'] = {'Mass': 86, 'a': 1.47272727272727, 'b': 5.5, 'c': 0.119290909090909,
                                            'x': 2.5, 'y': -2.75, 'z': 1}
    nouvelAvion['ElmAero']['Passager1'] = {'Mass': 80, 'h': 1, 'r': 0.3, 'x': 2.2, 'y': -0.4, 'z': 0}
    nouvelAvion['ElmAero']['Passager2'] = {'Mass': 80, 'h': 1, 'r': 0.3, 'x': 2.2, 'y': 0.4, 'z': 0}
    nouvelAvion['ElmAero']['Passager3'] = {'Mass': 0, 'h': 1, 'r': 0.3, 'x': 3.1, 'y': -0.4, 'z': 0}
    nouvelAvion['ElmAero']['Passager4'] = {'Mass': 0, 'h': 1, 'r': 0.3, 'x': 3.1, 'y': 4, 'z': 0}
    nouvelAvion['ElmAero']['Bagages'] = {'Mass': 0, 'a': 0.8, 'b': 0.8, 'c': 0.8, 'x': 3.7, 'y': 0, 'z': 0}

    nouvelAvion['ElmAero']['AileGaucheFlap']['GouverneType'] = 'Flap'
    nouvelAvion['ElmAero']['AileDroiteFlap']['GouverneType'] = 'Flap'
    nouvelAvion['ElmAero']['StabGauche']['GouverneType'] = 'Profondeur'
    nouvelAvion['ElmAero']['StabDroite']['GouverneType'] = 'Profondeur'
    nouvelAvion['ElmAero']['AileGaucheAileron']['GouverneType'] = 'RoulisGauche'
    nouvelAvion['ElmAero']['AileDroiteAileron']['GouverneType'] = 'RoulisDroite'
    nouvelAvion['ElmAero']['Gouverne']['GouverneType'] = 'Lacet'

    CurrentPlane = Avion(nouvelAvion)

    # Initialisation du vol

    ParamInit = {}
    ParamInit['vitesse'] = [56, 0.0, 0]  # Repère Global
    ParamInit['vitRot'] = [0, 0, 0]
    ParamInit['position'] = [0.0, 0.0, 100.0]
    ParamInit['assiette'] = 0.717
    ParamInit['inclinaison'] = 0
    ParamInit['course'] = 0
    ParamInit['Fmot'] = 1635 * 0.449
    ParamInit['masse'] = 1000.0

    commandesVol = {}
    commandesVol['Profondeur'] = 0
    commandesVol['Flap'] = 0
    commandesVol['Lacet'] = 0
    commandesVol['RoulisGauche'] = 0
    commandesVol['TrimProfondeur'] = -1.2933
    commandesVol['TrimLacet'] = 0
    commandesVol['TrimRoulisGauche'] = 0

    app = QtWidgets.QApplication(sys.argv)

    CurrentFlight = Vol(ParamInit, CurrentPlane, commandesVol, Instruments)

    CurrentFlight.start()

    sys.exit(app.exec_())
