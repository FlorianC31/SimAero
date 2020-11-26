# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 10:53:13 2020

@author: Florian
"""
from matrix3D import ProdVectoriel, SoustractVect, AddVect, ProduitMat, RotMatrix, Norm
from math import degrees, atan2, pi


class tensor:
    def __init__(self,force,position,Reference='Global',moment=[0,0,0]):
        self.Force=force
        self.Position=position
        self.Moment=moment
        self.Reference=Reference
        
    def Rotate(self,RotMatrix):
        
        RotForce=ProduitMat(self.Force,RotMatrix)
        RotMoment=ProduitMat(self.Moment,RotMatrix)
        return tensor(RotForce,(0,0,0),RotMoment)
        
        
    def Transport(self,newPosition):
        deltaP=SoustractVect(newPosition,self.Position)
        print(deltaP)
        self.Moment=AddVect(self.Moment,ProdVectoriel(self.Force,deltaP))


    def Add(self,tensor):
        self.Force=AddVect(self.Force,tensor.Force)
        self.Moment=AddVect(self.Moment,tensor.Moment)
        
        
    def Print(self):
        print('Force:',[int(round(x,0)) for x in self.Force],'N')
        print('Moment:',[int(round(x,0)) for x in self.Moment],'N.m')

            
            
        
class ElmAero:
    def __init__(self,profile,surface,position,plan):
        self.profile=profile
        self.surface=surface
        self.position=position
        self.plan=plan
        self.angle=0
        
        
    def SetTensor(self,vitesse,rho,incidence):
        alpha=incidence[self.plan]+self.angle
        print('alpha:',alpha)
        f=1/2*rho*self.surface*Norm(vitesse)**2
        force=[]
        for C in self.profile:
            if type(self.profile[C])==tuple:
                result=0
                for i in self.profile[C]:
                    exposant=len(self.profile[C])-self.profile[C].index(i)-1
                    result += i * alpha ** exposant
                force.append(f*result)
                print(C,result)
            else:
                force.append(f*self.profile[C])   
                print(C,self.profile[C]) 

        self.tensor=tensor(force,self.position)
    
    
            
        
    
    
class avion:
    def __init__(self,nouvelAvion):
        self.nom=nouvelAvion['nom']
        self.envergure=nouvelAvion['envergure']
        self.longueur=nouvelAvion['longueur']
        self.surfaceAlaire=nouvelAvion['surfaceAlaire']
        self.surfaceStab=nouvelAvion['surfaceStab']
        self.masseVide=nouvelAvion['masseVide']
        self.massMaxi=nouvelAvion['massMaxi']
        self.puissanceMoteur=nouvelAvion['puissanceMoteur']
        self.CoG=(nouvelAvion['CoG'],0,0)
        self.FuseRadius=nouvelAvion['FuseRadius']
        self.ElmAero=nouvelAvion['ElmAero']
        
        
        
    def GetGlobalTensor(self,vol):        
        
        # 3 repères:
        # - Repère Global
        # - Repère Avion
        # - Repère Aéro
        
        RotMat={}
        RotMat['Global2Avion']=RotMatrix((vol.inclinaison,vol.assiette,vol.course))
        RotMat['Avion2Global']=RotMatrix((vol.inclinaison,vol.assiette,vol.course),True)
                

        AvionVit=ProduitMat(vol.vitesse, RotMat['Avion2Global'])
        
        incidence={}
        incidence['XZ']=-degrees(atan2(AvionVit[2],AvionVit[0]))
        incidence['XY']=-degrees(atan2(AvionVit[1],AvionVit[0]))
        incidence['XYZ']=-degrees(atan2((AvionVit[2]**2+AvionVit[1]**2)**0.5,AvionVit[0]))

        RotMat['Aero2Avion']=RotMatrix((0,incidence['XZ'],incidence['XY']),False)
        
        print('VitesseGlobal:',vol.vitesse)
        print('VitesseAvion:',AvionVit)
        print(incidence)
        print('')
        
        
        AeroTensor=tensor([0,0,0],self.CoG)
        for Elm in self.ElmAero:
            print(Elm)
            self.ElmAero[Elm].SetTensor(vol.vitesse,vol.Rho,incidence)
            self.ElmAero[Elm].tensor.Transport(self.CoG)
            AeroTensor.Add(self.ElmAero[Elm].tensor)
            self.ElmAero[Elm].tensor.Print()
            print('')
            
        print('Total Aero')
        AeroTensor.Print()
        print('')
        
        AvionTensor=AeroTensor.Rotate(RotMat['Aero2Avion'])
        
        
        MotorTensor=tensor((-vol.Fmot,0,0),(0,0,0))
        print('Motor:')
        MotorTensor.Print()
        print('')
        AvionTensor.Add(MotorTensor)
        print('Total Avion')
        AvionTensor.Print()
        print('')
        
        
        
        GlobalTensor=AvionTensor.Rotate(RotMat['Avion2Global'])
        
        GravityTensor=tensor((0,0,-vol.gravity*vol.masse),(0,0,0))
        print('Gravity:')
        GravityTensor.Print()
        print('')
        GlobalTensor.Add(GravityTensor)

        return GlobalTensor
        
        
        
    
class Vol:
    def __init__(self,ParamInit,avion,commandesVol):
        
        # Param espace
        self.vitesse=ParamInit['vitesse'] # Repère Global
        self.vitRot=ParamInit['vitRot']
        self.position=ParamInit['position']
        self.assiette=ParamInit['assiette']   # Beta
        self.trajectoire=degrees(atan2(self.vitesse[2],self.vitesse[0]))     # Teta
        self.incidence=self.assiette - self.trajectoire        # Alpha = Beta - Teta
        self.inclinaison=0
        self.course=0
        
        # Param forces
        self.force={}
        self.moment=0
        self.Fmot=ParamInit['Fmot']
        self.gravity=9.81 # m/s²
        self.Rho=1.225 # kg/m³
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
        self.avion.ElmAero['StabGauche'].angle=self.profondeur
        self.avion.ElmAero['StabDroite'].angle=self.profondeur
        
           
    
    def getInertia(self):
        inertia = self.masse / 12 * (6 * self.avion.FuseRadius ** 2 + self.avion.longueur **2)
        return inertia
    
    
    def GetAvionTensor(self):
        GlobalTensor=self.avion.GetGlobalTensor(self)
        print('GlobalTensor')
        GlobalTensor.Print()
        

    
        
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
    nouvelAvion['CoG']=2.0 # m
    nouvelAvion['FuseRadius']=0.6 # m
    
    nouvelAvion['ElmAero']={}

    profile={'Cx':(0.000000004362,-0.0000000496,-0.000000694,0.00001086,0.000157,-0.0005582,0.006708),'Cy':0,'Cz':(0.00000001896,-0.0000005975,0.000001068,-0.00002579,-0.001372,0.1143,0.2673)}
    surface=8.1 # m²
    planIncidence='XZ'
    position=(2.1,-nouvelAvion['envergure']/4,0)
    nouvelAvion['ElmAero']['AileGauche']=ElmAero(profile,surface,position,planIncidence)
    position=(2.1,nouvelAvion['envergure']/4,0)
    nouvelAvion['ElmAero']['AileDroite']=ElmAero(profile,surface,position,planIncidence)
    
    profile={'Cx':0.33,'Cy':0,'Cz':0}
    surface=pi*nouvelAvion['FuseRadius']**2 # m²
    position=(nouvelAvion['CoG'],0,0)
    planIncidence='XYZ'
    nouvelAvion['ElmAero']['Fuselage']=ElmAero(profile,surface,position,planIncidence)
    
    
    profile={'Cx':(0.000000009392,0.00000002107,-0.000002723,-0.000006197,0.0003304,0.0003342,0.00452),'Cy':0,'Cz':(-0.000000008636,-0.0000002836,0.000003238,-0.0001056,-0.0002851,0.1194,0.0)}
    surface=1.35 # m²
    planIncidence='XZ'
    position=(8,-3.75/4,0)
    nouvelAvion['ElmAero']['StabGauche']=ElmAero(profile,surface,position,planIncidence)
    position=(8,3.75/4,0)
    nouvelAvion['ElmAero']['StabDroite']=ElmAero(profile,surface,position,planIncidence)
        
    surface=0#1 # m²
    position=(8,0,0)
    planIncidence='XY'
    nouvelAvion['ElmAero']['Gouverne']=ElmAero(profile,surface,position,planIncidence)
    
    
    CurrentPlane=avion(nouvelAvion)
    
    
    # Initialisation du vol
    
    ParamInit={}
    ParamInit['vitesse'] = [39.2,0.0,5.0]    # Repère Global
    ParamInit['vitRot']=0
    ParamInit['position']=[0.0,0.0,100.0]
    ParamInit['assiette']=8.0   # Beta
    ParamInit['Fmot']=CurrentPlane.puissanceMoteur * 745.699872 * 0.15 / 35
    ParamInit['masse']=1000.0
    
    commandesVol={}
    commandesVol['profondeur']=-14.7430604461893    # Phi
    
    CurrentFlight=vol(ParamInit,CurrentPlane,commandesVol)


    CurrentFlight.GetAvionTensor()
