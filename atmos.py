import numpy as np

def T_altitude (h_ft: float) -> float:
    """
    Calcula Temperatura de acordo com a altitude.
    Modelo ISA.
    Args:
        h_ft    (float): altitude          [ft]
    Return:
        T_local (float): Temperatura local [K]
        razaoT  (float): Razao Temperatura local por Temperatura ao nivel do mar
    """
    
    h_m = h_ft/0.3048  # [m]
    
    assert h_m <= 11000, 'Acima dessa altitude, as propriedades se comportam de maneira diferente.'
    
    T0  = 288.15    # [K]
    la  = 0.0065    # [K/m]
    
    T_local = T0 - la*h_m # [K]
    razaoT = T_local/T0
    
    return T_local, razaoT

def rho_altitude(h_ft: float) -> float:
    """
    Calcula a densidade do ar de acordo com a altitude.
    Modelo ISA.
    Args:
        h_ft      (float): altitude          [ft]
    Return:
        rho_local (float): densidade local [slug/ft3]
        razaoRho  (float): Razao densidade local por densidade ao nivel do mar
        
    """
    
    assert h_ft <= 11000*0.3048, 'Acima dessa altitude, as propriedades se comportam de maneira diferente.'
    
    g0 = 9.80665 # [m/s2]
    R  = 287.05  # [J/kg.K]
    rho0 = 1.225 # [kg/m3]
    la = 0.0065  # [K/m]
    fracT = T_altitude(h_ft)[1]
    
    rho_local = rho0 * fracT **( g0/(la*R)-1) # [kg/m3]
    rho_local_slugft3 = rho_local/515.4       # [slug/ft3]
    
    razaoRho = rho_local/rho0
    
    return rho_local_slugft3, razaoRho