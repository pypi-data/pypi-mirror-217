# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:09:10 2023

@author: lass_j
"""


import numpy as np
import matplotlib.pyplot as plt



from RPA import Lattice, System, Units, Coupling
from MagneticFormFactor import formFactor

from scipy.optimize import curve_fit

import PyCrystalField
# plt.close('all')


# Spin = 5/2
# z1 = 2
# z2 = 8


def MnF2(Q,J1=0.0354,J2=0.1499,D=0.131):
    Spin=5/2
    z1=2
    z2=8
    return np.sqrt(np.power(2*Spin*z2*J2+D+2*z1*Spin*J1*np.sin(Q[2,:]*np.pi)**2,2.0)-
            np.power(2*Spin*z2*J2*np.cos(Q[0]*np.pi)*np.cos(Q[1]*np.pi)*np.cos(Q[2]*np.pi),2.0))


def Gauss(x,A,mu,sigma,B):
    return A*np.exp(-np.power(x-mu,2.0)/(0.5*sigma**2))+B


Q1 = np.array([2.0,0.0,0.0])
Q2 = np.array([0.0,0.0,0.0])
Q3 = np.array([1.0,0.0,1.0])
Q4 = np.array([1.0,0.0,-1.0])

dq = 11#251#,1,51] # steps

Qs = [Q1,Q2,Q3,Q4]
QRLUChosen = np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs,Qs[1:])])).T

def MnF2Fitting(QRLU,J1,J2,D,verbose=False,plot=False):
    print(f'{J1=}, {J2=}, {D=}')
    T=0.01#  in K
    H=[0,0,0]#  in T
    
    Spin = 1/2
    # L = 0
    
    
    
    Sx = PyCrystalField.LSOperator.Sx(0,Spin).O
    Sy = PyCrystalField.LSOperator.Sy(0,Spin).O
    Sz = PyCrystalField.LSOperator.Sz(0,Spin).O
    
    
    
    
    
    operators  = np.asarray([Sx,Sy,Sz])
    # energies = np.zeros(len(operators[0]))


# J1 = 0.0354*5*2
# J2 = -0.1499*5*2*0.95
# D = 0.131#**2


    
    J1 *= 5*2
    J2 *= -5*2
    

    numberOfOperators = operators.shape[0]
    
    J1S1=np.zeros((numberOfOperators,numberOfOperators))
    J1S1[:3,:3]=J1*np.eye(3)
    
    J2S1=np.zeros((numberOfOperators,numberOfOperators))
    J2S1[:3,:3]=J2*np.eye(3)
    
    Ani = np.diag([-1,-1,2])*D/3.0#np.diag([-1,-1,2])*0.135/3#
    
    
    epsilon=0.15;
    omega=np.arange(epsilon,7.2,epsilon/6)#
    
    
    
    
    
    positions = np.asarray([[0.0,0.0,0.0],
                            [0.5,0.5,0.5]
                            ])
    
    SS = np.ones((len(positions)))*Spin
    
    lattice = Lattice(S=SS,g = np.full(len(SS),0.5),
                      active = np.ones_like(SS),positions = positions,
                      label = ['Ni2']*len(positions),
                      site = np.ones_like(SS),
                      lattice = [4.873,4.873,3.130,90,90,90]
                      )


    
    ### Rescale params
    
    
    # T=0.01#  in K
    S = System(temperature=T,magneticField=H, lattice=lattice)
    
    S.lattice.generateCouplings(maxDistance = 10.9)
    
    Js = [J1S1,J2S1]
    
    
    distances = [3.130,3.784480083181837]
    
    
    S.lattice.addExchangeInteractions(Js,distances,atol=0.001)
    
    
    
    ## Add anisotropy
    for i,pos in enumerate(S.lattice.r):
        exchange = Ani
        c = Coupling(i,i,pos,pos,np.asarray([0.0,0.0,0.0]),np.asarray([0.0,0.0,0.0]),0.0,exchange=exchange)
        S.lattice.couplings.append(c)
    
    
    
    S.operators = np.asarray([operators]).transpose(0,2,3,1)
    S.energies = np.asarray([[0.0,0.0]])
    
    
    # sizeS = Spin
    # doubling = False # Along c only
    # config = 1 # not sure
    Ncell = 1
    nExt = [1,1,Ncell]
    numOperators = S.operators.shape[-1]
    
    
    # plot = False
    
    
    stateUp = np.zeros((numberOfOperators))
    stateDown  = np.zeros((numberOfOperators))
    stateUp[2] = 1
    stateDown[2] = -1
    
    
    
    startStates = np.asarray([1,-1])
    
    fullConfiguration = np.zeros((numOperators,len(S.lattice.r)*Ncell))
    for i,state in enumerate(startStates ):
        fullConfiguration[:,i] = (state==-1)*stateDown+(state==1)*stateUp+0.1*(np.random.rand(fullConfiguration.shape[0])*2-1)




## Start of calculation

    
    
    S.fullConfiguration = fullConfiguration


    S.lattice.NCell = int(np.product(nExt))
    
    S.lattice.nExt = nExt
    
    S.fullConfiguration = fullConfiguration
    S.verbose=verbose
    S.solveSelfConsistency(limit=200)

    S.calculateChi0(omega)
    S.calculateJQ(QRLU)
    S.calculateChi(epsilon=1e-8)
    S.calculateSperp()
    
    
    # prefactor = (1.0/(1-np.exp(-omega*Units.calculateKelvinToMeV(T)*Units.meV))).reshape(1,-1)  # shape (nQ,nE)
    
    ## Calculate Formfactor
    
    # qLength = np.linalg.norm(S.QPoints,axis=1)
    
    
    # J = 4#15/2
    # Sval=1#5/2
    # L = 3
    
    Sperp = S.Sperp
    
    # F2 = formFactor(qLength,J=J,S=Sval,L=L,ion='Mn2').reshape(-1,1)#np.ones((nQ,1))
    
    # Sperp*=F2*prefactor
    
    
    
    ## Do a Gaussian smearing of the data
    
    # sigmaE = 0.1/np.diff(omega[[1,0]])
    # sigmaQ = 0.05/np.linalg.norm(np.diff(S.QPoints[[1,0]],axis=0))
    
    
    if plot:
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
    
    
    
    
    
    if plot:
        fig,AX = plt.subplots(ncols=2)
        
        ax = AX[0]
        
        Qsteps = QRLU.shape[-1]
        Qsegments = np.round(Qsteps/dq).astype(int)
        
        tickPositions = np.arange(0,Qsegments+0.1)
        
        p = ax.pcolormesh(np.arange(QRLU.shape[-1])/dq,omega,Sperp.T,shading='auto')#I.T)
        
        ECalc = MnF2(QRLU,J1=J1/(5*2),J2=-J2/(5*2),D=D)
        
        ax.EnergyPlot = ax.plot(np.arange(QRLU.shape[-1])/dq,ECalc,zorder=20,color='r')
        
        mi,ma = p.get_clim()
        
        ax.axis('auto')
        # fig.colorbar(p)
        ax.set_xlabel('Q = (0,0,L) [rlu]')
        ax.set_ylabel('Energy [meV]')
        
        
        tickPositions,ticksLabels = generateTicsk(Qs,14)
    
        ax.set_xticks(tickPositions)
        ax.set_xticklabels(ticksLabels)
        ax.set_title('H = '+','.join(['{:.0f}'.format(x) for x in H]))
        
        
        
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
    
    
    else:
        # chisq = 0
        CalulatedE = MnF2(QRLU,J1=J1/(5*2),J2=-J2/(5*2),D=D)
        pos = []
        for Q,I,T in zip(QRLU.T,Sperp,CalulatedE):
            
            EIdx = np.argmin(np.abs(T-omega))
            
            guess = [I[EIdx],omega[EIdx],0.1,0.0]
            
            
            params,errs = curve_fit(Gauss,omega,I,p0=guess)
            pos.append(params[1])
            # chisq+=np.power(T-params[1],2)
            
        return np.asarray(pos)






J1 = 0.0354
J2 = 0.1499
D = 0.131



J1Fitted, J2Fitted, DFitted = 0.03540209, 0.14992922, 0.13096674

startGuess = np.asarray([J1,J2,D])

ECalc = MnF2(QRLUChosen,J1,J2,D)

parameters,errors = curve_fit(MnF2Fitting,QRLUChosen,ECalc,p0=startGuess)






Q1 = np.array([2.0,0.0,0.0])
Q2 = np.array([0.0,0.0,0.0])
Q3 = np.array([1.0,0.0,1.0])
Q4 = np.array([1.0,0.0,-1.0])

dq = 251#251#,1,51] # steps

Qs = [Q1,Q2,Q3,Q4]
QRLUChosen = np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs,Qs[1:])])).T

MnF2Fitting(QRLUChosen,*parameters,verbose=True,plot=True)



    