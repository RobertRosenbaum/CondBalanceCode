import numpy as np

# V=LeakyIntegratorCurrent(Je,Ji,Se,Si,NeuronParameters,tau,dt)
def LeakyIntegratorCurrent(Je,Ji,Se,Si,NeuronParameters,tau,dt):
    Ne=len(Je)
    Ni=len(Ji)
    Cm = NeuronParameters['Cm']
    gL = NeuronParameters['gL']
    EL = NeuronParameters['EL']
    taue = tau[0]
    taui = tau[1]

    Ie = np.zeros(Nt)
    Ii = np.zeros(Nt)
    V = np.zeros(Nt)
    V[0]=EL
    ispikeE=0
    nspikeE=Se.shape[1]
    ispikeI=0
    nspikeI=Si.shape[1]

    for i in range(Nt-1):
        
        # # # # WE WOULD USE THIS FOR SPARSE REP OF Se and Si AND MATRIX FOR Je and Ji
        # # Propagate spikes by incrementing currents
        # while ispikeE + 1 < nspikeE and Se[0,ispikeE] <= i*dt:
        #     jpre = int(Se[1,ispikeE])
        #     Ie[i+1] = Ie[i] + Je[jpre] / taue
        #     ispikeE = ispikeE + 1
        # while ispikeI + 1 < nspikeI and Si[0,ispikeI] <= i*dt:
        #     jpre = int(Si[1,ispikeI])
        #     Ii[i+1] = Ii[i] + Ji[jpre] / taui
        #     ispikeI = ispikeI + 1

        # Euler update to currents
        # WE ADD Se and Si BELOW FOR FULL REP AS DIRAC DELTA FUNCTIONS
        Ie[i+1] = Ie[i]+(dt/taue)*(-Ie[i]+Je@Se[i])
        Ii[i+1] = Ii[i]+(dt/taui)*(-Ii[i]+Ji@Si[i])

        # Euler update to V
        V[i+1] = V[i] + (dt/Cm)*(-gL*(V[i]-EL)+Ie[i]+Ii[i])

        return V


# V=LeakyIntegratorCond(Je,Ji,Se,Si,NeuronParameters,tau,dt)
def LeakyIntegratorCond(Je,Ji,Se,Si,NeuronParameters,tau,dt):
    Ne=len(Je)
    Ni=len(Ji)
    Cm = NeuronParameters['Cm']
    gL = NeuronParameters['gL']
    EL = NeuronParameters['EL']
    Ee = NeuronParameters['Ee']
    Ei = NeuronParameters['Ei']
    taue = tau[0]
    taui = tau[1]

    ge = np.zeros(Nt)
    gi = np.zeros(Nt)
    V = np.zeros(Nt)
    V[0]=EL
    ispikeE=0
    nspikeE=Se.shape[1]
    ispikeI=0
    nspikeI=Si.shape[1]

    for i in range(Nt-1):
        
        # # # # WE WOULD USE THIS FOR SPARSE REP OF Se and Si
        # # Propagate spikes by incrementing currents
        # while ispikeE + 1 < nspikeE and Se[0,ispikeE] <= i*dt:
        #     jpre = int(Se[1,ispikeE])
        #     ge[i+1] = ge[i] + Je[:, jpre] / taue
        #     ispikeE = ispikeE + 1
        # while ispikeI + 1 < nspikeI and Si[0,ispikeI] <= i*dt:
        #     jpre = int(Si[1,ispikeI])
        #     gi[i+1] = gi[i] + Ji[:, jpre] / taui
        #     ispikeI = ispikeI + 1

        # Euler update to currents
        # WE ADD Se and Si BELOW FOR FULL REP AS DIRAC DELTA FUNCTIONS
        ge[i+1] = ge[i]+(dt/taue)*(-ge[i]+Se[i])
        gi[i+1] = gi[i]+(dt/taui)*(-gi[i]+Si[i])



        # Euler update to V
        V[i+1] = V[i] + (dt/Cm)*(-gL*(V[i]-EL)-ge[i]*(V[i]-Ee)+gi[i](V[i]-Ei))

        return V







    






# Function to generate blockwise ER connection matrix
# NsPre = tuple of ints containing number of pre neurons in each block
# Jm = matrix connection weights in each block
# P = matrix of connection probs in each block
# NsPost = number of post neurons in each block
# If NsPost == None, connectivity is assumed recurrent (so NsPre=NsPost)
def GetBlockErdosRenyi(NsPre,Jm,P,NsPost=None):

  if NsPost==None:
    NsPost=NsPre

  # # If Jm is a 1D array, reshape it to column vector
  # if len(Jm.shape)==1:
  #   Jm = np.array([Jm]).T
  # if len(P.shape)==1:
  #   P = np.array([P]).T

  Npre = int(np.sum(NsPre))
  Npost = int(np.sum(NsPost))
  cNsPre = np.cumsum(np.insert(NsPre,0,0)).astype(int)
  cNsPost = np.cumsum(np.insert(NsPost,0,0)).astype(int)
  J = np.zeros((Npost,Npre))

  for j1,N1 in enumerate(NsPost):
    for j2,N2 in enumerate(NsPre):
      J[cNsPost[j1]:cNsPost[j1+1],cNsPre[j2]:cNsPre[j2+1]]=Jm[j1,j2]*(np.random.binomial(1, P[j1,j2], size=(N1, N2)))
  return J


def PoissonProcess(r,Nt,dt,n=1,c=0,rep='full',taujitter=0):
  T=Nt*dt

  if c == 0 or n == 1:
    #print('r', c, n)
    S = np.random.binomial(1, r * dt, (n, Nt)) / dt
  else:
    #print('m')
    rm = r / c
    if rm * dt > .05:
      print('warning: mother process rate is kinda large')
    Sm = np.random.binomial(1, c, (n, Nt)) / dt
    S = Sm * np.random.binomial(1, rm * dt, Nt)
  if rep == 'sparse':
    I, J = np.nonzero(S)
    SpikeTimes = J * dt
    NeuronInds = I

    if taujitter>0:
      SpikeTimes = SpikeTimes + taujitter * np.random.randn(len(SpikeTimes))
      SpikeTimes[SpikeTimes<0] = -SpikeTimes[SpikeTimes<0]
      SpikeTimes[SpikeTimes>T] = T - (SpikeTimes[SpikeTimes>T] - T)

    Isort = np.argsort(SpikeTimes)
    SpikeTimes = SpikeTimes[Isort]
    NeuronInds = NeuronInds[Isort]
    ns = len(SpikeTimes)
    S = np.zeros((2, ns))
    S[0, :] = SpikeTimes
    S[1, :] = NeuronInds

  if taujitter!=0 and (c==0 or rep=='full'):
    print('Cannot jitter')


  # elif rep=='sparse':
  #   if c==0 or n==1:
  #     T=Nt*dt
  #     ns=np.random.poisson(r*T)
  #     SpikeTimes=np.sort(np.random.rand(ns)*T)
  #     NeuronInds=np.random.randint(n)
  #     # Isort=np.argsort(SpikeTimes)
  #     # SpikeTimes=SpikeTimes[Isort]
  #     # NeuronInds=NeuronInds[Isort]
  #     S=np.zeros((2,ns))
  #     S[0,:]=SpikeTimes
  #     S[1,:]=NeuronInds
  #   else:
  #     # First generate full, then convert to sparse
  #     # Maybe fix this later to generate sparse from the start.
  #     rm = r / c
  #     if rm*dt > .05:
  #         print('warning: mother process rate is kinda large')
  #     Sm = np.random.binomial(1, rm * dt, (n, Nt))/dt
  #     S = Sm * np.random.binomial(1, c, (n, Nt))
  #     I, J = np.nonzero(S)
  #     SpikeTimes = J * dt
  #     NeuronInds = I
  #     Isort=np.argsort(SpikeTimes)
  #     SpikeTimes=SpikeTimes[Isort]
  #     NeuronInds=NeuronInds[Isort]
  #     ns=len(SpikeTimes)
  #     S=np.zeros((2,ns))
  #     S[0,:]=SpikeTimes
  #     S[1,:]=NeuronInds

  return S



# # Returns 2D array of spike counts from sparse spike train, s.
# # Counts spikes over window size winsize.
# # h is represented as (neuron)x(time)
# # so h[j,k] is the spike count of neuron j at time window k
# def GetSpikeCounts(s,winsize,N,T):
#
#   xedges=np.arange(0,N+1,1)
#   yedges=np.arange(0,T+winsize,winsize)
#   h,_,_=np.histogram2d(s[1,:],s[0,:],bins=[xedges,yedges])
#   return h
#
# # Returns a resampled version of x
# # with a different dt.
# def DumbDownsample(x,dt_old,dt_new):
#   n = int(dt_new/dt_old)
#   if n<=1:
#     print('New dt should be larger than old dt. Returning x.')
#     return x
#   return x.reshape()
#
