# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 20:36:11 2020

@author: Florian
"""

from math import cos, sin, radians


def jk(i):
    if i==0:
        j=1
        k=2
    elif i==1:
        j=2
        k=0
    elif i==2:
        j=0
        k=1
    return j,k
    


def ProdScalaire(vectA,vectB):
    result=0
    for i in range(3):
        result+=vectA[i]+vectB[i]
    return result
    

def ProdVectoriel(vectA,vectB):
    result=[]
    for i in range(3):
        j,k=jk(i)     
        result.append(vectA[j]*vectB[k]-vectA[k]*vectB[j])
    return result
    
def Norm(vect):
    return (vect[0]**2+vect[1]**2+vect[2]**2)**0.5


def VectUnit(vect):
    unitaire=[]
    norm=Norm(vect)
    for i in range(3):
        unitaire.append(vect[i]/norm)


def Rotation(vect,matrix):
    result=[]
    for i in range(3):
        r=0
        for j in range(3):
            r+=vect[i]*matrix[i][j]
        result.append(r)
    return result



def RotMatrix(angles,inverse=False):
    MatrixSingle=[]    
    for i in range(3):
        if inverse:
            j=2-i
            signe=-1
        else:
            j=i
            signe=1
        MatrixSingle.append(RotMatrixSingle(radians(angles[j])*signe,j))
    return ProduitMat(ProduitMat(MatrixSingle[0],MatrixSingle[1]),MatrixSingle[2])


def PrintMatrix(matrix):
    for i in matrix:
        print(i[0],i[1],i[2])




def RotMatrixSingle(angle,i):
    j,k=jk(i)
    
    matrix=[[0,0,0],[0,0,0],[0,0,0]]
    matrix[i][i]=1
    matrix[i][j]=0
    matrix[i][k]=0
    matrix[j][i]=0
    matrix[j][j]=cos(angle)
    matrix[j][k]=-sin(angle)
    matrix[k][i]=0
    matrix[k][j]=sin(angle)
    matrix[k][k]=cos(angle)
    
    return matrix


def Vect2Mat(vector):
    result=[]
    for i in vector:
        result.append(i)
    return [result]


            
def ProduitMat(mat1,mat2):
    
    vector=False
    if type(mat1[0])!=list:
        mat1=Vect2Mat(mat1)
        vector=True

    result=[]
    for line1 in mat1:
        resultLine=[]
        for line2 in mat2:
            i=mat2.index(line2)
            for col2 in line2:
                j=line2.index(col2)
                if i==0:
                    resultLine.append(0)
                resultLine[j]+=line1[i]*col2
        result.append(resultLine)
    if vector:
        return result[0]
    else:
        return result
    
    
def SoustractVect(vect1,vect2):
    vector=[]
    for i in range(3):
        vector.append(vect1[i]-vect2[i])
    return vector
  

def AddVect(vect1,vect2):
    vector=[]
    for i in range(3):
        vector.append(vect1[i]+vect2[i])
    return vector          

def PrintMat(mat):
    for line in mat:
        print(','.join(map(str,line)))




if __name__ == '__main__':
    RotMat1=RotMatrix((17,52,82))
    RotMat2=RotMatrix((17,52,82),True)
    #PrintMat(RotMat)
    print(ProduitMat(ProduitMat((12,24,5),RotMat1),RotMat2))
    

    