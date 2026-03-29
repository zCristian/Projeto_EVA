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
#W5W4 = 0.995 # Land

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
Hc = 2000 * 3.28084 # Teto de serviço (ft)

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
            f"Cc: {self.Cc}"
        )


