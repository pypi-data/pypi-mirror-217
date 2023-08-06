# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:08:55 2023

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
import PyCrystalField

    
import time

start = time.time()
# plt.ioff()

#########
T=0.1#  in K
H=[0,0,5]#  in T

# plt.close('all')

Sval = 1/2

L = 1

Stevens = [PyCrystalField.LS_StevensOp(L,Sval,2,0),PyCrystalField.LS_StevensOp(L,Sval,2,-1),PyCrystalField.LS_StevensOp(L,Sval,2,1),
           ]

BV = [300.5,0.6,0.6]

H_CEF = np.sum([SO*B for SO,B in zip(Stevens,BV)],axis=0)
# LS_Coupling = -4# from Yokosuk et al. npj Quantum Materials (2020) 5:20 ; https://doi.org/10.1038/s41535-020-0224-6  -76.88/2.0


Sx = PyCrystalField.LSOperator.Sx(L,Sval).O
Sy = PyCrystalField.LSOperator.Sy(L,Sval).O
Sz = PyCrystalField.LSOperator.Sz(L,Sval).O
Hamiltonian = H_CEF

eigenValues,eigenVectors = np.linalg.eigh(Hamiltonian)

ev=eigenValues-np.min(eigenValues)

# States used in calculations
states = len(ev) # All states

Hamiltonian-=np.eye(Hamiltonian.shape[0])*np.min(eigenValues)


Hnew = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Hamiltonian,eigenVectors[:,:states]))#[:states,:states]

# Jx = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jx,eigenVectors[:,:states]))#[:states,:states]
# Jy = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jy,eigenVectors[:,:states]))
# Jz = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jz,eigenVectors[:,:states]))
Sx = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Sx,eigenVectors[:,:states]))#[:states,:states]
Sy = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Sy,eigenVectors[:,:states]))
Sz = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Sz,eigenVectors[:,:states]))

# relevantStevens = [np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(SO,eigenVectors[:,:states])) for SO in Stevens]



operators = np.asarray([[Sx,Sy,Sz]])#Jx,Jy,Jz,*relevantStevens]])
energies = np.asarray([ev[:states]])


J1=-1.1484# 
J2=-0.1484# 
J3=0.1484# 


size =len(operators[0])
J1S1=np.zeros((size,size))
J1S1[:3,:3]=J1*np.eye(3)

J2S1=np.zeros_like(J1S1)
J2S1[:3,:3]=J2*np.eye(3)#*0.0

J3S1=np.zeros_like(J1S1)
J3S1[:3,:3]=J3*np.eye(3)#*0.0

# 'Jx'    'Jy'    'Jz'    'O20'    'O2+1'    'O2-1'    'O2+2'    'O2-2'
#   1       2      3        4        5         6         7          8
#J2S1[4,4]=facO21;

##
epsilon=0.05;
omega=np.arange(0,10,epsilon/3)#
# wid=0.1

# Q1 = np.array([3.0,0.0,0.0])
# Q2 = np.array([0.0,0.0,0.0])
# Q3 = np.array([0.0,3.0,0.0])
Q4 = np.array([0.0,0.0,0.0])
Q5 = np.array([0.0,0.0,3.0])

dq = 121 # steps

# ElasticThreshold=1e-2
# Qz= np.concatenate([np.linspace(1.5,1.5,20),np.linspace(1.5,6,20)])


# Qy=np.zeros_like(Qz)#((len(Qz)))
# Qx=np.concatenate([np.linspace(-3,0,20),np.linspace(0,0,20)])#np.ones_like(Qz)*0.0#Qz#
# # Qz=

Qs = [#Q1,Q2,Q3,
      Q4,Q5]
QRLU = np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs,Qs[1:])])).T




positions = np.asarray([[0.5,0.5,0.5],
                        ])

lattice = Lattice(S=[1/2],g = [4/3],active = [1],positions = positions,
                  label = ['Dy1'], site = [1], lattice = [3.5,3.6,3.4,90,90,90])

S = System(temperature=T,magneticField=H, lattice=lattice)

S.lattice.generateCouplings(maxDistance = 3.61)





# h=kkk



distances = [3.4,3.5,3.6]
Js = [J1S1,J2S1,J3S1]

S.lattice.addExchangeInteractions(Js,distances[:len(Js)])







# S.operators = [Jx,Jy,Jz,#loadmat(r'C:\Users\lass_j\Documents\Software\RPA\RPA for Simon\operators\operatorsDySite1_1XM_O2.mat')['operator']
S.operators  = np.asarray(operators).transpose(0,2,3,1)
S.energies = energies



# InitialDistributionSite1_Ext
sizeS = 1.5

Ncell = 2
nExt = [1,1,2]
numOperators = S.operators.shape[-1]
fullConfiguration = np.zeros((numOperators,len(S.lattice.r)*Ncell))

stateUp = np.zeros(numOperators)
stateDown = np.zeros(numOperators)

stateUp[2] = sizeS
stateDown[2] = -sizeS

states = np.asarray([1,-1])# -1,1])#,   1,-1,-1, -1,1,1, -1,-1,1])

for i,state in enumerate(states):
    fullConfiguration[:,i] = (state==-1)*stateDown+(state==1)*stateUp

    
S.fullConfiguration = fullConfiguration

S.lattice.NCell = int(np.product(nExt))

S.lattice.nExt = nExt

## perform actual calculations
S.solveSelfConsistency()

# h=kkk

S.calculateChi0(omega)

# III = np.imag(np.sum(S.Chi0_inelastic[[0,1,2],[0,1,2],0,:],axis=0).T)

# fig,ax = plt.subplots()

# ax.scatter(omega,III)

# h=kkk
S.calculateJQ(QRLU)



S.calculateChi()

S.calculateSperp()
## calculate prefactor from temperature as well as form factor 

prefactor = (1.0/(1-np.exp(-omega*Units.calculateKelvinToMeV(T)*Units.meV))).reshape(1,-1)  # shape (nQ,nE)

## Calculate Formfactor for Dysprosium... 

qLength = np.linalg.norm(S.QPoints,axis=1)


J = 3/2
# Sval=1/2
L = 1

Sperp = S.Sperp

# F2 = formFactor(qLength,J=J,S=Sval,L=L,ion='Dy2').reshape(-1,1)#np.ones((nQ,1))

# Sperp*=F2*prefactor



## Do a Gaussian smearing of the data

sigmaE = 0.1/np.diff(omega[[1,0]])
sigmaQ = 0.05/np.linalg.norm(np.diff(S.QPoints[[1,0]],axis=0))


# I = gaussian_filter(Sperp,[sigmaQ,sigmaE],mode='constant',cval=0)


def generateTicsk(Qs,ticks=7):
    Qsegments = len(Qs)-1
    if Qsegments>=7:
        ticks = Qsegments
        tickPositions = np.linspace(0,Qsegments,ticks)
        ticks = ['\n'.join(['{:.2f}'.format(x) for x in Q]) for Q in Qs]
    
    else:
        #tickPositions = np.linspace(0,Qsegments,totalTicks)
        ticksPerQSegment = int(np.round((ticks-2)/Qsegments))
        
        
        tickPositions = np.concatenate([*[np.arange(0,1,1/ticksPerQSegment)+I for I in range(Qsegments)],[Qsegments]])
        QRLUTickPositions = np.concatenate([*np.asarray([np.linspace(q1,q2,ticksPerQSegment+1)[:-1] for q1,q2 in zip(Qs,Qs[1:])]),[Qs[-1].T]])
        ticks = ['\n'.join(['{:.2f}'.format(x) for x in Q]) for Q in QRLUTickPositions]
    return tickPositions,ticks




fig,AX = plt.subplots(nrows=2)

ax = AX[0]

Qsteps = QRLU.shape[-1]
Qsegments = np.round(Qsteps/dq).astype(int)

tickPositions = np.arange(0,Qsegments+0.1)

ax.p = ax.pcolormesh(np.arange(QRLU.shape[-1])/dq,omega,Sperp.T,shading='auto')#I.T)
mi,ma = ax.p.get_clim()

ax.axis('auto')
# fig.colorbar(p)
# ax.set_xlabel('Q = (0,0,L) [rlu]')
ax.set_ylabel('Energy [meV]')


tickPositions,ticksLabels = generateTicsk(Qs,11)

ax.set_xticks(tickPositions)
ax.set_xticklabels(ticksLabels)
ax.set_title('H = '+','.join(['{:.0f}'.format(x) for x in H])+' S = {:.1f}'.format(Sval))


# p.set_clim(0,10)
ax2 = AX[1]
Qsteps = QRLU.shape[-1]
Qsegments = np.round(Qsteps/dq).astype(int)

tickPositions = np.arange(0,Qsegments+0.1)

ax2.p2 = ax2.pcolormesh(np.arange(QRLU.shape[-1])/dq,omega,np.imag(np.sum(S.Chi_total[:,:,:3,:3],axis=(2,3))).T,shading='auto')#I.T)

mi,ma = np.min([mi,ax2.p2.get_clim()[0]]),np.max([ma,ax2.p2.get_clim()[1]])
ax2.axis('auto')
# fig.colorbar(p)
# ax.set_xlabel('Q = (0,0,L) [rlu]')
ax2.set_ylabel('Energy [meV]')

tickPositions,ticksLabels = generateTicsk(Qs,11)

ax2.set_xticks(tickPositions)
ax2.set_xticklabels(ticksLabels)

ma = 100
ax.p.set_clim(0.0,ma)
ax2.p2.set_clim(0.0,ma)

ax2.set_title('TOTAL S H = '+','.join(['{:.0f}'.format(x) for x in H]))

    
stop = time.time()
print('Calculation done in {:.2f} s'.format(stop-start))
