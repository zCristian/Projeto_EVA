# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:46:03 2026

@author: Vinícius Soares
"""

import numpy as np
from scipy.optimize import fsolve

from parameters import *

results = Estimatives()
AR = AspectRatio()

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
    cc = float(Cc())
    ldc = float(LDc())
    wcruise = np.exp(-R * cc / (V * ldc))
    results.wcruise = wcruise
    return wcruise

# Segment weight fraction equation - Section 3.4
def Wsegments(): 
    Wseg = W1W0 * W2W1 * Wcruise() 
    results.wseg = Wseg
    return Wseg

# Fuel-fraction - Equation 3.11 - Assuming 6% allowence for reserve and trapped fuel
def WfW0():
    wfw0 = 1.06 * (1 - Wsegments())
    results.wfw0 = wfw0
    return wfw0

# Iterative solution for W0
def func(W0):
    return W0 - (Wcrew + Wpay) / (1 - WfW0() - A * (W0 ** C) * Kvs)

################## GEOMETRY EQUATIONS ##################

# Wetted Aspect ratio - Equation Fig. 3.6
def WAR():    
    WAR = AR.value / (SwetSref)  
    print("WAR: ", WAR)  
    return WAR

# L/Dmax Equation
def LDmax():  
    print()  
    LDmax = Kld * np.sqrt(AR.value / (SwetSref))  
    results.ldmax = LDmax
    return LDmax

# L/D cruise equation for propeller
def LDc():
    ldc = LDmax()
    results.ldc = ldc
    return ldc

################## PARAMETERS EQUATIONS ##################

# Propeller cruise specific fuel consumption - Equation 3.10
def Cc():
    cc = Ccbhp * V / (550 * Ccnp)
    results.Cc = cc
    return cc