# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:41:31 2023

@author: lass_j
"""
try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

import sys
sys.path.append('.')

import PyCrystalField
from RPA import Lattice, System, Units, conversionMatrix, Coupling
from MagneticFormFactor import formFactor
from scipy.ndimage import gaussian_filter


    
# import time

# start = time.time()
    

#########
# lat=[10.088,11.943,3.42]# 


from os.path import split, join

import PyCrystalField
import matplotlib.pyplot as plt
# plt.close('all')
import numpy as np


ions = ['Ni1','Ni2','Ni3']
cif = 'C:/Users/lass_j/Documents/Ni3TeO6/TemperatureCIF/Ni3TeO6_15K.cif'



    
# eigenEnergies = []
# eigenVectors = []

# def commu(A,B):
#     return (np.dot(A,B)+np.dot(B,A))*0.5



L = 3
S = 1
operators = []
energies = []

BValues = [[-2.289846167405785,1.4504090674792935,-0.286922176815416,-9.68697028772953], # B20, B4m3, B40, B43
           [-2.94309459, 0.33238441,-0.22804069,-9.30617195],
           [-2.88092334, 0.58528521,-0.28682192,9.96108785]]


BValues = np.asarray([[-2.94309459, 0.33238441,-0.22804069,-9.30617195],  # B20, B4m3, B40, B43 corrected for updated spin-orbit
                      [-2.28984617, 1.45040907,-0.28692218,-9.68697029],
                      [-2.88092334, 0.58528521,-0.28682192, 9.96108785]])*30.0


# # From 15 K but with specified Y-axis = [-0.5,sqrt(3)/2,0]
# BValues = np.asarray([[-2.94309459,-3.83745521,-0.22804069,-8.48464809],  # B20, B4m3, B40, B43 corrected for updated spin-orbit
#                       [-2.28984617,-3.00507941,-0.28692218,-9.32258427],
#                       [-2.88092334, 4.95056495,-0.28682192, 8.66358682]])/30.0 # divide by 30 to replicate anisotropy term from SpinW
## From 60K
# BValues = [[-6.94034588,3.69431903,-0.19622515,-7.54630662],
#            [-3.90688095,2.13708543,-0.25778668,-8.67274454],
#            [9.09503412,3.31871947,-0.49518334,10.2024935]]

# for ion in ions:
    
#     c = PyCrystalField.importCIF(cif,mag_ion=ion,ionS=S,ionL=L,Yaxis=[-0.5,np.sqrt(3)/2,0],Zaxis=[0,0,1],LS_Coupling=-42)# Factor of two from Andrew Boothroyd due to wrong reading of value in PyCrystalField

#     l = c[0]
#     ce = c[1]
    
# h=kkk
    
    
#     # B20 = -2.289846167405785-2.94309459-2.88092334#-2.8809
#     # B4m3 = 1.4504090674792935+ 0.33238441+0.58528521#0.585285
#     # B40 = -0.286922176815416-0.22804069-0.28682192
#     # B43 = -9.68697028772953-9.30617195+9.96108785
    
#     # h=kk
#     # H_CEF = np.sum([SO*B for SO,B in zip(Stevens,[B20,B4m3,B40,B43])],axis=0)/3.0
    
    
    
for BV in [BValues[-1]]:
    
    
    Stevens = [PyCrystalField.LS_StevensOp(L,S,2,0),
               PyCrystalField.LS_StevensOp(L,S,4,-3),
               PyCrystalField.LS_StevensOp(L,S,4,0),
               PyCrystalField.LS_StevensOp(L,S,4,3)]
    
    H_CEF = np.sum([SO*B for SO,B in zip(Stevens,BV)],axis=0)
    LS_Coupling = -42# from Yokosuk et al. npj Quantum Materials (2020) 5:20 ; https://doi.org/10.1038/s41535-020-0224-6  -76.88/2.0
    
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
    
    # States used in calculations
    states = 3#len(ev)
    
    Hamiltonian-=np.eye(Hamiltonian.shape[0])*np.min(eigenValues)
    
    
    #np.einsum('ik,ij,jl->kl',np.conj(eigenVectors[:,:states]),Hamiltonian,eigenVectors[:,:states])
    
    Hnew = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Hamiltonian,eigenVectors[:,:states]))#[:states,:states]
    
    Jx = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jx,eigenVectors[:,:states]))#[:states,:states]
    Jy = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jy,eigenVectors[:,:states]))
    Jz = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Jz,eigenVectors[:,:states]))
    
    Sx = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Sx,eigenVectors[:,:states]))#[:states,:states]
    Sy = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Sy,eigenVectors[:,:states]))
    Sz = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Sz,eigenVectors[:,:states]))
    
    Lx = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Lx,eigenVectors[:,:states]))#[:states,:states]
    Ly = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Ly,eigenVectors[:,:states]))
    Lz = np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(Lz,eigenVectors[:,:states]))
    
    relevantStevens = [np.dot(np.conjugate(eigenVectors[:,:states]).T,np.dot(SO,eigenVectors[:,:states])) for SO in Stevens]



    operators.append([Jx,Jy,Jz])#,*relevantStevens])
    
    
    
    energies.append(ev)
    


operators  = np.asarray([Jx,Jy,Jz]).transpose(1,2,0)
T=5#  in K
H=[0,0,0]#  in T



F = -1.0#2.994#**2#2.7**2#S*(S+1)#np.sqrt(2) # Factor

# -9.2659, J2 = -12.9024, J3 = 1.2184, J4 = 0.1265 
# DM1 = 0.4322, DM2 = 0.3247

J1 = -9.2659*F#*2#.5 
J2 = -12.9024*F#*2#.5
J3 = 1.2184*F#*2
J4 = 0.1265*F#*2

J3 = 0.6383*F 
J4 = 0.6672*F 

DM1 = 0.4322*2#*F#*2#.5#*F 
DM2 = 0.3247*2#*F#*2#.5#*F 

Ani = np.diag([0.0,0.0,2.94309459/3])*0.75#Ani = np.diag([0.0,0.0,0.1])#2.94309459/3])#*12

numberOfOperators = operators.shape[-1]

J1S1=np.zeros((numberOfOperators,numberOfOperators))
J1S1[:3,:3]=J1*np.eye(3)

J2S1=np.zeros_like(J1S1)
J2S1[:3,:3]=J2*np.eye(3)

J3S1=np.zeros_like(J1S1)
J3S1[:3,:3]=J3*np.eye(3)

J4S1=np.zeros_like(J1S1)
J4S1[:3,:3]=J4*np.eye(3)


def DMMatrixFromVector(v):
    return np.asarray([[0.0,v[2],-v[1]],[-v[2],0.0,v[0]],[v[1],-v[0],0.0]])

def VectorFromDMMatrix(m):
    return np.asarray([m[1,2],-m[0,2],m[0,1]])



dmVector1 = [-0.42746356,-0.29602687,0.85419143];
dmVector2 = [ 0.69239715,-0.07716215,0.71737869];

epsilon=0.35;
omega=np.arange(0,6.0,epsilon/3)#


Qs = np.asarray([#[Q1,Q2,Q3,Q4]
                 # [4.0,0.0,0],
                 # [2.0,0.0,0],
                  # [0.5,0.0,1.7],
                  # [0.0,0.0,1.7],
                 # [0.0,0.0,0],
                  [0.0,0.0,1.0],
                  [0.0,0.0,5.0],
                 ])

Qs2 = np.asarray([#[Q1,Q2,Q3,Q4]
                 # [4.0,0.0,0],
                 # [2.0,0.0,0],
                  # [0.5,0.0,1.7],
                  # [0.0,0.0,1.7],
                 # [0.0,0.0,0],
                  [0.4,0.0,1.7],
                  [0.0,0.0,1.7],
                 ])


dq = 71 # steps                 
QRLU1 = np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs,Qs[1:])])).T
QRLU2 = np.concatenate(np.asarray([np.linspace(q1,q2,dq) for q1,q2 in zip(Qs2,Qs2[1:])])).T

QRLU = QRLU1#np.concatenate([QRLU1,QRLU2],axis=1)





z1 = 0.5015  
z2 = 0.2081  
z3 = 0.0088  
positions = np.asarray([[0.0,0.0,z1],
                        [2/3,1/3,z1+1/3],
                        [1/3,2/3,z1+2/3-1],
                        
                        [0.0,0.0,z2],
                        [2/3,1/3,z2+1/3],
                        [1/3,2/3,z2+2/3],
                        
                        [0.0,0.0,z3],
                        [2/3,1/3,z3+1/3],
                        [1/3,2/3,z3+2/3],
                        ])

thetas = [0.0,-np.pi*2/3,np.pi*2/3]*3
rotationOperator = np.asarray([[[np.cos(theta),-np.sin(theta),0.0],[np.sin(theta),np.cos(theta),0.0],[0.0,0.0,1.0]] for theta in thetas])

SS = np.ones((len(positions)))#[1,1,1, 1,1,1, 1,1,1]

lattice = Lattice(S=SS,g = np.full(len(SS),2.5),
                  active = np.ones_like(SS),positions = positions,
                  label = ['Ni2']*len(positions),#,'Ni2','Ni2', 'Ni2','Ni2','Ni2', 'Ni2','Ni2','Ni2'], 
                  site = np.ones_like(SS),#[1,1,1, 1,1,1, 1,1,1], 
                  lattice = [5.15343,5.15343,13.89103,90,90,120],#np.array([[5.15343,0.0,0.0],
                            #          [-5.1534*np.cos(2*np.pi/3)*0,5.15343,0.0],#*np.sin(2*np.pi/3.0),0.0],
                            #         [0.0,0.0,13.89103]]),
                 # equivalence=[0,0,0,1,1,1,2,2,2]#2,3,4,5,6,7,8,9]
                  )



S = System(temperature=T,magneticField=H, lattice=lattice)

S.lattice.generateCouplings(maxDistance = 6.9)


Js = [J2S1,J1S1,J3S1,J4S1]


distances = [2.7685, 3.0266, 3.5099,3.70855]
labels = ['J2','J1','J3','J4']

# nonzero = np.asarray([[j,d] for j,d in zip(Js,distances) if not np.all(np.isclose(j,0.0))]).T


S.lattice.addExchangeInteractions(Js,distances[:len(Js)],labels=labels,atol=0.001)


for i,pos in enumerate(S.lattice.r):
    exchange = Ani
    c = Coupling(i,i,pos,pos,np.asarray([0.0,0.0,0.0]),np.asarray([0.0,0.0,0.0]),0.0,exchange=exchange,label='Ani')
    S.lattice.couplings.append(c)



# def converter(idP):
#     if(idP+1<4):
#         return idP+1+6
#     elif (idP+1)>6:
#         return (idP+1)-6 
#     else:
#         return idP+1

# DMMatrix2 = DMMatrixFromVector(dmVector2)
for coup in S.lattice.couplings:
    if not np.any([np.isclose(coup.exchange[0,0],J3),np.isclose(coup.exchange[0,0],J4)]):continue
    # if not np.isclose(coup.exchange[0,0],J3):continue
    
    p1 = coup.atom1Pos#np.dot(S.lattice.A,coup.atom1Pos)
    p2 = coup.atom2Pos#np.dot(S.lattice.A,coup.atom2Pos)#+np.dot(S.lattice.A,coup.dl)
    
    dV = p2-p1
    
    centre = 0.5*(p1+p2)
    
    dVNormal=dV/np.linalg.norm(dV) 
    ortho = np.cross(dVNormal,np.asarray([0.0,0.0,1.0]))
    normal = np.cross(ortho,dVNormal)
    normal*=1.0/np.linalg.norm(normal)
    
    
    DMMatrix = DMMatrixFromVector(normal)
    if np.isclose(coup.exchange[0,0],J3):
        exchange = DMMatrix*DM1
        title = 'DM1'
    else:
        exchange = DMMatrix*DM2
        title = 'DM2'
        
    coup.exchange+=exchange

S.operators = np.asarray([operators])
S.energies = np.asarray([energies[0][:states]])*0.01



# InitialDistributionSite1_Ext
sizeS = 1
doubling = False # Along c only
config = 1 # not sure
Ncell = 2
nExt = [1,1,Ncell]
numOperators = S.operators.shape[-1]


plot = True



stateUp = np.zeros((numberOfOperators))
stateDown  = np.zeros((numberOfOperators))
stateUp[2] = 1
stateDown[2] = -1



startStates = np.asarray([-1,1,1, 1,-1,1, 1,-1,1,      1,-1,-1, -1,1,-1, -1,1,-1])#,   1,-1,-1, -1,1,1, -1,-1,1])

fullConfiguration = np.zeros((numOperators,len(S.lattice.r)*Ncell))
for i,state in enumerate(startStates ):
    fullConfiguration[:,i] = (state==-1)*stateDown+(state==1)*stateUp
    
    
#######################
import numpy as np
from numpy import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
#################
    
    
if plot:
    ax = plt.figure().add_subplot(projection='3d')
    
    
    positions = np.asarray([[np.dot(S.lattice.A,x+np.asarray([0,0,c])) for x in S.lattice.r for c in [0]]]).T.reshape(3,-1)
    
    ax.scatter3D(*positions ,c = fullConfiguration[2,:positions.shape[-1]]>0.0)
    
    colours = ['r','b','k']
    
    colours = {}
    labelsUsed = []
    for coupling in S.lattice.couplings:
        #line = np.asarray([S.lattice.r[coupling.atom1],S.lattice.r[coupling.atom2]]).T
        try:
            if np.sum(np.abs(coupling.exchange))<0.01:
                continue
        except:
            pass
        p1 = coupling.atom1Pos#np.dot(S.lattice.A,coupling.atom1Pos)
        p2 = coupling.atom2Pos#+np.dot(S.lattice.A,coupling.dl)
        if coupling.type == 'Heisenberg':
            
            line = np.asarray([p1,p2]).T
            regular = True
            a = None
        elif coupling.type == '':
            line = np.asarray([p1,p2]).T
            centre = 0.5*(p1+p2)
            vec = VectorFromDMMatrix(coupling.exchange)
            vec*=1.0/np.linalg.norm(vec)
            
            lineA = np.asarray([centre,centre+vec]).T
            a = Arrow3D(*lineA)
        else:
            
            centre = 0.5*(p1+p2)
            vec = VectorFromDMMatrix(coupling.exchange)
            vec*=5.0/np.linalg.norm(vec)
            lineA = np.asarray([centre,centre+vec]).T
            a = Arrow3D(*lineA)
            line = None
        
        label=coupling.label
        
        
        
        if label in labelsUsed:
            
            c = colours[label]
            label = '_'+label
        else:
            labelsUsed.append(label)
            c = 'C{}'.format((len(labelsUsed)*1)%10)
            
        if not line is None:
            p = ax.plot3D(*line,c=c,label=label)[0]
            colour = p.get_color()
        if not a is None:
            a.set_color(c)
            a.set_label(label)
            p = ax.add_artist(a)
            colour = p.get_facecolor()
            
        if not label[0] == '_':
            colours[label] = colour
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    
    diffs = [np.diff(getattr(ax,'get_{}lim'.format(x))()) for x in ['x','y','z']]
    M = np.max(diffs)
    spare = [0.5*(M-diff) for diff in diffs]
    minima = [getattr(ax,'get_{}lim'.format(x))()[0] for x in ['x','y','z']]
    [getattr(ax,'set_{}lim'.format(x))(m-s,m+M-s) for x,m,s in zip(['x','y','z'],minima,spare)]
    
    # h=kkk


S.fullConfiguration = fullConfiguration


S.lattice.NCell = int(np.product(nExt))

S.lattice.nExt = nExt
# h = KKK

if False:
    temperatures = [5]#[300,100,50,30,20,5]
    
    
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
        # S.fullConfiguration[:3]+=np.random.rand(3, S.fullConfiguration.shape[-1])*0.01
        S.solveSelfConsistency(0.01,limit=100)
        
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
    S.fullConfiguration = fullConfiguration#+(0.001*(np.random.rand(*fullConfiguration.shape)*2-1))*0
    #S.fullConfiguration[:3]+=np.random.rand(3, S.fullConfiguration.shape[-1])*0.001
    S.solveSelfConsistency(limit=100)
    
    S.calculateChi0(omega)


    
S.calculateJQ(QRLU)


S.calculateChi(epsilon=1e-9)



S.calculateSperp()
## calculate prefactor from temperature as well as form factor 

prefactor = (1.0/(1-np.exp(-omega*Units.calculateKelvinToMeV(T)*Units.meV))).reshape(1,-1)  # shape (nQ,nE)

## Calculate Formfactor

qLength = np.linalg.norm(S.QPoints,axis=1)


J = 4#15/2
Sval=1#5/2
L = 3

Sperp = S.Sperp

F2 = formFactor(qLength,J=J,S=Sval,L=L,ion='Ni2').reshape(-1,1)#np.ones((nQ,1))

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
    
    
    tickPositions,ticksLabels = generateTicsk(Qs,12)

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
    
    # ma = 15
    
    # p.set_clim(0.0,ma)
    # p2.set_clim(0.0,ma)
    
    ax.set_title('TOTAL S H = '+','.join(['{:.0f}'.format(x) for x in H]))

    