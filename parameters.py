# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:46:33 2026

@author: Vinícius Soares
"""

import numpy as np

Wcrew = 0 # Wcrew
Wpay = 60 * 2.2046 # Wpayload (lb)
W1W0 = 0.97 # Warmup and takeoff
W2W1 = 0.985 # Climb

# Aircraft parameters
A = 1.67 # Table 3.1 Raymer
C = -0.16 # Table 3.1 Raymer
Kvs = 1 # Table 3.1 Raymer
Kld = 11
SwetSref = 3.5

Ccbhp = 0.4 / 3600 # Propeller cruise Cbhp - Table 3.4 (1/s)
Ccnp = 0.8  # Propeller cruise Np - Table 3.4

# Mission parameters
R = 2000 * 3280.8399 # Range (ft)
V = 250 * 0.91134 # Cruise velocity (ft/s)
Vsound = np.sqrt(1.4 * 287 * 275) * 3.28084 # Sound velocity (ft/s)
M = V / Vsound
Hc = 2000 * 3.28084 # Teto de serviço (ft)

# Calculated values
hpW0 = 0.046
W0S = 20
Vmax = 280 * 0.539 # kt

class AspectRatio:
    value = float

class Estimatives:
    wcruise = float
    wseg = float
    wew0 = float
    wfw0 = float
    ldc = float
    ldmax = float
    w0 = float
    w1 = float
    w2 = float
    w3 = float
    wf = float
    we = float 
    Cc = float

    def __str__(self):
        return (
            f"wcruise: {self.wcruise}\n"
            f"wseg: {self.wseg}\n"
            f"wew0: {self.wew0}\n"
            f"wfw0: {self.wfw0}\n"
            f"ldc: {self.ldc}\n"
            f"ldmax: {self.ldmax}\n"
            f"w0: {self.w0}\n"
            f"w1: {self.w1}\n"
            f"w2: {self.w2}\n"
            f"w3: {self.w3}\n"
            f"wf: {self.wf}\n"
            f"we: {self.we}\n"
            f"Cc: {self.Cc}"
        )

class Estimatives_updated:
    w2w1 = float
    wcruise = float
    wew0 = float
    wfw0 = float
    wf = float
    w0 = float
    w2 = float
    w3 = float
    we = float 

    def __str__(self):
        return (
            f"w2w1: {self.w2w1}\n"
            f"wcruise: {self.wcruise}\n"
            f"wew0: {self.wew0}\n"
            f"wfw0: {self.wfw0}\n"
            f"wf: {self.wf}\n"
            f"w0: {self.w0}\n"
            f"w2: {self.w2}\n"
            f"w3: {self.w3}\n"
            f"we: {self.we}"
        )