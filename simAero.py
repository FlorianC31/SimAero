# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 19:04:51 2020

@author: Florian
"""

from math import radians, degrees, cos, sin, atan2




class avion():
    def __init__(self,nouvelAvion):
        self.nom=nouvelAvion['nom']
        self.envergure=nouvelAvion['envergure']
        self.longueur=nouvelAvion['longueur']
        self.surfaceAlaire=nouvelAvion['surfaceAlaire']
        self.surfaceStab=nouvelAvion['surfaceStab']
        self.masseVide=nouvelAvion['masseVide']
        self.massMaxi=nouvelAvion['massMaxi']
        self.puissanceMoteur=nouvelAvion['puissanceMoteur']
        self.profil=nouvelAvion['profil']
        self.CoG=(nouvelAvion['CoG'],0)
        self.Xaile=(nouvelAvion['Xaile'],0)
        self.Xstab=(nouvelAvion['Xstab'],0)
        self.FuseRadius=nouvelAvion['FuseRadius']
        
        
    def getCxz(self,incidence):
        output=[]
        for C in self.profil:
            result=0
            for i in self.profil[C]:
                result += i * incidence ** self.profil[C].index(i)
            output.append(result)
        return output
    
    
class force():
    def __init__(self,charge,position):
        self.charge=charge
        self.position=position
        
    def calculMoment(self,point):
        moment = self.charge[0] * (point[1] - self.position[1]) - self.charge[1] * (point[0] - self.position[0])
        return moment
    
    
    def RepereGlobal(self,inclinaison):
        GlobalCharge=[]
        GlobalCharge.append(self.charge[0] * cos(radians(inclinaison)) - self.charge[1] * sin(radians(inclinaison)))
        GlobalCharge.append(self.charge[1] * cos(radians(inclinaison)) + self.charge[0] * sin(radians(inclinaison)))
        self.charge=GlobalCharge
    
    
class vol():
    def __init__(self,ParamInit,avion,commandesVol):
        
        # Param espace
        self.vitesse=ParamInit['vitesse'] # Repère Global
        self.vitRot=ParamInit['vitRot']
        self.position=ParamInit['position']
        self.inclinaison=ParamInit['inclinaison']   # Beta
        self.trajectoire=degrees(atan2(self.vitesse[1],self.vitesse[0]))     # Teta
        self.incidence=self.inclinaison - self.trajectoire        # Alpha = Beta - Teta
        
        # Param forces
        self.force={}
        self.moment=0
        self.Fmot=ParamInit['Fmot']
        self.gravity=9.81 # m/s²
        self.Rho=1.225 #♣ kg/m³
        self.acceleration=[0,0]
        self.accAngulaire=0
        
        # Param Avion
        self.avion=avion
        self.masse=ParamInit['masse']
        self.AngInertia=self.getInertia()
        
        # Param Simu
        self.IterTime=0.1 # s
        self.time=-self.IterTime
        
        # Param Commandes
        self.profondeur=commandesVol['profondeur']      # Phi
        
        
    def getInertia(self):
        inertia = self.masse / 12 * (6 * self.avion.FuseRadius ** 2 + self.avion.longueur **2)
        return inertia
    
        
        
    def iteration(self):
        
        self.time+=self.IterTime
        self.calculVitesse()
        if self.time>0:
            self.calculDeplacement()
        self.calculForce()
        self.autostab()
        self.calculAcceleration()

    
    def calculVitesse(self):
        for i in range(len(self.vitesse)):
            self.vitesse[i] += self.acceleration[i] * self.IterTime

        self.vitRot += self.accAngulaire * self.IterTime
                
        self.trajectoire=degrees(atan2(self.vitesse[1],self.vitesse[0]))     # Teta
        
        

    
    def calculDeplacement(self):
        for i in range(len(self.vitesse)):
            self.position[i]+=self.vitesse[i]*self.IterTime
            
        self.inclinaison += self.vitRot *self.IterTime
        self.incidence=self.inclinaison - self.trajectoire        # Alpha = Beta - Teta
        
            
            
    def getPortance(self,surface,incidence):
        V=(self.vitesse[0]**2 + self.vitesse[1]**2)**0.5
        Cxz=self.avion.getCxz(incidence)
        portance=[]
        portance.append(-1/2 * V**2 * self.Rho * surface * Cxz[0])
        portance.append(1/2 * V**2 * self.Rho * surface * Cxz[1])
        return portance
    
    
    def calculForce(self):
            
        # Gravité
        self.force['gravity']=force((0,-self.gravity*self.masse),self.avion.CoG)
    
        # Moteur
        self.force['motor']=force((self.Fmot,0),self.avion.CoG)
        
        # Portance Aile
        self.force['portance']=force(self.getPortance(self.avion.surfaceAlaire,self.incidence),self.avion.Xaile)

        # Portance Stab
        self.force['stab']=force(self.getPortance(self.avion.surfaceStab,self.incidence+self.profondeur),self.avion.Xstab)
        

        self.moment=0
        for f in self.force:
            self.moment+=self.force[f].calculMoment(self.avion.CoG)
            
        # Expression des torseurs dans le repère Global
        self.force['motor'].RepereGlobal(self.inclinaison)
        self.force['portance'].RepereGlobal(self.inclinaison-self.incidence) # Teta = Beta - Alpha
        self.force['stab'].RepereGlobal(self.inclinaison-self.incidence) # Teta = Beta - Alpha
        
                
    def calculAcceleration(self):
        
        for i in range(len(self.acceleration)):
            self.acceleration[i]=0
            for f in self.force:
                self.acceleration[i] += self.force[f].charge[i] / self.masse
                
        self.accAngulaire = self.moment / self.AngInertia
    
    
    def printParam(self):

        print('Vitesse:',[round(x,1) for x in self.vitesse], 'm/s')
        print('Position:',[round(x,0) for x in self.position],' m')
        print('Moment:',str(round(self.moment,0)),'N.m')
        print('incidence (Alpha):',str(round(self.incidence,2)),'°')
        print('inclinaison (Beta):',str(round(self.inclinaison,2)),'°')
        print('trajectoire (Teta):',str(round(self.trajectoire,2)),'°')
        print('stab (Phi):',str(round(self.profondeur,2)),'°')
        for f in self.force:
            print(f,'->',[round(x,0) for x in self.force[f].charge],'N')
            print(f,'->',str(round(self.force[f].calculMoment(self.avion.CoG),0)),'N.m')
        print('Acceleration:',[round(x,1) for x in self.acceleration],' m')
        
        
    def autostab(self):
        x=[]
        y=[]
        x.append(self.profondeur)
        y.append(self.moment)
        
        x.append(x[0]+2)
        self.profondeur=x[1]
        self.calculForce()
        y.append(self.moment)
        
        i=0
        
        while abs(y[i+1])>1 and i<50:

            a=(y[i+1]-y[i])/(x[i+1]-x[i])
            b=y[i+1]-a*x[i+1]
            
            
            x.append(-b/a)
            self.profondeur=x[i+2]
            self.calculForce()
            y.append(self.moment)
            i+=1
            
        #print('Itérations:',i)
            
        
            
    
    
if __name__ == '__main__':
    
    # Définition Cesna 172
    nouvelAvion={}
    nouvelAvion['nom']="Cesna 172"
    nouvelAvion['envergure']=11.0 # m
    nouvelAvion['longueur']=8.28 # m
    nouvelAvion['surfaceAlaire']=16.2 # m²
    nouvelAvion['surfaceStab']=nouvelAvion['surfaceAlaire'] / 6
    nouvelAvion['masseVide']=779.0 # kg
    nouvelAvion['massMaxi']=1111.0 # kg
    nouvelAvion['puissanceMoteur']=160.0 # HP
    nouvelAvion['profil']={'Cx':(0.0100658, -0.000683448, 0.000103685, 0.0000318888, 0.0000000976181, -0.00000043463, 0.0000000266707),'Cz':(0.161398, 0.149321, -0.00584013, -0.000974682, 0.000122132, 0.00000209553, -0.000000427536)}
    
    nouvelAvion['CoG']=2.0 # m
    nouvelAvion['Xaile']=2.1 # m
    nouvelAvion['Xstab']=8 # m
    nouvelAvion['FuseRadius']=0.6 # m
    
    CurrentPlane=avion(nouvelAvion)
    
    
    # Initialisation du vol
    
    ParamInit={}
    ParamInit['vitesse'] = [39.2,5.0]    # Repère Global
    ParamInit['vitRot']=0
    ParamInit['position']=[0.0,100.0]
    ParamInit['inclinaison']=10.0   # Beta
    ParamInit['Fmot']=CurrentPlane.puissanceMoteur * 745.699872 * 0.15 / 35
    ParamInit['masse']=1000.0
    
    commandesVol={}
    commandesVol['profondeur']=-4.8    # Phi
    
    CurrentFlight=vol(ParamInit,CurrentPlane,commandesVol)

    '''
    CurrentFlight.iteration()
    CurrentFlight.printParam()
    print('')
    CurrentFlight.iteration()
    CurrentFlight.printParam()'''
    
    for i in range(101):
        CurrentFlight.iteration()
        print(round(CurrentFlight.time,1),',',CurrentFlight.position[0],',',CurrentFlight.position[1],',',CurrentFlight.incidence,',',CurrentFlight.inclinaison,',',CurrentFlight.trajectoire,',',CurrentFlight.profondeur,',',CurrentFlight.acceleration[0],',',CurrentFlight.acceleration[1])
        
        
    
    
    
    
    