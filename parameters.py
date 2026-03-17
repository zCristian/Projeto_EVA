# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:46:33 2026

@author: Vinícius Soares
"""

Wcrew = 10800 # Wcrew
Wpay = 0 # Wpayload
W1W0 = 0.97 # Warmup and takeoff
W2W1 = 0.985 # Climb
W5W4 = 0.995 # Land


# Aircraft parameters
A = 0.93 # Table 3.1
C = -0.07 # Table 3.1
Kvs = 1 # Table 3.1
Kld = 1
Swet = 1
Sref = 1.02

Ccbhp = 0.4 # Propeller cruise Cbhp - Table 3.4
Ccnp = 0.8 # Propeller cruise Np - Table 3.4

Clbhp = 0.5 # Propeller loiter Cbhp - Table 3.4
Clnp = 0.7 # Propeller loiter Np - Table 3.4

# Mission parameters
R = 100 # Range
V = 10 # Cruise velocity
E = 1 # Loiter time
