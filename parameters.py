# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:46:33 2026

@author: Vinícius Soares
"""

import numpy as np
from dataclasses import dataclass
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


@dataclass

class ConstraintsParameters:
    
    # Wing loading range for T/W curves:
    WS = np.linspace(1, 100, 200)     # [lbf/ft²]

    # Stall Speed Criteria:
    rho_stall: float = 0.002378         # [slug/ft³]  //sea level
    v_stall: float = 90                 # [ft/s]
    cl_max_stall: float = 1.8           # [-]

    # Cruise Speed Criteria:
    q_cruise: float = 50.67           # [lbf/ft²]  //pho=0.0019528281740147837 V=227,8
    cd_min_cruise: float = 0.02       # [-]
    k_ind_cruise: float = 0.04        # [-]        //e=0.8 AR=10

    # Rate of Climb Criteria:
    v_vertical_climb: float = 1.2*v_stall*0.1    # [ft/s]
    v_inf_climb: float = 1.2*v_stall                                # [ft/s]     //V_inf = 1.2V_stall
    q_climb: float = 7.976                                          # [lbf/ft²]  //pho=0.0021568512825572957 V=86.4
    cd_min_climb: float = 0.02                                      # [-]
    k_ind_climb: float = 0.04                                       # [-]

    # Level Constant Velocity Turn Criteria:
    q_turn: float = 35.0              # [lbf/ft²]
    n_turn: float = 2.0               # [-]
    cd_min_turn: float = 0.02         # [-]
    k_ind_turn: float = 0.06          # [-]

    # Service Ceiling Criteria: (Gudmundsson 3-11)
    #v_y_ceiling: float = 160.0       # [ft/s]
    q_ceiling:      float = 50.67     # [lbf/ft²]  //pho=0.0019528281740147837 V=227,8
    cd_min_ceiling: float = 0.02      # [-]
    k_ind_ceiling:  float = 0.04      # [-]

    # Service Ceiling Criteria: (Gudmundsson Slide)
    v_vertical:  float = 100/60       # [ft/s]  
    rho_ceiling: float = 0.00195      # [slug/ft³] // 2000m

    # T-O Ground Run Distance Criteria  
    cl_max_to:      float = 1.8           # [-]
    cl_to:          float = 0.8*cl_max_to # [-]
    cd_to:          float = 0.08          # [-]
    rho_to:         float = 0.00215       # [slug/ft³] //1000m
    #q_to:           float = 5            # [lbf/ft²] 
    sg:             float = 196.85        # [ft]
    friction_const: float = 0.04          # [-]
    g_acc:          float = 32.174        # [ft/s²]
