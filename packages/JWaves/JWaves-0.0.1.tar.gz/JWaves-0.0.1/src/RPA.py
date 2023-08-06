# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:06:02 2023

@author: lass_j
"""

import numpy as np
import warnings
import time


def cosd(angle):
    return np.cos(np.deg2rad(angle))

def sind(angle):
    return np.sin(np.deg2rad(angle))


class Units:
    kb=1.38065e-23#  # in J/K
    muB_J=9.274e-24#  # in J
    meV=1.602176565e-19/1000#  # in J
    mu0=4*np.pi*1e-7 #
    def calculateKelvinToMeV(T):
        return np.reciprocal(Units.kb*T)


def getTimeUnit(timeRemaining):
    if timeRemaining>60*60*100:
        timeRemaining*=1./(60.0*60*24)
        unit = 'days.. go home!'
    elif timeRemaining>60*100: # convert to hours due to more than 100 minutes
        timeRemaining*=1./(60.0*60)
        unit = 'hr'
    elif timeRemaining>100:
        timeRemaining*=1./60.0
        unit = 'min'
    else:
        unit = 'sec'
    return timeRemaining, unit

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    if hasattr(printProgressBar,'_iterations'):
        if iteration == printProgressBar._iterations[-1]:
            return
    
    if iteration == 0 or (iteration == 1 and not hasattr(printProgressBar,'_time')):
        printProgressBar._time = [time.time()]
        printProgressBar._iterations = [iteration]
        timeEstimate = ''
    
    else:
        printProgressBar._time.append(time.time())
        printProgressBar._iterations.append(iteration)
        timeDelta = np.diff(-np.asarray(printProgressBar._time))
        iterationDelta = np.diff(-np.asarray(printProgressBar._iterations))
        
        timeRemaining = np.mean(timeDelta/iterationDelta)*(total-iteration)
        timeRemaining,unit = getTimeUnit(timeRemaining)

        timeEstimate = '({:.2f} {:})'.format(timeRemaining,unit)
        
        
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    
    
    print(f'\r{prefix} |{bar}| {percent}% {timeEstimate} {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        totalTime = printProgressBar._time[-1]-printProgressBar._time[0]
        totalTime,unit = getTimeUnit(totalTime)
        tt = '({:.2f} {:})'.format(totalTime,unit)
        print(f'\r{prefix} |{bar}| DONE {tt} {suffix}', end = printEnd)
        print()

class Coupling():

    def __init__(self,atom1,atom2,atom1Pos,atom2Pos,dl,distanceVector,distance,exchange=None,doubleCounted = False, label = None):
        """Coupling class
        
        Args:

            - atom1 (int): Atom index of first atom

            - atom2 (int): Atom index of second atom

            - atom1Pos (list): Fractional position of atom 1 within unit cell

            - atom2Pos (list): Fractional position of atom 2 within unit cell

            - dl (list): Lattice displacement to second atom

            - distanceVector (list): Distance vector in AA

            - distance (float): Real space distance between atoms

        Kwargs:

            - exchange (list): Exchange matrix (default None)

            - doubleCounting (bool): Double counting flag (default False)


        """
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom1Pos = atom1Pos
        self.atom2Pos = atom2Pos
        self.dl = dl
        self.distanceVector = distanceVector
        self.distance = distance
        self.exchange = exchange
        self.label = label

        self.isDouble = doubleCounted # double counting flag

    @property
    def exchange(self):
        return self._exchange
    
    @exchange.getter
    def exchange(self):
        return self._exchange
    
    @exchange.setter
    def exchange(self,newExchange):
        self._exchange = newExchange
        if newExchange is None:
            self.type = ''
        elif np.all(np.isclose(np.diag(np.diag(newExchange)),newExchange)):# exchange is diagonal
            self.type = 'Heisenberg'
        elif np.all(np.isclose(newExchange,newExchange.T)):
            self.type = 'Symmetric'
        elif np.all(np.isclose(newExchange,-newExchange.T)):
            self.type = 'Antisymmetric'
        else:
            self.type = ''
    


    def __eq__(self,other):
        """Check equivalence of couplings"""

        # All is the same
        idxTestDirect = self.atom1 == other.atom1 and self.atom2 == other.atom2
        idxTestDirect *= np.all(np.isclose(self.dl,other.dl))

        # opposite direction
        idxTestOpposite = self.atom1 == other.atom2 and self.atom1 == other.atom2
        idxTestOpposite *= np.all(np.isclose(self.dl,-other.dl))

        if not (idxTestDirect or idxTestOpposite):
            #print('idxtest')
            #print(idxTestDirect)
            #print(idxTestOpposite)
            return False
        
        if (self.exchange is None) ^ (other.exchange is None):
            # One of the exchanges is zero
            #print('single None')
            return False
        if (self.exchange is None) and (other.exchange is None):
            #print('Both none')
            return True
        
        if np.all(np.isclose(self.exchange,other.exchange)):
            #print('exchange is the same')
            return True
        return False 

    def __str__(self):
        return "Coupling between {:} and {:} (distance {:} - dl = {:})".format(self.atom1,self.atom2,self.distance,self.dl)+(not self.exchange is None)*(" with exchange\n"+str(self.exchange))


class Lattice: # From Add_ChainS1N1 (without Active, site, label and equivalence)
    def __init__(self,S=None,g=None, positions = None, active=None, lattice = None, 
                 label=None,site=None,equivalence = None):
        
        
        self.g = g
        self.S = S
        self.active = active
        self.r = np.asarray(positions).reshape(-1,3)
        
        self.Natom = len(self.S)
        
        
        
        
        self.label = label
        self.site = site
        if equivalence is None:
            self.equivalence = np.zeros(len(positions),dtype=int)
        else:
            self.equivalence = equivalence
        self.couplings = []
        
        lattice = np.asarray(lattice)
        
        if len(lattice.shape)>1:
            self.A = lattice
        else:
            self.generateLattice(*lattice)
        
        self.calculateB()
    
    def generateLattice(self,a,b,c,alpha,beta,gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.realVectorA = np.array([self.a,0,0])
        self.realVectorB = self.b*np.array([cosd(self.gamma),sind(self.gamma),0.0])#np.dot(np.array([self.b,0,0]),rotationMatrix(0,0,self.gamma))
        self.realVectorC = self.c*np.array([cosd(self.beta),(cosd(self.alpha)-cosd(self.beta)*cosd(self.gamma))/sind(self.gamma),
        np.sqrt(1-cosd(self.beta)**2-((cosd(self.alpha)-cosd(self.beta)*cosd(self.gamma))/sind(self.gamma))**2)])
        self.A = np.asarray([self.realVectorA,self.realVectorB,self.realVectorC]).T

    def calculateB(self):
        vol = np.dot(self.A[2],np.cross(self.A[0],self.A[1]))
        self.B = np.pi*2*np.asarray([np.cross(a1,a2)/vol for a1,a2 in zip([self.A[1],self.A[2],self.A[0]],[self.A[2],self.A[0],self.A[1]])])
        
    def generateCouplings(self,maxDistance):
        # Find number of unit cells along a, b, and c for calculation
        norm = np.linalg.norm(self.A,axis=1)
        NVector = np.ceil(maxDistance/norm).astype(int)+1
        couplings = []
        for c in range(-NVector[2],NVector[2]+1):
            for b in range(-NVector[1],NVector[1]+1):
                for a in range(-NVector[0],NVector[0]+1):#range(NVector[2]):#r
                    for I,atom1 in enumerate(self.r):
                        for J,atom2 in enumerate(self.r):
                            atom2Pos = np.dot(self.A,atom2+[a,b,c])#+np.dot([a,b,c],self.A)
                            
                            dl = np.array([a,b,c])
                            atom1Pos = np.dot(self.A,atom1)
                            d = atom2Pos-atom1Pos
                            normD = np.linalg.norm(d)
                            if np.isclose(normD,0):
                                continue
                            
                            if normD<maxDistance:
                                # check if opposite coupling is already present
                                idxes = [idx for idx in couplings if idx.atom1==J and idx.atom2 == I and (np.all(idx.dl==dl) or np.all(idx.dl==-dl))]
                                if not np.any([np.isclose(normD,idx.distance) for idx in idxes]):
                                    couplings.append(Coupling(I,J,atom1Pos,atom2Pos,dl,d,normD))

        # Sort couplings in increasing distance
        couplings.sort(key=lambda coupling: coupling.distance)
        self.couplings = couplings

        
    def checkDoublCounting(self):
        testMatrix = np.full((len(self.couplings),len(self.couplings)),False)
        for i,c1 in enumerate(self.couplings):
            for j,c2 in enumerate(self.couplings):#[:i]):
                testMatrix[i,j] = c1==c2

        return testMatrix
    
        
    def addExchangeInteractions(self,Js,distances,labels=None, atol=0.001):
        """add exchange interactions
        
        Args:
            
            - Js (list): List of J-matrices
            
            - distances (list): Distance of J coupling
            
        Kwargs:

            - labels (list): List of labels corresponding to the provided couplings (default None)
            
            - atol (float): absolute tolerence for comparing distances (default 0.001)
            
        """
        if not hasattr(self,'couplings'):
            raise AttributeError('Lattice has no couplings generated. Please invoke .generateCouplings(maxDistance)')
        
        
        if not len(Js) == len(distances):
            raise AttributeError('Provided list of Js does not match length of distances....')
            
        if not labels is None:
            labels = np.asarray(labels)
        Js = np.asarray(Js)
        for coupling in self.couplings:
            if self.site[coupling.atom1] == self.site[coupling.atom2]: # Lattice.Site(atom1)==Lattice.Site(atom2)
                if self.site[coupling.atom1] == 1: # Not sure what this checks....
                    # Find J corresponding to current coupling, from distance
                    comparison = np.isclose(coupling.distance,distances,atol=atol)
                    #print(coupling)
                    if np.sum(comparison) == 0:
                        J = None
                    #if not np.sum(comparison) == 1:
                    #    raise AttributeError('Number of couplings found is not equal 1. Found',np.sum(comparison))
                    else:
                        J = Js[comparison][0] ## TODO: move exchange to coupling
                        if not labels is None:
                            label = labels[comparison][0]
                        else:
                            label = None
                    
                    coupling.exchange = J
                    coupling.label = label
        
        self.couplings = [coupling for coupling in self.couplings if not coupling.exchange is None]
                    
    def buildDipolarInteractionMatrix(self):
        for i,coupling in enumerate(self.couplings):
            atom1 = coupling.atom1
            atom2 = coupling.atom2
            dl = coupling.dl
            r1 = coupling.atom1Pos
            r2 = r1+np.dot(self.A,dl)
            
            g1 = self.g[atom1]
            g2 = self.g[atom2]
            
            J,NormR,DiffR = DipolarMatrix(g1, g2, Units.muB_J, Units.mu0, Units.meV, r1, r2)
            
            coupling.exchange[:3,:3]+=J


class System:
    """Class to manage the RPA calculations"""
    
    epsilon = 0.05 # Small imaginary part to add to ensure invertability of matrices
    
    def __init__(self,temperature = None, magneticField = [0.0,0.0,0.0], lattice = None):
        
        self.verbose = True
        
        self.temperature = temperature
        self.magneticField = np.asarray(magneticField)
        self.lattice = lattice
        
        
    def getProperty(self,propertyName,inputValue):
        if not hasattr(self,propertyName):
            setattr(self,propertyName,inputValue)
            return inputValue
        else:
            if inputValue is None:
                val = getattr(self,propertyName,None)
        return val
    
    @property
    def NOperators(self):
        return self.operators.shape[-1]
    
    @NOperators.getter
    def NOperators(self):
        if not hasattr(self,'operators'):
            raise AttributeError('System does not have any operators!')
        return self.operators.shape[-1]


        
    def solveSelfConsistency(self,ConvergenceCriteria = 0.005, fullConfiguration=None,operators=None,energy=None,limit=100):
        fullConfiguration = self.getProperty('fullConfiguration',fullConfiguration)
        operators = self.getProperty('operators', operators)
        energy = self.getProperty('energy',energy)
        states_energy = self.energies#np.repeat(self.energies[np.newaxis],repeats=self.lattice.Natom,axis=0)
            
        if fullConfiguration is None:
            raise AttributeError('fullConfiguration is not set!')
            
        convergence = 1
        
        expectedJ = fullConfiguration
        totalRounds = 0
        while convergence >= ConvergenceCriteria and totalRounds<limit:# 
            ##################
            # Calculate_Heff
            
            expectedJ_previous = expectedJ
            
            Hamiltonian_Heff = np.zeros((self.NOperators,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            for c in range(self.lattice.nExt[2]):
                for b in range(self.lattice.nExt[1]):
                    for a in range(self.lattice.nExt[0]): # loop through extended unit cells
                        for atomID in np.arange(self.lattice.Natom): # loop through all atoms in a unit cell
                            total = np.zeros((1,self.NOperators),dtype=np.complex)
                            for coupling in self.lattice.couplings:
                                
                                if atomID==coupling.atom1:
                                    

                                    atom2ID = coupling.atom2
                                    cellRelative = (np.mod((coupling.dl+np.array([a,b,c]))/self.lattice.nExt,1)*self.lattice.nExt).astype(int)
                                
                                    relIdx = relativeIdx(cellRelative,self.lattice.nExt,self.lattice.Natom)
                                    Sj = fullConfiguration[:,atom2ID+relIdx]
                                    
                                    Jij = coupling.exchange
                                    
                                    total+=np.dot(Jij,Sj)
                                    
                                if atomID==coupling.atom2:
                                    
                                    atom2ID = coupling.atom1
                                    cellRelative = (np.mod((-coupling.dl+np.array([a,b,c]))/self.lattice.nExt,1)*self.lattice.nExt).astype(int)
                                
                                    relIdx = relativeIdx(cellRelative,self.lattice.nExt,self.lattice.Natom)
                                    
                                    Sj = fullConfiguration[:,atom2ID+relIdx]
                                    Jij = coupling.exchange
                                    total+=np.dot(Jij,Sj)
                                    
                            idxAtom1 = relativeIdx([a,b,c],self.lattice.nExt,self.lattice.Natom)
                            Hamiltonian_Heff[:,atomID+idxAtom1] = total
                            
            
            ###################
            # Solve_MF_Hamiltonian
            MatSize = len(self.energies[0])
            
            # Initialize the needed amtrices
            Hamiltonian_Hcf=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            Hamiltonian_Hfield=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            Hamiltonian_Hint1=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            Hamiltonian_Hint2=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            Hamiltonian_Hfull=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            Hamiltonian_Hdiag=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            Hamiltonian_eigenV=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell),dtype=np.complex);
            
            Hamiltonian_Gs=np.zeros((MatSize,MatSize,self.lattice.Natom*self.lattice.NCell,self.NOperators),dtype=np.complex);
            
            
            expectedJ = np.zeros((self.NOperators,self.lattice.Natom*self.lattice.NCell),dtype=np.complex)
            
            for c in range(self.lattice.nExt[2]):
                for b in range(self.lattice.nExt[1]):
                    for a in range(self.lattice.nExt[0]): # loop through extended unit cells
                        for j in range(self.lattice.Natom): # loop over atoms
                            if self.lattice.active[j]: # Only if the atom is active
                                equivalenceID = self.lattice.equivalence[j]

                                trueIndex = relativeIdx([a,b,c],self.lattice.nExt,self.lattice.Natom)+j
                                
                                HField = np.zeros((MatSize,MatSize,3),dtype=np.complex);
                                
                                Si = fullConfiguration[:,trueIndex]
                                
                                # Hamiltonian from Crystal Electric Field (Solved independently)
                                Hamiltonian_Hcf[:,:,trueIndex]=np.diag(states_energy[equivalenceID]);
                                
                                # Hamiltonian for field, assuming first three operators ar Jx, Jy, and Jz!
                                for k in range(3):
                                    
                                    HField[:,:,k]=self.operators[equivalenceID,:,:,k].T*self.lattice.g[equivalenceID]*Units.muB_J*self.magneticField[k]/Units.meV;
                                
                                Hamiltonian_Hfield[:,:,trueIndex] = -np.sum(HField,axis=-1)
                                    
                                #Hamiltonian for first part of interaction
                                
                                for op,eff in zip(operators[equivalenceID].transpose(2,1,0),Hamiltonian_Heff[:,trueIndex]):
                                    
                                    Hamiltonian_Hint1[:,:,trueIndex]+=-1.0*op*eff;
                                
                                
                                
                                #Hamiltonian for second part of interaction
                                int2=0.5*np.dot(Si,Hamiltonian_Heff[:,trueIndex]);
                                Hamiltonian_Hint2[:,:,trueIndex]=int2*np.eye(MatSize);
                                
                                Hamiltonian_Hfull[:,:,trueIndex]=Hamiltonian_Hcf[:,:,trueIndex]\
                                    +Hamiltonian_Hfield[:,:,trueIndex] \
                                    +Hamiltonian_Hint1[:,:,trueIndex] \
                                    +Hamiltonian_Hint2[:,:,trueIndex];
                                
                                
                                eigenValues,eigenVectors = np.linalg.eig(Hamiltonian_Hfull[:,:,trueIndex])
                                eigenValues = np.real(eigenValues)
                                Hamiltonian_Hdiag[:,:,trueIndex]=np.diag(eigenValues)
                                Hamiltonian_eigenV[:,:,trueIndex] = eigenVectors
                                
                                
                                for m in range(MatSize):
                                    for n in range(MatSize):
                                        for k,op in enumerate(operators[equivalenceID].transpose(2,1,0)):
                                            Hamiltonian_Gs[m,n,trueIndex,k]= np.dot(np.conj(Hamiltonian_eigenV[:,n,trueIndex]),np.dot(op.T,Hamiltonian_eigenV[:,m,trueIndex].T))
                                            
                                            
                                
                                expectedJ[:,trueIndex] =  np.einsum('i,iik->k',population(eigenValues,self.temperature),Hamiltonian_Gs[:,:,trueIndex])
            
            # Make sure the magnetic moment of the expected J is real
            if np.abs(np.imag(expectedJ[:3])).max()>1e-2:

                raise AttributeError('The imaginary part of the expectation value of J is larger than 1e-2. Was',np.imag(expectedJ[:3]))
            expectedJ[:3]=np.real(expectedJ[:3])
                                
            # use found J's as new input
            fullConfiguration = expectedJ ## Take care of inactive ions
            
            self.Hamiltonian_Hcf=Hamiltonian_Hcf
            self.Hamiltonian_Hfield=Hamiltonian_Hfield
            self.Hamiltonian_Hfull=Hamiltonian_Hfull
            self.Hamiltonian_Hdiag=Hamiltonian_Hdiag
            self.Hamiltonian_Gs=Hamiltonian_Gs
            self.fullConfiguration = fullConfiguration
            
            convergence = np.max(np.abs(np.diff([expectedJ,expectedJ_previous],axis=0)))
            if self.verbose: print('Convergence ('+str(totalRounds)+'):',convergence)
            totalRounds+=1
            
            
        if self.verbose and convergence<=ConvergenceCriteria: print('Self-consistency equations solved')
        else:
            warnings.warn('Self-consistency equations are not solve! Solution might be dodgy...')
        
    def calculateChi0(self,omega,ElasticThreshold=0.01):
        
        self.Chi0_elastic = np.zeros((self.NOperators,self.NOperators,self.lattice.Natom*self.lattice.NCell),dtype=np.complex)
        self.Chi0_inelastic = np.zeros((self.NOperators,self.NOperators,self.lattice.Natom*self.lattice.NCell,len(omega)),dtype=np.complex)
        
        self.omega = omega
        
        MegaG=self.Hamiltonian_Gs
        MatSize = len(self.energies[0])
        if self.verbose: print(r'Calculating Chi0')
        
        for c in range(self.lattice.nExt[2]):
            for b in range(self.lattice.nExt[1]):
                for a in range(self.lattice.nExt[0]): # loop through extended unit cells
                    for j in range(self.lattice.Natom): # loop over atoms
                        if self.lattice.active[j]: # Only if the atom is active
                            trueIndex = relativeIdx([a,b,c],self.lattice.nExt,self.lattice.Natom)+j
                            Energies=np.diag(self.Hamiltonian_Hdiag[:,:,trueIndex])
                            pop=population(Energies,self.temperature)
                            
                            for x in np.arange(self.NOperators):# enumerate(self.operators.transpose(2,1,0)):
                                for y in np.arange(self.NOperators):#enumerate(self.operators.transpose(2,1,0)):
                                    for m in range(MatSize):
                                        for n in range(MatSize):
                                            deltaE = Energies[m]-Energies[n]
        
                                            if abs(deltaE)<ElasticThreshold: # We are elastic
                                                
                                                self.Chi0_elastic[x,y,trueIndex]+=Units.calculateKelvinToMeV(self.temperature)*Units.meV*pop[m]*\
                                                    MegaG[m,n,trueIndex,x]*MegaG[n,m,trueIndex,y]
                                            else: # the inelastic case
                                                self.Chi0_inelastic[x,y,trueIndex,:]+=MegaG[m,n,trueIndex,x]*MegaG[n,m,trueIndex,y]*\
                                                    (pop[m]-pop[n])/(Energies[n]-Energies[m]-(self.omega+self.epsilon*1j))
                                                        
                                                    
                                            
                        
    def calculateJQ(self,QRLU=None):
        QRLU = self.getProperty('QRLU', QRLU)
        self.QPoints = np.asarray([np.dot(self.lattice.B,q) for q in QRLU.T])
        
        self.Chi0_JQ = np.zeros((self.NOperators,self.NOperators,len(self.QPoints),self.lattice.Natom*self.lattice.NCell,self.lattice.Natom*self.lattice.NCell),dtype=np.complex)
        
        if self.verbose: print('Calculating J(Q)')
        for qidx,Q in enumerate(self.QPoints):
            for c in range(self.lattice.nExt[2]):
                for b in range(self.lattice.nExt[1]):
                    for a in range(self.lattice.nExt[0]): # loop through extended unit cells
                        for atomID in np.arange(self.lattice.Natom): # loop through all atoms in a unit cell
                            
                            for coupling in self.lattice.couplings:
                                
                                if atomID in [coupling.atom1,coupling.atom2]:#coupling[0] == atomID or coupling[1] == atomID:
                                    
                                    if atomID == coupling.atom1:
                                        
                                        atom1 = atomID
                                        atom2 = coupling.atom2
                                        dl = coupling.dl
                                        shift = dl+np.asarray([a,b,c])
                                        indices = (np.mod(shift/self.lattice.nExt,1)*self.lattice.nExt).astype(int)
                                        atom2 += relativeIdx(indices,self.lattice.nExt,self.lattice.Natom)
                                        atom1 += relativeIdx([a,b,c],self.lattice.nExt,self.lattice.Natom)
                                        
                                        deltaR = -coupling.distanceVector
                                        Jij = coupling.exchange.T
                                        self.Chi0_JQ[:,:,qidx,atom1,atom2]+=+Jij*np.exp(-1j*np.dot(Q,deltaR))
                                        
                                        
                                    if atomID == coupling.atom2:
                                        atom2 = atomID
                                        atom1 = coupling.atom1
                                        dl = coupling.dl
                                        shift = dl+np.asarray([a,b,c])
                                        indices = (np.mod(shift/self.lattice.nExt,1)*self.lattice.nExt).astype(int)
                                        atom2 += relativeIdx(indices,self.lattice.nExt,self.lattice.Natom)
                                        atom1 += relativeIdx([a,b,c],self.lattice.nExt,self.lattice.Natom)
                                    
                                        deltaR = -coupling.distanceVector
                                        Jij = coupling.exchange
                                        self.Chi0_JQ[:,:,qidx,atom2,atom1]+=Jij*np.exp(-1j*np.dot(Q,-deltaR))


    def calculateChi(self,ElasticThreshold=0.01, epsilon = 0.0):
        """
        Calculate the magnetic Susceptibility

        Kwargs:

            - ElasticThreshold (float): Distance to the elastic line within which the elastic susceptibility is used (default 0.01 meV)

            epsilon (float): Regularization parameter used to ensure invertibility of Chi0_inelastic (default 0, but use 1e-8)
        """

        
        
        active = np.repeat(self.lattice.active,axis=0,repeats=self.lattice.NCell).astype(bool)

        equivalent = np.arange(self.lattice.Natom*self.lattice.NCell)[active]
        
        totalActiveAtoms = len(equivalent)
        
        
        
        self.Chi = np.zeros((self.NOperators,self.NOperators,totalActiveAtoms,totalActiveAtoms,len(self.QPoints),len(self.omega)),dtype=np.complex)
        self.Chi_total = np.zeros((self.NOperators,self.NOperators,len(self.QPoints),len(self.omega)),dtype=np.complex)
        
        # print('Calculating Chi and Chi_total')
        if self.verbose: printProgressBar(0,len(self.QPoints),prefix='Calculating Chi and Chi_total',length=71)
        for qidx,q in enumerate(self.QPoints):
            try:
                regularization = np.eye(len(self.Chi0_inelastic))*epsilon
                for omegaidx,om in enumerate(self.omega):
                    for i in range(totalActiveAtoms):
                        
                        Mat = np.zeros((totalActiveAtoms,self.NOperators,totalActiveAtoms,self.NOperators),dtype=np.complex)
                        aa,bb = np.meshgrid(equivalent,equivalent)
                        
                        Mat[aa,:,bb,:]=-self.Chi0_JQ[:,:,qidx,aa,bb].transpose(2,3,0,1)
                        
                        
                        if np.abs(om) < ElasticThreshold:
                            
                            chi0 = np.asarray([np.linalg.inv(self.Chi0_elastic[:,:,a]+self.Chi0_inelastic[:,:,a,omegaidx]+regularization) for a in equivalent])
                        else:
                            chi0 = np.asarray([np.linalg.inv(self.Chi0_inelastic[:,:,a,omegaidx]+regularization) for a in equivalent])
                        Mat[equivalent,:,equivalent,:]+=chi0
                    
            
                        Vec = np.zeros((self.NOperators*totalActiveAtoms,self.NOperators),dtype=np.complex)
                        Vec[i*self.NOperators:(i+1)*self.NOperators,:] = np.eye(self.NOperators)
                        
                        Mat = Mat.reshape(totalActiveAtoms*self.NOperators,totalActiveAtoms*self.NOperators)
                        
                        Var = np.linalg.solve(Mat,Vec)
                        
                        
                        iEqui = equivalent[i]
                        
                        for j in equivalent:
                            self.Chi[:,:,j,iEqui,qidx,omegaidx] = Var[j*self.NOperators:(j+1)*self.NOperators,:]
                        self.Chi_total[:,:,qidx,omegaidx]+=np.sum(Var.reshape(totalActiveAtoms,self.NOperators,self.NOperators),axis=0)
            except np.linalg.LinAlgError as e:
                print(q,i,om)
#                print(Mat,Vec)
                raise e
                    
            if self.verbose: printProgressBar(qidx+1,len(self.QPoints),prefix='Calculating Chi and Chi_total',length=71)
            
        self.Chi_total = self.Chi_total.transpose([2,3,0,1])
        
        
    def calculateSperp(self):
        # Assuming that the first three operators are Sx, Sy, Sz
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            QPerp = np.array([1.0,1.0,1.0]).reshape(1,3)-np.abs(self.QPoints)/(np.linalg.norm(self.QPoints,axis=1).reshape(-1,1))
        
        QPerp[np.isnan(QPerp).any(axis=1),:] = 0.0
        
        self.Sperp = np.einsum('ijkk,ik->ij',np.imag(self.Chi_total[:,:,:3,:3]),QPerp)
        
    
    
   


def relativeIdx(cellRelative,nExt,nAtoms):
    """calculate relative indices between different unit cells
    
    Args:
        
        cellRelative (list of ints): vector connecting cells
        
        nExt (list): list of unit cell extensions in [a,b,c]
        
        nAtoms (int): number of atoms in unit cell
    """
    # The relative index between different unit cells is
    # nAtoms*deltaC+nExt[2]*nAtoms*deltaB+nExt[2]*nExt[1]*nAtoms*deltaA
    return nAtoms*cellRelative[2]+nExt[2]*nAtoms*cellRelative[1]+nExt[2]*nExt[1]*nAtoms*cellRelative[0]


def population(energies,temperature):
    """Calculate population of a set of states given energy [meV] and temperature [K]"""
    
    Energies=energies-np.min(np.real(energies))

    expPart = np.exp(-Units.calculateKelvinToMeV(temperature)*Energies*Units.meV)
    return expPart/np.sum(expPart)#

def DipolarMatrix(g1,g2,muB,mu0,meV,r1,r2):
    
    # calculate the dipolar interaction matrix
    #
    # [DipMat, NormR, DiffR]=DipolarMatrix(g1,g2,muB,mu0,meV,r1,r2)
    #
    # Output:
    # DipMat    Dipolar matrix (3x3)
    # NormR     Norm of R, distance (r2-r1)
    # DiffR     Normalized r2-r1
    #
    
    # N.Gauthier, 2017/09/22
    
    NormR=np.linalg.norm(r2-r1);  
    DiffR=(r2-r1)/NormR;
    
    # Positive = ferro, negatice = antiferro
    
    C= g1*g2*np.power(muB,2.0)*mu0/(4*np.pi*np.power(NormR/1e10,3.0))/meV;
    DipMat= C * np.asarray([[3*DiffR[0]**2-1,3*DiffR[0]*DiffR[1],3*DiffR[0]*DiffR[2]],
                [3*DiffR[0]*DiffR[1],3*DiffR[1]**2-1,3*DiffR[1]*DiffR[2]],
                [3*DiffR[0]*DiffR[2],3*DiffR[1]*DiffR[2],3*DiffR[2]**2-1]])
    return [DipMat, NormR, DiffR]




def ClebschGordan(j1,j2,m1,m2,J,M):
    if not M == m1+m2:
        return 0
    f1 = np.sqrt((2*J+1)*np.math.factorial(J+j1-j2)*np.math.factorial(J-j1+j2)*np.math.factorial(j1+j2-J)/np.math.factorial(j1+j2+J+1))
    f2 = np.sqrt(np.math.factorial(J+M)*np.math.factorial(J-M)*np.math.factorial(j1-m1)*np.math.factorial(j1+m1)*np.math.factorial(j2-m2)*np.math.factorial(j2+m2))
    s = 0
    kmax =2*(j1+j1)+1
    for k in range(-kmax,kmax+1):
        try:
            
            s+=(-1)**k/(np.math.factorial(k)*np.math.factorial(j1+j2-J-k)*np.math.factorial(j1-m1-k)*\
                        np.math.factorial(j2+m2-k)*np.math.factorial(J-j2+m1+k)*np.math.factorial(J-j1-m2+k))
            #print(k)
        except:
            
            continue
    #print(f1,f2,s)
    return f1*f2*s
    



def conversionMatrix(L,S):
    JMax = L+S
    JMin = L-S
    jStates = np.arange(JMin,JMax+1)
    mStates = [x*2+1 for x in jStates]
    
    lStates =(2*L+1) 
    sStates = (2*S+1)
    States = int(lStates*sStates)

    matrix = np.zeros((States,States))
    
    for l in np.arange(-L,L+1):
        for s in np.arange(-S,S+1):
            
            idx = (l*sStates+s+np.floor(States/2)).astype(int)
    
            for I,j in enumerate(jStates):
                for J,m in enumerate(np.arange(-j,j+1)):
                    idx2 = int(np.sum(mStates[:I]).astype('int')+J)
                    f = ClebschGordan(L,S,l,s,j,m)
                    #if not np.isclose(f,0):
                        #print('<{} {} ; {} {} | {} {} >= {}'.format(L,S,l,s,j,m,f))
                    matrix[idx,idx2] = f
    return matrix







