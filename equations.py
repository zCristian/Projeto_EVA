# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:46:03 2026

@author: Vinícius Soares
"""

import numpy as np
from scipy.optimize import fsolve

from parameters import *

################## FUEL EQUATIONS ##################

# W0 Equation - Equation 3.4
def W0Eq():    
    W0 = (Wcrew + Wpay) / (1 - WfW0() - WeW0Eq())    
    return W0

# Empty weight fraction equation (We/W0) - Equation Table 3.1
def WeW0Eq():    
    WeW0 = A * (W0Eq() ** C) * Kvs    
    return WeW0

# Cruise weight fraction - Equation 3.6
def Wcruise():
    return np.exp(-R * Cc() / (V * LDc()))

# Loiter weight fraction - Equation 3.8
def Wloiter():
    return np.exp(-E * Cl() / LDl())

# Segment weight fraction equation - Section 3.4
def Wsegments():     
    return W1W0 * W2W1 * Wcruise() * Wloiter() * W5W4   

# Fuel-fraction - Equation 3.11 - Assuming 6% allowence for reserve and trapped fuel
def WfW0():
    return 1.06 * (1 - Wsegments())

# Iterative solution for W0
def func(W0):
    return W0 - (Wcrew + Wpay) / (1 - WfW0() - A * (W0 ** C) * Kvs)

################## GEOMETRY EQUATIONS ##################

# Wetted Aspect ratio - Equation Fig. 3.6
def WAR():    
    WAR = A / (Swet / Sref)    
    return WAR

# L/Dmax Equation
def LDmax():    
    LDmax = Kld * np.sqrt(A / (Swet / Sref))    
    return LDmax

# L/D cruise equation for propeller
def LDc():
    return LDmax()

# L/D loiter equation for propeller
def LDl():
    return 0.866 * LDmax()

################## PARAMETERS EQUATIONS ##################

# Propeller cruise specific fuel consumption - Equation 3.10
def Cc():
    return Ccbhp * V / (550 * Ccnp)

# Propeller loiter specific fuel consumption - Equation 3.10
def Cl():
    return Clbhp * V / (550 * Clnp)
