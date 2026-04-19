# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:46:03 2026

@author: Vinícius Soares
"""

import numpy as np
from scipy.optimize import fsolve
from parameters import *

results = Estimatives()
results_updated = Estimatives_updated()
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

################## UPDATED EQUATIONS ################## 
def updated_WeW0(W0):
    wew0 = a + b * (W0 ** C1) * (A ** C2) * (hpW0 ** C3) * (W0S ** C4) * (Vmax ** C5)
    results_updated.wew0 = wew0
    return wew0

def updated_W2W1():
    w2w1 = 1.0065 - 0.0325 * M
    #w2w1 = 0.985
    results_updated.w2w1 = w2w1
    return w2w1

def updated_Wf(W1, W2):
    Wf = 1.06 * ((1 - updated_W2W1()) * W1 + (1 - Wcruise()) * W2)
    results_updated.wf = Wf
    results_updated.wfw0 = Wf/W1
    return Wf

# Iterative solution for W0
def func_updated(W0):
    W1 = W0
    W2 = updated_W2W1() * W1
    W3 = Wcruise() * W2
    We = updated_WeW0(W0) * W0
    results_updated.wcruise = Wcruise()

    results_updated.w2 = W2
    results_updated.we = We
    results_updated.w3 = W3

    return W0 - Wcrew - Wpay - updated_Wf(W1, W2) - updated_WeW0(W0) * W0