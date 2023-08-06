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
    

#########
T=0.1#  in K
H=[0,0,0]#  in T

# plt.close('all')

S = 1/2
L = 1

Stevens = [PyCrystalField.LS_StevensOp(L,S,2,0),PyCrystalField.LS_StevensOp(L,S,2,-1),PyCrystalField.LS_StevensOp(L,S,2,1),
           ]

BV = [-1.5,0.6,0.6]

H_CEF = np.sum([SO*B for SO,B in zip(Stevens,BV)],axis=0)
LS_Coupling = -4# from Yokosuk et al. npj Quantum Materials (2020) 5:20 ; https://doi.org/10.1038/s41535-020-0224-6  -76.88/2.0


Sx = PyCrystalField.LSOperator.Sx(L,S).O
Sy = PyCrystalField.LSOperator.Sy(L,S).O
Sz = PyCrystalField.LSOperator.Sz(L,S).O
Lx = PyCrystalField.LSOperator.Lx(L,S).O
Ly = PyCrystalField.LSOperator.Ly(L,S).O
Lz = PyCrystalField.LSOperator.Lz(L,S).O

Jx = Sx + Lx
Jy = Sy + Ly
Jz = Sz + Lz

H_SOC = (Lx*Sx + Ly*Sy + Lz*Sz)*LS_Coupling
    
Hamiltonian = H_SOC+H_CEF

# eigenValues,eigenVectors = np.linalg.eig(Hamiltonian)
eigenValues,eigenVectors = np.linalg.eigh(Hamiltonian)

ev=eigenValues-np.min(eigenValues)
# h=kkk
# States used in calculations
states = 4

Hamiltonian-=np.eye(Hamiltonian.shape[0])*np.min(eigenValues)


#np.einsum('ik,ij,jl->kl',np.conj(eigenVectors[:,:states]),Hamiltonian,eigenVectors[:,:states])
# h=kkk
Hnew = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Hamiltonian,eigenVectors[:,:states]))#[:states,:states]

Jx = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jx,eigenVectors[:,:states]))#[:states,:states]
Jy = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jy,eigenVectors[:,:states]))
Jz = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jz,eigenVectors[:,:states]))

relevantStevens = [np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(SO,eigenVectors[:,:states])) for SO in Stevens]



operators = np.asarray([[Jx,Jy,Jz,*relevantStevens]])
energies = np.asarray([ev[:states]])


J1=-1.1484# 
J2=-0.1484# 
J3=0.1484# 


size =len([Jx,Jy,Jz,*relevantStevens])
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
omega=np.arange(6,11,epsilon/3)#
wid=0.1

Q1 = np.array([3.0,0.0,0.0])
Q2 = np.array([0.0,0.0,0.0])
Q3 = np.array([0.0,3.0,0.0])
Q4 = np.array([0.0,0.0,3.0])
Q5 = np.array([0.0,0.0,0.0])

dq = 61 # steps


Qs = [Q1,Q2,Q3,Q4,Q5]
QRLU = np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs,Qs[1:])])).T




positions = np.asarray([[0.5,0.5,0.5],
                        ])

lattice = Lattice(S=[1/2],g = [4/3],active = [1],positions = positions,
                  label = ['Dy1'], site = [1], lattice = [3.5,3.6,3.4,90,90,90])

S = System(temperature=T,magneticField=H, lattice=lattice)

S.lattice.generateCouplings(maxDistance = 3.61)


distances = [3.4,3.5,3.6]
Js = [J1S1,J2S1,J3S1]

S.lattice.addExchangeInteractions(Js,distances[:len(Js)])



S.operators  = np.asarray(operators).transpose(0,2,3,1)
S.energies = energies


# InitialDistributionSite1_Ext
sizeS = 1.5

Ncell = 4
nExt = [1,2,2]
numOperators = S.operators.shape[-1]
fullConfiguration = np.zeros((numOperators,len(S.lattice.r)*Ncell))

stateUp = np.zeros(numOperators)
stateDown = np.zeros(numOperators)

stateUp[2] = sizeS
stateDown[2] = -sizeS

states = np.asarray([1,-1, -1,1])#,   1,-1,-1, -1,1,1, -1,-1,1])

for i,state in enumerate(states):
    fullConfiguration[:,i] = (state==-1)*stateDown+(state==1)*stateUp

    
S.fullConfiguration = fullConfiguration

S.lattice.NCell = int(np.product(nExt))

S.lattice.nExt = nExt

## perform actual calculations
S.solveSelfConsistency()


S.calculateChi0(omega)

if True:
    III = np.imag(np.sum(S.Chi0_inelastic[[0,1,2],[0,1,2],0,:],axis=0).T)

    fig,ax = plt.subplots()

    ax.scatter(omega,III)
    ax.set_xlabel('Energy [meV]')
    ax.set_ylabel('Imag(Sum(Chi0))')
# h=kkk
S.calculateJQ(QRLU)



S.calculateChi()

S.calculateSperp()
## calculate prefactor from temperature as well as form factor 

prefactor = (1.0/(1-np.exp(-omega*Units.calculateKelvinToMeV(T)*Units.meV))).reshape(1,-1)  # shape (nQ,nE)

## Calculate Formfactor for Dysprosium... 

qLength = np.linalg.norm(S.QPoints,axis=1)


J = 3/2
Sval=1/2
L = 1

Sperp = S.Sperp

F2 = formFactor(qLength,J=J,S=Sval,L=L,ion='Dy2').reshape(-1,1)

Sperp*=F2*prefactor



## Do a Gaussian smearing of the data

sigmaE = 0.1/np.diff(omega[[1,0]])
sigmaQ = 0.05/np.linalg.norm(np.diff(S.QPoints[[1,0]],axis=0))


def generateTicsk(Qs,ticks=7):
    Qsegments = len(Qs)-1
    if Qsegments>=7:
        ticks = Qsegments
        tickPositions = np.linspace(0,Qsegments,ticks)
        ticks = ['\n'.join(['{:.2f}'.format(x) for x in Q]) for Q in Qs]
    
    else:
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

p = ax.pcolormesh(np.arange(QRLU.shape[-1])/dq,omega,Sperp.T,shading='auto')#I.T)
mi,ma = p.get_clim()

ax.axis('auto')
# fig.colorbar(p)
ax.set_xlabel('Q = (0,0,L) [rlu]')
ax.set_ylabel('Energy [meV]')


tickPositions,ticksLabels = generateTicsk(Qs,11)

ax.set_xticks(tickPositions)
ax.set_xticklabels(ticksLabels)
ax.set_title('H = '+','.join(['{:.0f}'.format(x) for x in H]))


ax = AX[1]
Qsteps = QRLU.shape[-1]
Qsegments = np.round(Qsteps/dq).astype(int)

tickPositions = np.arange(0,Qsegments+0.1)

p2 = ax.pcolormesh(np.arange(QRLU.shape[-1])/dq,omega,np.imag(np.sum(S.Chi_total[:,:,:3,:3],axis=(2,3))).T,shading='auto')#I.T)

mi,ma = np.min([mi,p2.get_clim()[0]]),np.max([ma,p2.get_clim()[1]])
ax.axis('auto')

ax.set_xlabel('Q = (0,0,L) [rlu]')
ax.set_ylabel('Energy [meV]')

tickPositions,ticksLabels = generateTicsk(Qs,11)

ax.set_xticks(tickPositions)
ax.set_xticklabels(ticksLabels)


p.set_clim(0.0,ma)
p2.set_clim(0.0,ma)

ax.set_title('TOTAL S H = '+','.join(['{:.0f}'.format(x) for x in H]))
stop = time.time()
print('Calculation done in {:.2f} s'.format(stop-start))
