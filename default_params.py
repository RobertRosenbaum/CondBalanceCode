
import numpy as np

print('Setting default parameters.')


# Connection weights
jee = 17.5
jei = -100.0
jie = 60.0
jii = -150.0
jex = 100.0
jix = 75.0

taujitter=5

# qx=Nx/N
qx=0.3

# Connection probabilities
p=0.2
P = np.array([[p, p], [p, p]])
Px = np.array([[p], [p]])

# Synaptic timescales
taue = 8.0
taui = 4.0
taux = 10.0

# Rate of external population
rx=10/1000

# EIF Neuron Parameters
NeuronParams = {}
NeuronParams['Cm'] = 1.0
NeuronParams['gL'] = 1/15.0
NeuronParams['EL'] = -72.0
NeuronParams['Vth'] = -50.0
NeuronParams['Vre'] = -75.0
NeuronParams['Vlb'] = -np.inf#-80.0
NeuronParams['DeltaT'] = 1.0
NeuronParams['VT'] = -55.0


NeuronParamsCond = NeuronParams.copy()
NeuronParamsCond['Ee'] = 0.0
NeuronParamsCond['Ei'] = -80.0


# For spike count correlation
winsize=250


# Synaptic time constants
tau = np.array([taue,taui,taux])

# Connection weights for conductance-based sims
Vref = NeuronParams['EL']
Ee=0
Ei=-80
jeeCond = jee/(Ee-Vref)
jeiCond = jei/(Ei-Vref)
jieCond = jie/(Ee-Vref)
jiiCond = jii/(Ei-Vref)
jexCond = jex/(Ee-Vref)
jixCond = jix/(Ee-Vref)

Q = np.array([[0.8,0.2],[0.8,0.2]])

Wmf = np.array([[jee, jei], [jie, jii]])*Q*P
Wxmf = np.array([[jex], [jix]])*qx*Px
rBal = -np.linalg.inv(Wmf)@Wxmf*rx
