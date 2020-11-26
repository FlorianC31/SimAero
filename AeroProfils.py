# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 09:52:56 2020

@author: Florian
"""

class profil:
    def __init__(self,Name,Naca,Cx,Cy,Cz,Cm_d=0):
        self.Cx=Cx
        self.Cy=Cy
        self.Cz=Cz
        
        if type(Cm_d)==list:
            self.Cm=Cm_d
            self.d_type='from_Cm'
        elif Cm_d==0:
            self.d="CoG"
            self.d_type='CoG'
        else:
            self.d=Cm_d
            self.d_type='d_direct'
        
        self.Naca=Naca
        self.Name=Name
        
        
        
    def GetCxz(self,incidence):
        
        if incidence==0:
            Cx=self.Cx[0]
            Cy=self.Cy[0]
            Cz=self.Cz[0]
            
            if self.d_type=='from_Cm':
                d=-self.Cm[0]/Cz
            else:
                d=self.d

        else:
            Cx=0
            Cy=0
            Cz=0
            
            for i in range(len(self.Cx)):
                Cx+=self.Cx[i]*incidence**i
            for i in range(len(self.Cy)):    
                Cy+=self.Cy[i]*incidence**i
            for i in range(len(self.Cz)):
                Cz+=self.Cz[i]*incidence**i
                
            if self.d_type=='from_Cm':
                Cm=0
                for i in range(len(self.Cm)):
                    Cm+=self.Cm[i]*incidence**i
                d=-Cm/Cz
            else:
                d=self.d
                
        return (Cx,Cy,Cz), d
    

    
def Profils(p):
    Profil={}
    Profil['NACA2412']=profil('NACA2412',True,[0.006708, -0.0005582, 0.000157, 0.00001086, -0.000000694, -0.0000000496, 0.000000004362], [0], [0.2673, 0.1143, -0.001372, -0.00002579, 0.000001068, -0.0000005975, 0.00000001896],[-0.1235, -0.02929, -0.0008014, 0.0006912, -0.0001588, 0.00001622, -0.0000005935])
    Profil['NACA0012']=profil('NACA0012',True,[0.00452, 0.0003342, 0.0003304, -0.000006197, -0.000002723, 0.00000002107, 0.000000009392], [0], [0, 0.1194, -0.0002851, -0.0001056, 0.000003238, -0.0000002836, -0.000000008636], 0.265)
    Profil['Train']=profil('Train',False, [0.033], [0.1], [0.06])
    Profil['PrimStruct']=profil('PrimStruct',False, [0.033], [0.08], [0.08])
    Profil['SecondStruct']=profil('SecondStruct',False, [0], [0.08], [0.08])
    return Profil[p]
    

if __name__ == '__main__':
    p=Profils('Train')
    print(p.GetCxz(0))