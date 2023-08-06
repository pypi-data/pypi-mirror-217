# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:09:10 2023

@author: lass_j
"""


import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('.')
from RPA import Lattice, System, Units, Coupling
from MagneticFormFactor import formFactor

def MnF2(Q,J1=0.0354,J2=0.1499,D=0.131,Spin=5/2):
        
        z1=2
        z2=8
        return np.sqrt(np.power(2*Spin*z2*J2+D+2*z1*Spin*J1*np.sin(Q[2,:]*np.pi)**2,2.0)-
                np.power(2*Spin*z2*J2*np.cos(Q[0]*np.pi)*np.cos(Q[1]*np.pi)*np.cos(Q[2]*np.pi),2.0))
import PyCrystalField
# plt.close('all')

T=0.01#  in K
H=[0,0,0]#  in T

S = 1/2
STrue = 5/2 #5/2
L = 0

# plt.ioff()




Sx = PyCrystalField.LSOperator.Sx(0,S).O
Sy = PyCrystalField.LSOperator.Sy(0,S).O
Sz = PyCrystalField.LSOperator.Sz(0,S).O





operators  = np.asarray([Sx,Sy,Sz])
energies = np.zeros(len(operators[0]))


# z1 = 2
# z2 = 8

J1Yamani = 0.0354
J2Yamani = 0.1499
DdYamani = 0.131

spinFactor = (STrue/S)



changeFactor = 2*spinFactor#0.5*F*(spinFactor)**2

J1 = 0.5*changeFactor*J1Yamani#/2.5
J2 = -changeFactor*J2Yamani#*5**2#/2.5#*25/4#*np.sqrt(5*7/4)#np.sqrt(35)
# J3 = -0.5
# J4 = -0.5



# facO21=0# 


numberOfOperators = operators.shape[0]

J1S1=np.zeros((numberOfOperators,numberOfOperators))
J1S1[:3,:3]=J1*np.eye(3)

J2S1=np.zeros((numberOfOperators,numberOfOperators))
J2S1[:3,:3]=J2*np.eye(3)


Ani = np.diag([0.0,0.0,1.0])*DdYamani#/3.0#/2.5#np.diag([-1,-1,2])*0.135/3#

# Ani = 0.5*0.5*changeFactor




Q1 = np.array([2.0,0.0,0.0])
Q2 = np.array([0.0,0.0,0.0])
Q3 = np.array([1.0,0.0,1.0])
Q4 = np.array([1.0,0.0,-1.0])

dq = 101#,1,51] # steps

Qs = [Q1,Q2,Q3,Q4]
# Qs = [Q3,Q4]
QRLU = np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs,Qs[1:])])).T


EMax = np.max(MnF2(QRLU,J1=J1Yamani,J2=J2Yamani,D=DdYamani,Spin=STrue))*1.1
##
epsilon=0.15;
omega=np.arange(epsilon,EMax,epsilon/6)#

# QQS = [[Q1,Q2],[Q3,Q4]]
# QRLU = []
# for Qs  in QQS:#[Q1,Q2,Q3,Q4]
#     QRLU.append(np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs,Qs[1:])])))

# QRLU = np.concatenate(QRLU).T



# z1 = 0.5015
# z2 = 0.2081
# z3 = 0.0088  

# z1 = 0.5015  
# z2 = 0.2081  
# z3 = 0.0088  
positions = np.asarray([[0.0,0.0,0.0],
                        [0.5,0.5,0.5]
                        # [2/3,1/3,z1+1/3],
                        # [1/3,2/3,z1+2/3-1],
                        
                        # [0.0,0.0,z2],
                        # [2/3,1/3,z2+1/3],
                        # [1/3,2/3,z2+2/3],
                        
                        # [0.0,0.0,z3],
                        # [2/3,1/3,z3+1/3],
                        # [1/3,2/3,z3+2/3],
                        ])

SS = np.ones((len(positions)))#[1,1,1, 1,1,1, 1,1,1]

lattice = Lattice(S=SS,g = np.full(len(SS),STrue),
                  active = np.ones_like(SS),positions = positions,
                  label = ['Ni2']*len(positions),#,'Ni2','Ni2', 'Ni2','Ni2','Ni2', 'Ni2','Ni2','Ni2'], 
                  site = np.ones_like(SS),#[1,1,1, 1,1,1, 1,1,1], 
                  lattice = [4.873,4.873,3.130,90,90,90],#np.array([[5.15343,0.0,0.0],
                            #          [-5.1534*np.cos(2*np.pi/3)*0,5.15343,0.0],#*np.sin(2*np.pi/3.0),0.0],
                            #         [0.0,0.0,13.89103]]),
                  #equivalence=[0,0,0,1,1,1,2,2,2]#2,3,4,5,6,7,8,9]
                  )

# A = np.array([[5.15343,0.0,0.0],
#              [-5.1534*np.cos(2*np.pi/3),5.1534*np.sin(2*np.pi/3.0),0.0],
#             [0.0,0.0,13.89103]])

# A = np.asarray([5.15343,5.15343,13.89103])
S = System(temperature=T,magneticField=H, lattice=lattice)

S.lattice.generateCouplings(maxDistance = 3.8)
# 
# h = kkk

Js = [J1S1,J2S1]#,J1S1,J3S1,J4S1]


distances = [3.130,3.784480083181837]#, 3.0266, 3.5099,3.70855]

# nonzero = np.asarray([[j,d] for j,d in zip(Js,distances) if not np.all(np.isclose(j,0.0))]).T


S.lattice.addExchangeInteractions(Js,distances,atol=0.001,labels=['J1','J2'])



## Add anisotropy
for i,pos in enumerate(S.lattice.r):
    exchange = Ani
    c = Coupling(i,i,pos,pos,np.asarray([0.0,0.0,0.0]),np.asarray([0.0,0.0,0.0]),0.0,exchange=exchange,label='Ani')
    S.lattice.couplings.append(c)




# h=kkk

# threeByThreeOperators = np.asarray([threeByThreeOperators[0],threeByThreeOperators[1],threeByThreeOperators[2],
                       # ])

# h=kkk

S.operators = np.asarray([operators]).transpose(0,2,3,1)



S.energies = np.asarray([[0.0,0.0]])#np.zeros((1,S.operators.shape[1]))#np.asarray([ev[:states] for ev in energies])

# S.energies = np.asarray([[0.0,Ani[2,2],Ani[2,2]*200,Ani[2,2]*200,Ani[2,2],0.0]])
# h=kk

# InitialDistributionSite1_Ext
sizeS = 1
doubling = False # Along c only
config = 1 # not sure
Ncell = 1
nExt = [1,1,Ncell]
numOperators = S.operators.shape[-1]


plot = False



stateUp = np.zeros((numberOfOperators))
stateDown  = np.zeros((numberOfOperators))
stateUp[2] = 0.5#STrue
stateDown[2] = -0.5



startStates = np.asarray([1,-1])#np.asarray([-1,1,1, 1,-1,1, 1,-1,1,      1,-1,-1, -1,1,-1, -1,1,-1])#,   1,-1,-1, -1,1,1, -1,-1,1])

fullConfiguration = np.zeros((numOperators,len(S.lattice.r)*Ncell))
for i,state in enumerate(startStates ):
    fullConfiguration[:,i] = (state==-1)*stateDown+(state==1)*stateUp#+0.1*(np.random.rand(fullConfiguration.shape[0])*2-1)


if plot:
    ax = plt.figure().add_subplot(projection='3d')
    
    # ax.scatter3D(*np.einsum('ij,...j->i...',S.lattice.A.T,S.lattice.r),c = fullConfiguration[2,:])
    
    
    positions = np.asarray([[np.dot(S.lattice.A,x+np.asarray([0,0,c])) for x in S.lattice.r for c in [0]]]).T.reshape(3,-1)
    # [ax.scatter3D(*x.T) for x in positions.reshape(3,-1,3).transpose(1,2,0)]#,c = fullConfiguration[2,:]>0.0)
    ax.scatter3D(*positions ,c = fullConfiguration[2,:positions.shape[-1]]>0.0)
    
    colours = ['r','b','k']
    labelsUsed = []
    for coupling in S.lattice.couplings:
        #line = np.asarray([S.lattice.r[coupling.atom1],S.lattice.r[coupling.atom2]]).T
        try:
            if np.sum(np.abs(coupling.exchange))<0.01:
                continue
        except:
            pass
        line = np.asarray([positions[:,coupling.atom1],positions[:,coupling.atom2]]).T
        line[:,1]+=np.dot(S.lattice.A,coupling.dl)
        
        try:
            if np.isclose(coupling.exchange[0,0],J1):
                c = 'r'
                label = 'J1'
            elif np.isclose(coupling.exchange[0,0],J2):
                c = 'b'
                label = 'J2'
            elif np.isclose(coupling.exchange[0,0],J3):
                c = 'm'
                label = 'J3'
            else:
                c = 'k'
                label = 'J4'
        except:
            c = 'k'
            label = '_'
            
        if label in labelsUsed:
            label = '_'+label
        else:
            labelsUsed.append(label)
        ax.plot3D(*line,c=c,label=label)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    # h=kkk


S.fullConfiguration = fullConfiguration


S.lattice.NCell = int(np.product(nExt))

S.lattice.nExt = nExt
# h = KKK

if False:
    temperatures = [5,50]#[300,100,50,30,20,5]
    
    
    n = int(np.ceil(np.sqrt(len(temperatures))))
    m = int(np.ceil(len(temperatures)/n))
    
    # fig,AX =  plt.subplots(nrows=m,ncols=n)
    # try:
    #     AX = AX.flatten()
    # except:
    #     AX=[AX]
        
    S.verbose = True
    CEF = []
    for T,ax in zip(temperatures,np.ones_like(temperatures)):#[1]):
        # perform actual calculations
        S.temperature = T
        
        S.fullConfiguration = fullConfiguration
        S.fullConfiguration[:3]+=np.random.rand(3, S.fullConfiguration.shape[-1])*0.01
        S.solveSelfConsistency(limit=100)
        
        S.calculateChi0(omega)
            
        
        cef = np.sum(np.imag(S.Chi0_inelastic[:3,:3]),axis=(0,1))
        CEF.append(cef)
        # ax.scatter(omega,np.sum(cef,axis=0))
        # ax.set_xlabel('Omega [meV]')
        # ax.set_ylabel('Imag(Chi)')
        # ax.set_title('T = {:.0f} K'.format(T))
        #h=kkk
        
        if False:
            fig,AX = plt.subplots(nrows=4,ncols=5)
            Ax = AX.flatten()
            # fig,AX2 = plt.subplots(nrows=4,ncols=5)
            # Ax2 = AX2.flatten()
            
            for i,ax in zip(range(18),Ax):
                ax.I = ax.imshow(np.real(S.Chi0_elastic[:3,:3,i]))
            # for i,ax in zip(range(18),Ax2):
                # ax.I = ax.imshow(np.imag(S.Chi0_elastic[:3,:3,i]))
                
            for ax in Ax[:18]:
                ax.I.set_clim(0,10)
                
    fig,ax = plt.subplots()
    [ax.plot(omega,cef.sum(axis=0),label = label) for cef,label in zip(CEF,temperatures)]
    
    ax.set_xlabel('Omega [meV]')
    ax.set_ylabel('Imag(Chi)')
    ax.legend()
else:
    S.fullConfiguration = fullConfiguration
    # S.fullConfiguration[:3]+=np.random.rand(3, S.fullConfiguration.shape[-1])*0.01
    S.solveSelfConsistency(limit=200)
    
    S.calculateChi0(omega)
# h=kkk
        
        # for i,ax in zip(range(18),Ax2):
            # ax.I = ax.pcolormesh(np.imag(S.Chi0_inelastic[2,2,:,i]))
        # for ax in Ax2[:18]:
            # ax.I.set_clim(0,10)
    
S.calculateJQ(QRLU)

S.calculateChi(epsilon=1e-8)

S.calculateSperp()
## calculate prefactor from temperature as well as form factor 

prefactor = (1.0/(1-np.exp(-omega*Units.calculateKelvinToMeV(T)*Units.meV))).reshape(1,-1)  # shape (nQ,nE)

## Calculate Formfactor

qLength = np.linalg.norm(S.QPoints,axis=1)


# J = 4#15/2
# Sval=1#5/2
# L = 3

Sperp = S.Sperp

# F2 = formFactor(qLength,J=J,S=Sval,L=L,ion='Ni2').reshape(-1,1)#np.ones((nQ,1))

# Sperp*=F2*prefactor



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
        #tickPositions = np.linspace(0,Qsegments,totalTicks)
        ticksPerQSegment = int(np.round((ticks-2)/Qsegments))
        
        
        tickPositions = np.concatenate([*[np.arange(0,1,1/ticksPerQSegment)+I for I in range(Qsegments)],[Qsegments]])
        QRLUTickPositions = np.concatenate([*np.asarray([np.linspace(q1,q2,ticksPerQSegment+1)[:-1] for q1,q2 in zip(Qs,Qs[1:])]),[Qs[-1].T]])
        ticks = ['\n'.join(['{:.2f}'.format(x) for x in Q]) for Q in QRLUTickPositions]
    return tickPositions,ticks

# def multiTicks(QQS,totalTicks =)

if True:
    fig,AX = plt.subplots(ncols=2)
    
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
    
    
    tickPositions,ticksLabels = generateTicsk(Qs,14)

    ax.set_xticks(tickPositions)
    ax.set_xticklabels(ticksLabels)
    ax.set_title('H = '+','.join(['{:.0f}'.format(x) for x in H]))
    
    
    # p.set_clim(0,10)
    ax = AX[1]
    Qsteps = QRLU.shape[-1]
    Qsegments = np.round(Qsteps/dq).astype(int)
    
    tickPositions = np.arange(0,Qsegments+0.1)
    
    ITotal = np.einsum('...ii->...',np.imag(S.Chi_total[:,:,:3,:3]))
    
    p2 = ax.pcolormesh(np.arange(QRLU.shape[-1])/dq,omega,ITotal.T,shading='auto')#I.T)
    
    mi,ma = np.min([mi,p2.get_clim()[0]]),np.max([ma,p2.get_clim()[1]])
    ax.axis('auto')
    fig.colorbar(p)
    ax.set_xlabel('Q = (0,0,L) [rlu]')
    ax.set_ylabel('Energy [meV]')
    
    tickPositions,ticksLabels = generateTicsk(Qs,14)

    ax.set_xticks(tickPositions)
    ax.set_xticklabels(ticksLabels)
    
    ma = 15
    
    p.set_clim(0.0,ma)
    p2.set_clim(0.0,ma)
    
    ax.set_title('TOTAL S H = '+','.join(['{:.0f}'.format(x) for x in H]))



    
    
    
    
    ECalc = MnF2(QRLU,J1=J1Yamani,J2=J2Yamani,D=DdYamani,Spin=STrue)
    ax.plot(np.arange(QRLU.shape[-1])/dq,ECalc,color='r')
    
    
    
    
ps = []

fig,AX = plt.subplots(ncols=3,nrows=3)
AX = AX.flatten()

idxesX,idxesY = np.asarray(np.meshgrid(np.arange(3),np.arange(3)))
idxesX = idxesX.flatten()
idxesY = idxesY.flatten()
# Title = ['Sxx','Syy','Szz','Sxy','Sxz','Syz',]

coordinate='xyz'

Title = ['S{}{}'.format(coordinate[idx1],coordinate[idx2]) for idx1,idx2 in zip(idxesX,idxesY)]

for idx1,idx2,ax,title in zip(idxesX,idxesY,AX,Title):

    Qsteps = QRLU.shape[-1]
    Qsegments = np.round(Qsteps/dq).astype(int)
    
    tickPositions = np.arange(0,Qsegments+0.1)
    
    
    ChiAlongQ =  QRLU/np.linalg.norm(QRLU,axis=0)
    
    ITotal = np.imag(S.Chi_total[:,:,idx1,idx2])#np.einsum('ijkk,ik->ij',np.imag(S.Chi_total[:,:,:3,:3]),ChiAlongQ.T)
    
    # ITotal = np.einsum('...ii->...',np.imag(S.Chi_total[:,:,:3,:3]))
    
    ps.append(ax.pcolormesh(np.arange(QRLU.shape[-1])/dq,omega,ITotal.T,shading='auto'))#I.T))
    
    
    ax.axis('auto')
    
    ax.set_xlabel('Q  [rlu]')
    ax.set_ylabel('Energy [meV]')
    
    tickPositions,ticksLabels = generateTicsk(Qs,14)
    
    ax.set_xticks(tickPositions)
    ax.set_xticklabels(ticksLabels)
    
    # ma = 15
    
    # p.set_clim(0.0,ma)
    # p2.set_clim(0.0,ma)
    
    ax.set_title(title+' H = '+','.join(['{:.0f}'.format(x) for x in H]))