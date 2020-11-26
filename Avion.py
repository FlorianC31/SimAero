# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:19:32 2020

@author: Florian
"""

from AeroProfils import Profils
from matrix3D import ProdVectoriel, SoustractVect, AddVect, ProduitMat, RotMatrix, Norm, PrintMatrix
from math import degrees, atan2, pi

class Tensor:
    def __init__(self,force,position,Reference='Global',moment=[0,0,0]):
        self.Force=force
        self.Position=position
        self.Moment=moment
        self.Reference=Reference
        
    def Rotate(self,RotMat,NewRef):
        
        self.Force=ProduitMat(self.Force,RotMat)
        self.Moment=ProduitMat(self.Moment,RotMat)
        self.Reference=NewRef
        
        
    def Transport(self,newPosition):
        deltaP=SoustractVect(newPosition,self.Position)
        self.Moment=AddVect(self.Moment,ProdVectoriel(deltaP,self.Force))
        self.Position=newPosition


    def Add(self,tensor):
        self.Force=AddVect(self.Force,tensor.Force)
        self.Moment=AddVect(self.Moment,tensor.Moment)
        
        
    def Print(self,Titre):
        output=Titre
        for x in self.Force:
            output+=', '+str(x)
        for x in self.Moment:
            output+=', '+str(x)
        
        print(output)



class Avion:
    def __init__(self,InputData):
        self.puissanceMoteur=InputData['puissanceMoteur']
        self.Elements={}
        for Elm in InputData['ElmAero']:
            self.Elements[Elm]=ElmStruct(Elm,InputData['ElmAero'][Elm])
        self.GetCoG()
        self.ViewTensor=[]


    def GetCoG(self):
        self.CoG=[0,0,0]
        self.TotalMass=0
        for Elm in self.Elements:
            M=self.Elements[Elm].Mass
            self.TotalMass+=M
            for i in range(3):
                self.CoG[i]+=self.Elements[Elm].Position[i]*M
        for i in range(3):
            self.CoG[i]=self.CoG[i]/self.TotalMass       

                
    def GetInertia(self):
        self.Inertia=[0,0,0]
        for Elm in self.Elements:
            Io=self.Elements[Elm].getCoGInertia(self.CoG)
            for i in range(3):
                self.Inertia[i]+=Io[i]
             
    def ApplyCommandesVol(self,CommandesVol):
        for Elm in self.Elements:
            GouverneName=self.Elements[Elm].GouverneType
            if GouverneName in CommandesVol:
                self.Elements[Elm].Gouverne=CommandesVol[GouverneName]
                TrimName='Trim'+GouverneName
                if TrimName in CommandesVol:
                    self.Elements[Elm].Trim=CommandesVol[TrimName]
            else:
                self.Elements[Elm].Gouverne=0
                self.Elements[Elm].Trim=0
                
        
        
        
    def GetGlobalTensor(self,vol):
        
        self.Rho=vol.Rho
        
        self.RotMat={}
        self.RotMat['Avion2Global']=RotMatrix(vol.angles,True)
        
        self.Vitesse={}
        self.Vitesse['Global']=vol.vitesse
        self.Vitesse['Avion']=ProduitMat(vol.vitesse, self.RotMat['Avion2Global'])
        self.Vitesse['Aero']=Norm(vol.vitesse)
        
        self.Incidence={}
        self.Incidence['XZ']=-degrees(atan2(self.Vitesse['Avion'][2],self.Vitesse['Avion'][0]))
        self.Incidence['XY']=-degrees(atan2(self.Vitesse['Avion'][1],self.Vitesse['Avion'][0]))
        self.Incidence['XYZ']=0
        

        self.RotMat['Aero2Avion']=RotMatrix((0,self.Incidence['XZ'],self.Incidence['XY']),True)
        self.RotMat['Aero2Global']=ProduitMat(self.RotMat['Aero2Avion'],self.RotMat['Avion2Global'])
        
        self.GlobalTensor=Tensor([0,0,0],self.CoG,'Global',[0,0,0])
        
        self.Tensors={}
        
        for Elm in self.Elements:
            if self.Elements[Elm].Profil!="":

                alpha=self.Incidence[self.Elements[Elm].Plan]


                ElmTensor=self.Elements[Elm].getTensor(self.Rho,alpha,self.Vitesse['Aero'],self.Vitesse['Avion'])
                
                ElmTensor.Transport(self.CoG)
                #ElmTensor.Print(Elm)
                ElmTensor.Rotate(self.RotMat[ElmTensor.Reference + '2Global'],'Global')
                
                self.Tensors[Elm]=ElmTensor

                self.GlobalTensor.Add(ElmTensor)

            
        self.MotorTensor=Tensor((-vol.Fmot,0,0),self.Elements['Helice'].Position,'Avion')
        self.MotorTensor.Transport(self.CoG)
        self.MotorTensor.Rotate(self.RotMat['Avion2Global'],'Global')
        self.GlobalTensor.Add(self.MotorTensor)

        
        self.GravityTensor=Tensor((0,0,-vol.gravity*self.TotalMass),self.CoG,'Global')
        self.GlobalTensor.Add(self.GravityTensor)
        
        
        self.setViewTensor()        
        
        
    def setViewTensor(self):
        group=[]
        group.append([['TrainAvant','TrainGauche','TrainDroite','Moteur','Cabine','Queue'],self.CoG])
        group.append([['AileGaucheFlap','AileGaucheAileron','AileDroiteFlap','AileDroiteAileron'],(self.Elements['AileGaucheFlap'].Position[0],0,self.Elements['AileGaucheFlap'].Position[2])])
        group.append([['StabGauche','StabDroite','Gouverne'],(self.Elements['StabGauche'].Position[0],0,self.Elements['StabGauche'].Position[2])])

        self.ViewTensor=[]

        for g in group:
            for elm in g[0]:
                if g[0].index(elm)==0:
                    newTensor=self.Tensors[elm]
                else:
                    newTensor.Add(self.Tensors[elm])
                newTensor.Transport(g[1])
            self.ViewTensor.append(newTensor)
        self.ViewTensor.append(self.GravityTensor)
        self.ViewTensor.append(Tensor(self.MotorTensor.Force,self.Elements['Helice'].Position,'Avion'))
        
        
        
        
    def GetAcceleration(self):
        self.AccelerationLinear=[]
        self.AccelerationRotation=[]
        for i in range(3):
            self.AccelerationLinear.append(self.GlobalTensor.Force[i]/self.TotalMass)
            self.AccelerationRotation.append(self.GlobalTensor.Moment[i]/self.Inertia[i])
        #print(self.GlobalTensor.Moment[1]/self.Inertia[1],self.GlobalTensor.Moment[1],self.Inertia[1])
            






class ElmStruct:
    def __init__(self,Name,InputData):
        self.Name=Name
        self.InputData=InputData
        self.Position=[self.InputData['x'],self.InputData['y'],self.InputData['z']]
        self.Mass=InputData['Mass']
        self.Gouverne=0
        self.Trim=0
        self.Ksm=0.5
        if 'GouverneType' in InputData:
            self.GouverneType=InputData['GouverneType']
        else:
            self.GouverneType=''
        
        if 'Profil' in InputData:
            self.Profil=Profils(InputData['Profil'])
            self.Plan=InputData['Plan']
            self.getAreas()
        else:
            self.Profil=''
            self.Plan=''
        
    def getSelfInertia(self):
        M=self.Mass
        if 'a' in self.InputData:
            a=self.InputData['a']
            b=self.InputData['b']
            c=self.InputData['c']
            self.SelfInertia=[M*b*c/4,M*a*c/4,M*a*b/4]
        else:
            h=self.InputData['h']
            r=self.InputData['r']
            self.SelfInertia=[M*r**2,M/12*(6*r**2+h**2),M/12*(6*r**2+h**2)]
            

            
            
    def getCoGInertia(self,CoG):
        self.getSelfInertia()
        
        x=self.InputData['x']
        y=self.InputData['y']
        z=self.InputData['z']
        M=self.Mass
        
        xo=CoG[0]
        yo=CoG[1]
        zo=CoG[2]
        
        Ix=self.SelfInertia[0]
        Iy=self.SelfInertia[1]
        Iz=self.SelfInertia[2]
        
        Iox=Ix+M*((yo-y)**2+(zo-z)**2)
        Ioy=Iy+M*((zo-z)**2+(xo-x)**2)
        Ioz=Iz+M*((xo-x)**2+(yo-y)**2)

        return [Iox,Ioy,Ioz]
            
    
    def getAreas(self):
        if 'a' in self.InputData:
            a=self.InputData['a']
            b=self.InputData['b']
            c=self.InputData['c']
            if self.Profil.Naca:
                if self.Plan=="XZ":
                    self.Areas=[a*b,0,a*b]
                else:
                    self.Areas=[a*c,a*c,0]
            else:
                self.Areas=[b*c,a*c,a*b]
        else:
            h=self.InputData['h']
            r=self.InputData['r']
        
            self.Areas=[pi*r**2,r*h,r*h]
            
            
    def getTensor(self,Rho,Incidence,VitesseAero,VitesseAvion):
        p=self.Profil
        Force=[]
        
        Alpha=Incidence+(self.Gouverne+self.Trim)*self.Ksm
        C, d=p.GetCxz(Alpha)
        

        if p.Naca:
            a=self.InputData['a']
            position=[self.Position[0]-a/2+a*d,self.Position[1],self.Position[2]]
            for i in range(3):
                Force.append(1/2*Rho*C[i]*self.Areas[i]*VitesseAero**2)
            if self.Name=='AileGaucheFlap':
                pass#print(self.Name,C[2],self.Areas[2],d,Incidence,VitesseAero,Force[2])
            tensor=Tensor(Force,position,'Aero')
        else:
            for i in range(3):
                Force.append(1/2*Rho*C[i]*self.Areas[i]*VitesseAvion[i]**2)
            tensor=Tensor(Force,self.Position,'Avion')
        return tensor
        
        