# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:30:45 2023

@author: lass_j


"""
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

import sys
sys.path.append('.')
from RPA import Lattice, formFactor, System, Units
from scipy.ndimage import gaussian_filter


    
import time

start = time.time()
    

#########
lat=[10.088,11.943,3.42]# 


T=0.1#  in K
H=[0,0,0]#  in T



J1=-0.1484/3.9892**2# 
J2=-0.1023/3.9892**2# 
facO21=0# 


J1S1=np.zeros((8,8))
J1S1[:3,:3]=J1*np.eye(3)

J2S1=np.zeros((8,8))
J2S1[:3,:3]=J2*np.eye(3)

# 'Jx'    'Jy'    'Jz'    'O20'    'O2+1'    'O2-1'    'O2+2'    'O2-2'
#   1       2      3        4        5         6         7          8
J2S1[4,4]=facO21;

##
epsilon=0.05;
omega=np.arange(2,10,epsilon/3)#
wid=0.1

# ElasticThreshold=1e-2
Qz=np.arange(0,2,0.075)


Qy=np.zeros_like(Qz)#((len(Qz)))
Qx=np.zeros_like(Qz)
QRLU=np.asarray([Qx,Qy,Qz])

positions = np.asarray([[0.4242,0.1110,0.25],
                        [0.5758,0.8890,0.75]])

lattice = Lattice(S=[15/2,15/2],g = [4/3,4/3],active = [1,1],positions = positions,
                  label = ['Dy1','Dy1'], site = [1,1], lattice = [10.0884,11.9427,3.4289],
                  equivalence=[1,3])

S = System(temperature=T,magneticField=H, lattice=lattice)

S.lattice.generateCouplings(maxDistance = 3.51)

distances = [3.5082,3.4289]
Js = [J1S1,J2S1]

S.lattice.addExchangeInteractions(Js,distances)


S.operators = loadmat(r'C:\Users\lass_j\Documents\Software\RPA\RPA for Simon\operators\operatorsDySite1_1XM_O2.mat')
S.energies = np.array([0,0,4,4,8.09,8.09])



# InitialDistributionSite1_Ext
sizeS = 3.9892
doubling = True # Along c only
config = 1 # not sure
Ncell = 2
nExt = [1,1,Ncell]
numOperators = len(S.operators['operatorList'][0])
site1 = np.zeros((numOperators,len(S.lattice.r)))
site1[2,0] = sizeS
site1[2,1] = site1[2,0]*config

fc = site1
fullConfiguration = np.repeat(fc, Ncell,axis=-1)

spins = np.repeat(site1[:3],Ncell,axis=-1)

if doubling: # add AFM along c
    tt=np.ones_like(fullConfiguration)
    tt[:,-2::4]=-tt[:,-2::4]
    tt[:,-1::4]=-tt[:,-1::4]
    
    
    fullConfiguration=fullConfiguration*tt;
    
    
S.fullConfiguration = fullConfiguration


S.lattice.NCell = int(np.product(nExt))

S.lattice.nExt = nExt

## perform actual calculations
S.solveSelfConsistency()

S.calculateChi0(omega)
    
S.calculateJQ(QRLU)

S.calculateChi()

S.calculateSperp()
## calculate prefactor from temperature as well as form factor 

prefactor = (1.0/(1-np.exp(-omega*Units.calculateKelvinToMeV(T)*Units.meV))).reshape(1,-1)  # shape (nQ,nE)

## Calculate Formfactor for Dysprosium... 

qLength = np.linalg.norm(S.QPoints,axis=1)
A=0.1157;
a=15.073;
B=0.3270;
b=6.799;
C=0.5821;
c=3.020;
D=-0.0249;

Ap=0.2523;
ap=18.517;
Bp=1.0914;
bp=6.736;
Cp=0.9345;
cp=2.208;
Dp=0.0250;

J = 15/2
Sval=5/2
L = 5

Sperp = S.Sperp

F2 = formFactor(qLength,A=A,a=a,B=B,b=b,C=C,c=c,D=D,
                Ap=Ap,ap=ap,Bp=Bp,bp=bp,Cp=Cp,cp=cp,Dp=Dp,
                J=J,S=Sval,L=L).reshape(-1,1)#np.ones((nQ,1))

Sperp*=F2*prefactor



## Do a Gaussian smearing of the data

sigmaE = 0.1/np.diff(omega[[1,0]])
sigmaQ = 0.05/np.linalg.norm(np.diff(S.QPoints[[1,0]],axis=0))


I = gaussian_filter(Sperp,[sigmaQ,sigmaE],mode='constant',cval=0)



fig,ax = plt.subplots()
p = ax.pcolormesh(QRLU[2],omega,I.T,shading='auto')#I.T)
ax.axis('auto')
fig.colorbar(p)
ax.set_xlabel('Q = (0,0,L) [rlu]')
ax.set_ylabel('Energy [meV]')
p.set_clim(0,1000)


stop = time.time()
print('Calculation done in {:.2f} s'.format(stop-start))

