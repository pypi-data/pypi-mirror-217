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
from RPA import Lattice, System, Units
from MagneticFormFactor import formFactor
from scipy.ndimage import gaussian_filter


    
import time

start = time.time()
    

#########
lat=[10.088,11.943,3.42]# 


T=0.1#  in K
H=[0,0,0]#  in T



J1=0#-0.1484/3.9892**2# 
J2=0#-0.1023/3.9892**2# 
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
omega=np.arange(0,9,epsilon/3)#
wid=0.1

# ElasticThreshold=1e-2
Qz=np.arange(0,2,0.075)


Qy=np.zeros_like(Qz)#((len(Qz)))
Qx=np.zeros_like(Qz)
QRLU=np.asarray([Qx,Qy,Qz])

positions = np.asarray([[0.4242,0.1110,0.25],
                        [0.5758,0.8890,0.75]])

lattice = Lattice(S=[15/2,15/2],g = [4/3,4/3],active = [1,1],positions = positions,
                  label = ['Dy1','Dy1'], site = [1,1], lattice = [10.0884,11.9427,3.4289,90,90,90],
                  equivalence=[0,0])

S = System(temperature=T,magneticField=H, lattice=lattice)

S.lattice.generateCouplings(maxDistance = 3.51)

distances = [3.5082,3.4289]
Js = [J1S1,J2S1]

S.lattice.addExchangeInteractions(Js,distances)


S.operators = loadmat(r'C:\Users\lass_j\Documents\Software\RPA\RPA for Simon\operators\operatorsSHO_sxtal0p45.mat')['operator']
S.operators = np.asarray([S.operators,S.operators])
S.energies = np.array([[0,0.626,2.12,3.07,5.36,8.22]])



# InitialDistributionSite1_Ext
sizeS = 3.9892
doubling = False # Along c only
config = 1 # not sure
Ncell = 1
nExt = [1,1,Ncell]
numOperators = S.operators.shape[-1]
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
    
S.lattice.NCell = int(np.product(nExt))

S.lattice.nExt = nExt




    
fig,Ax = plt.subplots(nrows=2,ncols=2,figsize=(14,10))
Ax = Ax.flatten()
for field,ax in zip([0.0,0.1,0.5,1.0],Ax):
    
    S.magneticField = np.array([0.0,0.0,field])
    S.fullConfiguration = fullConfiguration
    
    S.solveSelfConsistency()
    print(np.round(np.real(S.fullConfiguration),4))
    S.calculateChi0(omega)

    
    

    
    Y = [np.imag(S.Chi0_inelastic[i,i,0,:]) for i in range(3)]
    Y.append(np.sum(Y,axis=0))
    Y = np.asarray(Y)
    for y,c,title in zip(Y,['b','r','g','k--'],['Jx','Jy','Jz','Jtot']):
        ax.plot(omega,y,c,label=title)
    ax.set_xlabel('Energy [meV]')
    ax.set_ylabel('Imag(X_0 inelastic)')
    ax.set_title('Magnetic Field = ('+', '.join(['{:}'.format(x) for x in S.magneticField])+') [T]')
    ax.legend()

fig.tight_layout()



##

hh = np.arange(0,2,0.05);

sqw=np.zeros((len(hh),len(omega)))
for hi,h in enumerate(hh):
    S.magneticField = np.array([0,0,h]);
    S.solveSelfConsistency()
    S.calculateChi0(omega)
    
    sqw[hi,:]=np.imag(np.sum(S.Chi0_inelastic[[0,1,2],[0,1,2],0,:],axis=0).T)
    

fig2,ax2 = plt.subplots()
p = ax2.pcolormesh(hh,omega,sqw.T,shading='auto')#;shading flat

ax2.set_xlabel('H (T)')
ax2.set_ylabel('Energy (meV)')
p.set_clim(0,500)
fig2.colorbar(p)



