### This chunk contains functions
import math
IntDivide = lambda n,k: int((math.floor(n-1)/k))

import numpy as np

def EIFNetworkCurrent(J, Sx, Jx, Ne, NeuronParameters, tau, Nt, dt, maxns, IeRecord, IiRecord, dtRecord=None):
  N = len(J)
  Ni = N - Ne

  if dtRecord==None:
    dtRecord=dt
  nBinsRecord=round(dtRecord/dt)
  #timeRecord=np.arange(dtRecord, T+dtRecord, dtRecord)
  NtRec=int(np.ceil(Nt/nBinsRecord))


  Jee = J[:Ne, :Ne]
  Jei = J[:Ne, Ne:]
  Jie = J[Ne:, :Ne]
  Jii = J[Ne:, Ne:]
  Jex = Jx[:Ne, :]
  Jix = Jx[Ne:, :]

  Cm = NeuronParameters['Cm']
  gL = NeuronParameters['gL']
  EL = NeuronParameters['EL']
  Vth = NeuronParameters['Vth']
  Vre = NeuronParameters['Vre']
  Vlb = NeuronParameters['Vlb']
  DeltaT = NeuronParameters['DeltaT']
  VT = NeuronParameters['VT']

  taue = tau[0]
  taui = tau[1]
  taux = tau[2]

  Ve = np.random.rand(Ne) * (VT - Vre) + Vre
  Vi = np.random.rand(Ni) * (VT - Vre) + Vre

  #VeFree = np.random.rand(Ne) * (VT - Vre) + Vre
  #ViFree = np.random.rand(Ni) * (VT - Vre) + Vre

  Iee = np.zeros(Ne)
  Iei = np.zeros(Ne)
  Iie = np.zeros(Ni)
  Iii = np.zeros(Ni)
  Iex = np.zeros(Ne)
  Iix = np.zeros(Ni)

 # nBinsRecord = round(dtRecord / dt)
 # NtRec = int(np.ceil(Nt / nBinsRecord))

  Nerecord = len(IeRecord)
  VeRec = np.zeros((NtRec, Nerecord))
  Nirecord = len(IiRecord)
  ViRec = np.zeros((NtRec, Nirecord))

  #VeFreeRec = np.zeros((NtRec, Nerecord))
  #ViFreeRec = np.zeros((NtRec, Nirecord))

  IeeRec = np.zeros((NtRec, Nerecord))
  IeiRec = np.zeros((NtRec, Nerecord))
  IieRec = np.zeros((NtRec, Nirecord))
  IiiRec = np.zeros((NtRec, Nirecord))
  IexRec = np.zeros((NtRec, Nerecord))
  IixRec = np.zeros((NtRec, Nirecord))

  iXspike=0
  nspikeX=Sx.shape[1]

  if hasattr(gL, "__len__"):
    gLe=gL[0]
    gLi=gL[1]
  else:
    gLe=gL
    gLi=gL

  if hasattr(EL, "__len__"):
    ELe=EL[0]
    ELi=EL[1]
  else:
    ELe=EL
    ELi=EL

  nespike = 0
  nispike = 0
  TooManySpikes = False
  se = -1.0 + np.zeros((2, maxns))
  si = -1.0 + np.zeros((2, maxns))
  for i in range(Nt):


    # Euler update to V
    Ve = Ve + (dt / Cm) * (Iee + Iei + Iex + gLe * (ELe - Ve) + DeltaT * np.exp((Ve - VT) / DeltaT))
    Vi = Vi + (dt / Cm) * (Iie + Iii + Iix + gLi * (ELi - Vi) + DeltaT * np.exp((Vi - VT) / DeltaT))
    Ve = np.maximum(Ve, Vlb)
    Vi = np.maximum(Vi, Vlb)

    # Euler update to synaptic currents
    Iee -= dt * Iee / taue
    Iei -= dt * Iei / taui
    Iie -= dt * Iie / taue
    Iii -= dt * Iii / taui
    Iex -= dt * Iex / taux
    Iix -= dt * Iix / taux


    #VeFree = VeFree + (dt / Cm) * (Iee + Iei + Iex + gLe * (ELe - VeFree))
    #ViFree = ViFree + (dt / Cm) * (Iie + Iii + Iix + gLi * (ELi - ViFree))
    #VeFree = np.maximum(VeFree, Vlb)
    #ViFree = np.maximum(ViFree, Vlb)


    # Find which E neurons spiked
    Ispike = np.nonzero(Ve >= Vth)[0]
    if Ispike.any() and not (TooManySpikes):
      # Store spike times and neuron indices
      if nespike + len(Ispike) <= maxns:
        se[0, nespike:nespike + len(Ispike)] = dt * i
        se[1, nespike:nespike + len(Ispike)] = Ispike
      else:
        TooManySpikes = True

      # Reset e mem pot.
      Ve[Ispike] = Vre

      # Update exc synaptic currents
      Iee = Iee + Jee[:, Ispike].sum(axis=1) / taue
      Iie = Iie + Jie[:, Ispike].sum(axis=1) / taue

      # Update cumulative number of e spikes
      nespike = nespike + len(Ispike)

    # Find which I neurons spiked
    Ispike = np.nonzero(Vi >= Vth)[0]
    if Ispike.any() and not (TooManySpikes):
      # Store spike times and neuron indices
      if nispike + len(Ispike) <= maxns:
        si[0, nispike:nispike + len(Ispike)] = dt * i
        si[1, nispike:nispike + len(Ispike)] = Ispike
      else:
        TooManySpikes = True

      # Reset i mem pot.
      Vi[Ispike] = Vre

      # Update inh synaptic currents
      Iei = Iei + Jei[:, Ispike].sum(axis=1) / taui
      Iii = Iii + Jii[:, Ispike].sum(axis=1) / taui

      # Update cumulative number of i spikes
      nispike = nispike + len(Ispike)

    if TooManySpikes:
      print('Too many spikes. Exiting sim at time t =', i * dt)
      break

    Ve[~np.isfinite(Ve)]=Vth
    Vi[~np.isfinite(Vi)]=Vth

    # External inputs
    # Iex = Iex + dt * (-Iex + Jex @ Sx[:, i]) / taux
    # Iix = Iix + dt * (-Iix + Jix @ Sx[:, i]) / taux


    while iXspike + 1 < nspikeX and Sx[0,iXspike] <= i*dt:
      jpre = int(Sx[1,iXspike])
      Iex += Jex[:, jpre] / taux
      Iix += Jix[:, jpre] / taux
      iXspike += 1


    ii=IntDivide(i,nBinsRecord)

    VeRec[ii, :] += np.minimum(Ve[IeRecord],Vth)
    ViRec[ii, :] += np.minimum(Vi[IiRecord],Vth)
    #VeFreeRec[ii, :] += VeFree[IeRecord]
    #ViFreeRec[ii, :] += ViFree[IiRecord]
    IeeRec[ii,:] += Iee[IeRecord]
    IeiRec[ii, :] += Iei[IeRecord]
    IieRec[ii,:] += Iie[IiRecord]
    IiiRec[ii, :] += Iii[IiRecord]
    IexRec[ii, :] += Iex[IeRecord]
    IixRec[ii, :] += Iix[IiRecord]


  Recording={}
  Recording['Ve']=VeRec/nBinsRecord
  Recording['Vi'] = ViRec/nBinsRecord
  #Recording['VeFree'] = VeFreeRec/nBinsRecord
  #Recording['ViFree'] = ViFreeRec/nBinsRecord

  Recording['Iee'] = IeeRec/nBinsRecord
  Recording['Iei'] = IeiRec/nBinsRecord
  Recording['Iie'] = IieRec/nBinsRecord
  Recording['Iii'] = IiiRec/nBinsRecord
  Recording['Iex'] = IexRec/nBinsRecord
  Recording['Iix'] = IixRec/nBinsRecord

  return se, si, Recording

# E-I recurrent EIF spiking network with conductance-based external synaptic input
def EIFNetworkCond(J, Sx, Jx, Ne, NeuronParameters, tau, Nt, dt, maxns, IeRecord, IiRecord, dtRecord=None):
  N = len(J)
  Ni = N - Ne

  if dtRecord==None:
    dtRecord=dt
  nBinsRecord=round(dtRecord/dt)
  #timeRecord=np.arange(dtRecord, T+dtRecord, dtRecord)
  NtRec=int(np.ceil(Nt/nBinsRecord))


  Cm = NeuronParameters['Cm']
  gL = NeuronParameters['gL']
  EL = NeuronParameters['EL']
  Vth = NeuronParameters['Vth']
  Vre = NeuronParameters['Vre']
  Vlb = NeuronParameters['Vlb']
  DeltaT = NeuronParameters['DeltaT']
  VT = NeuronParameters['VT']
  Ee = NeuronParameters['Ee']
  Ei = NeuronParameters['Ei']

  Jee = J[:Ne, :Ne]
  Jei = J[:Ne, Ne:]
  Jie = J[Ne:, :Ne]
  Jii = J[Ne:, Ne:]
  Jex = Jx[:Ne, :]
  Jix = Jx[Ne:, :]

  taue = tau[0]
  taui = tau[1]
  taux = tau[2]


  if hasattr(gL, "__len__"):
    gLe=gL[0]
    gLi=gL[1]
  else:
    gLe=gL
    gLi=gL

  if hasattr(EL, "__len__"):
    ELe=EL[0]
    ELi=EL[1]
  else:
    ELe=EL
    ELi=EL

  Ve = np.random.rand(Ne) * (VT - Vre) + Vre
  Vi = np.random.rand(Ni) * (VT - Vre) + Vre
  #VeFree = np.random.rand(Ne) * (VT - Vre) + Vre
  #ViFree = np.random.rand(Ni) * (VT - Vre) + Vre

  gee = np.zeros(Ne)
  gei = np.zeros(Ne)
  gie = np.zeros(Ni)
  gii = np.zeros(Ni)
  gex = np.zeros(Ne)
  gix = np.zeros(Ni)

  Nerecord = len(IeRecord)
  VeRec = np.zeros((NtRec, Nerecord))
  Nirecord = len(IiRecord)
  ViRec = np.zeros((NtRec, Nirecord))

  #VeFreeRec = np.zeros((NtRec, Nerecord))
  #ViFreeRec = np.zeros((NtRec, Nirecord))


  geeRec = np.zeros((NtRec, Nerecord))
  geiRec = np.zeros((NtRec, Nerecord))
  gieRec = np.zeros((NtRec, Nirecord))
  giiRec = np.zeros((NtRec, Nirecord))
  gexRec = np.zeros((NtRec, Nerecord))
  gixRec = np.zeros((NtRec, Nirecord))

  iXspike=0
  nspikeX=Sx.shape[1]

  nespike = 0
  nispike = 0
  TooManySpikes = False
  se = -1.0 + np.zeros((2, maxns))
  si = -1.0 + np.zeros((2, maxns))
  for i in range(Nt):
    # # External inputs
    # gex = gex + dt * (-gex + Jex @ Sx[:, i]) / taux
    # gix = gix + dt * (-gix + Jix @ Sx[:, i]) / taux

    while iXspike + 1 < nspikeX and Sx[0,iXspike] <= i*dt:
        jpre = int(Sx[1,iXspike])
        gex = gex + Jex[:, jpre] / taux
        gix = gix + Jix[:, jpre] / taux
        iXspike = iXspike + 1

    # Euler update to V
    Ve = Ve + (dt / Cm) * (gee * (Ee - Ve) + gei * (Ei - Ve) + gex * (Ee - Ve) + gLe * (ELe - Ve) + DeltaT * np.exp(
      (Ve - VT) / DeltaT))
    Vi = Vi + (dt / Cm) * (gie * (Ee - Vi) + gii * (Ei - Vi) + gix * (Ee - Vi) + gLi * (ELi - Vi) + DeltaT * np.exp(
      (Vi - VT) / DeltaT))
    Ve = np.maximum(Ve, Vlb)
    Vi = np.maximum(Vi, Vlb)

    #VeFree = VeFree + (dt / Cm) * (gee * (Ee - VeFree) + gei * (Ei - VeFree) + gex * (Ee - VeFree) + gL * (EL - VeFree))
    #ViFree = ViFree + (dt / Cm) * (gie * (Ee - ViFree) + gii * (Ei - ViFree) + gix * (Ee - ViFree) + gL * (EL - ViFree))
    # VeFree = np.maximum(VeFree, Vlb)
    # ViFree = np.maximum(ViFree, Vlb)

    # Find which E neurons spiked
    Ispike = np.nonzero(Ve >= Vth)[0]
    if Ispike.any() and not (TooManySpikes):
      # Store spike times and neuron indices
      if nespike + len(Ispike) <= maxns:
        se[0, nespike:nespike + len(Ispike)] = dt * i
        se[1, nespike:nespike + len(Ispike)] = Ispike
      else:
        TooManySpikes = True

      # Reset e mem pot.
      Ve[Ispike] = Vre

      # Update exc synaptic currents
      gee = gee + Jee[:, Ispike].sum(axis=1) / taue
      gie = gie + Jie[:, Ispike].sum(axis=1) / taue

      # Update cumulative number of e spikes
      nespike = nespike + len(Ispike)

    # Find which I neurons spiked
    Ispike = np.nonzero(Vi >= Vth)[0]
    if Ispike.any() and not (TooManySpikes):
      # Store spike times and neuron indices
      if nispike + len(Ispike) <= maxns:
        si[0, nispike:nispike + len(Ispike)] = dt * i
        si[1, nispike:nispike + len(Ispike)] = Ispike
      else:
        TooManySpikes = True

      # Reset i mem pot.
      Vi[Ispike] = Vre

      # Update inh synaptic currents
      gei = gei + Jei[:, Ispike].sum(axis=1) / taui
      gii = gii + Jii[:, Ispike].sum(axis=1) / taui

      # Update cumulative number of i spikes
      nispike = nispike + len(Ispike)

    if TooManySpikes:
      print('Too many spikes. Exiting sim at time t =', i * dt)
      break

    # Euler update to synaptic currents
    gee = gee - dt * gee / taue
    gei = gei - dt * gei / taui
    gie = gie - dt * gie / taue
    gii = gii - dt * gii / taui
    gex = gex - dt * gex / taux
    gix = gix - dt * gix / taux


    Ve[~np.isfinite(Ve)]=Vth
    Vi[~np.isfinite(Vi)]=Vth
    ii=IntDivide(i,nBinsRecord)

    VeRec[ii, :] += np.minimum(Ve[IeRecord],Vth)
    ViRec[ii, :] += np.minimum(Vi[IiRecord],Vth)
    #VeFreeRec[ii, :] += VeFree[IeRecord]
    #ViFreeRec[ii, :] += ViFree[IiRecord]
    geeRec[ii, :] += gee[IeRecord]
    geiRec[ii, :] += gei[IeRecord]
    gieRec[ii, :] += gie[IiRecord]
    giiRec[ii, :] += gii[IiRecord]
    gexRec[ii, :] += gex[IeRecord]
    gixRec[ii, :] += gix[IiRecord]

  Recording = {}
  Recording['Ve'] = VeRec/nBinsRecord
  Recording['Vi'] = ViRec/nBinsRecord
  #Recording['VeFree'] = VeFreeRec/nBinsRecord
  #Recording['ViFree'] = ViFreeRec/nBinsRecord

  Recording['gee'] = geeRec/nBinsRecord
  Recording['gei'] = geiRec/nBinsRecord
  Recording['gie'] = gieRec/nBinsRecord
  Recording['gii'] = giiRec/nBinsRecord
  Recording['gex'] = gexRec/nBinsRecord
  Recording['gix'] = gixRec/nBinsRecord

  return se, si, Recording

