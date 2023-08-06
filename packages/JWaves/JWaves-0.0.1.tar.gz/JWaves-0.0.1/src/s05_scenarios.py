# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:49:33 2023

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


def s05_scenarios(J1,J2,O21a,O21b,dipole,levels,ax=None):
# if True:
    # J1 = -0.005
    # J2=0.0
    # O21a=0
    # O21b=0
    # dipole=False
    # levels=True
    # ax = None
    # lat=[10.088,11.943,3.42];
    
    # ConvergenceCriteria=0.05
    T=0.1; # in K
    H=[0,0,0]; # in T
    # maxDistance=3.51;
    
    
    # operators='/home/l_mc01/mpi/gauthier/GauthierPark/RPA/operators/operatorsSHO_sxtal0p45.mat';
    # operators=r'C:\Users\lass_j\Documents\Software\RPA\RPA for Simon\operators\operatorsSHO_sxtal0p45.mat';
    
    ##
    
    J1S1=np.zeros((8,8));
    J1S1[:3,:3]=J1*np.eye(3);
    
    J2S1=np.zeros((8,8));
    J2S1[:3,:3]=J2*np.eye(3);
    
    # 'Jx'    'Jy'    'Jz'    'O20'    'O2+1'    'O2-1'    'O2+2'    'O2-2'
    #   1       2      3        4        5         6         7          8
    J1S1[5,4]=O21a;
    J1S1[4,5]=O21a;
    
    J2S1[4,5]=O21b;
    J2S1[5,4]=O21b;
    ##
    epsilon=0.03;
    omega=np.arange(0.1,4.5,epsilon/3);
    # wid=0.1;
    ElasticThreshold=1e-2;
    
    Qz=np.arange(-0.5,1.5,0.075)
    #Qz=-0.5:0.075:0.5;
    ##
    
    Qy=np.zeros((len(Qz)))
    Qx=np.zeros((len(Qz)))+2
    Q=np.array([Qx+2,Qy,Qz])
    
    
    positions = np.asarray([[0.4242,0.1110,0.25],
                            [0.5758,0.8890,0.75],
                            [0.0758,0.6110,0.75],
                            [0.9242,0.3890,0.25]])
    
    lattice = Lattice(S=[15/2,15/2,15/2,15/2],g = [4/3,4/3,4/3,4/3],active = [1,1,1,1],positions = positions,
                      label = ['Dy1','Dy1','Dy1','Dy1'], site = [1,1,1,1], lattice = [10.0884,11.9427,3.4289,90,90,90])#,
                      #equivalence=[1,3,2,4])
    
    S = System(temperature=T,magneticField=H, lattice=lattice)
    
    S.lattice.generateCouplings(maxDistance = 3.53)
    
    # h=kkk
    S.lattice.NCell = 1
    S.lattice.nExt = [1,1,1]
    
    distances = [3.5082,3.4289]
    Js = [J1S1,J2S1]
    
    S.lattice.addExchangeInteractions(Js,distances)
    if dipole:
        S.lattice.buildDipolarInteractionMatrix()
    
    S.operators = np.asarray([loadmat(r'C:\Users\lass_j\Documents\Software\RPA\RPA for Simon\operators\operatorsSHO_sxtal0p45.mat')['operator']])
    
    S.energies = np.array([[0,0.626,1.7,3.5,5.36,8.22]])
    # if levels:
    #     S.energies = np.array([0,0.626,1.7,3.5,5.36,8.22])
    # else:
    #     S.energies = np.array([0,0.626,2.12,3.07,5.36,8.22])
    
    
    
    #InitialDistributionSite1_2zigzag()
    S.verbose = False
    
    fullConfiguration = np.zeros((S.operators.shape[-1],4))
    
    fullConfiguration[2] = 3.9892
    fullConfiguration[2,1:3]*=-1
    
    S.solveSelfConsistency(fullConfiguration=fullConfiguration)
    
    S.calculateChi0(omega,ElasticThreshold=ElasticThreshold)
    
    S.calculateJQ(Q)
    
    S.verbose = True
    S.calculateChi()
    
    
    S.calculateSperp()
    
    Sperp = S.Sperp
    
    
    prefactor = (1.0/(1-np.exp(-omega*Units.calculateKelvinToMeV(T)*Units.meV))).reshape(1,-1)  # shape (nQ,nE)

    
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
    
    F2 = formFactor(qLength,A=A,a=a,B=B,b=b,C=C,c=c,D=D,
                    Ap=Ap,ap=ap,Bp=Bp,bp=bp,Cp=Cp,cp=cp,Dp=Dp,
                    J=J,S=Sval,L=L).reshape(-1,1)#np.ones((nQ,1))
    
    Sperp*=F2*prefactor
    
    
    
    ## Do a Gaussian smearing of the data
    
    sigmaE = 0.5/np.diff(omega[[1,0]])
    sigmaQ = 0.0/np.linalg.norm(np.diff(S.QPoints[[1,0]],axis=0))
    
    
    I = gaussian_filter(Sperp,[sigmaQ,sigmaE],mode='constant',cval=0)
    
    if ax is None:
        fig,ax = plt.subplots()
    ax.p = ax.pcolormesh(Q[2],omega,I.T,shading='auto')#I.T)
    ax.axis('auto')
    #ax.get_figure().colorbar(p)
    ax.set_xlabel('Q = (0,0,L) [rlu]')
    ax.set_ylabel('Energy [meV]')
    ax.p.set_clim(0,600)


# else:

fig,AX = plt.subplots(nrows=4,ncols=2)
Ax = AX.flatten()

parameters = [{'J1':-0.005,'J2':0.0,'O21a':0,'O21b':0,'dipole':False,'levels':True},
              {'J1':0.0,'J2':0.005,'O21a':0,'O21b':0,'dipole':False,'levels':True},
              {'J1':-0.0025,'J2':0.0025,'O21a':0,'O21b':0,'dipole':False,'levels':True},
              {'J1':0.0,'J2':0.0,'O21a':0,'O21b':0,'dipole':True,'levels':True},
              {'J1':-0.003,'J2':-0.003,'O21a':0,'O21b':0,'dipole':True,'levels':True},
              {'J1':-0.003,'J2':-0.003,'O21a':0,'O21b':0.0004,'dipole':True,'levels':True},
              {'J1':-0.003,'J2':-0.003,'O21a':0.0002,'O21b':0.0004,'dipole':True,'levels':True},
              ]

titles = ['A: J_1 = -0.005','B: J_2=0.005','C: J_1=J_2=-0.0025','D: Dipolar',
          'E: Dipolar, J_1=J_2=-0.003','F:  Dipolar, J_1=J_2=-0.003,O21a',
          'G:  Dipolar, J_1=J_2=-0.003,O21a,O21b']

for par,ax,title in zip(parameters,Ax,titles):
    print(title,':')
    s05_scenarios(**par,ax=ax)
    
    ax.set_title(title)
    
fig.tight_layout()



