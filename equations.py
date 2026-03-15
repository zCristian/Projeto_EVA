# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:46:03 2026

@author: Vinícius Soares
"""

import numpy as np

# W0 Equation - Equation 3.4
def W0Eq(Wc, Wp, WfW0, WeW0):
    
    W0 = (Wc + Wp) / (1 - WfW0 - WeW0)
    
    return W0

# Empty weight fraction equation (We/W0) - Equation Table 3.1
def WeW0Eq(A, W0, C, Kvs):
    
    WeW0 = A * W0 ** C * Kvs
    
    return WeW0

# Fuel fraction equation (Wf/W0) - Section 3.4
def WfW0(W1W0, W2W1, R, E, C, V, LD):
    
    W3W2 = np.exp(- R * C / (V * LD)) # Equation 3.6
    
    WfW0 = W1W0 * W2W1 * W3W2
    
    return WfW0

# Wetted Aspect ratio - Equation Fig. 3.6
def WAR(A, Swet, Sref):
    
    WAR = A / (Swet / Sref)
    
    return WAR

# L/Dmax Equation
def LDmax(Kld, A, Swet, Sref):
    
    LDmax = Kld * np.sqrt(A / (Swet / Sref))
    
    return LDmax
