import numpy as np

def Power2Thrust_Weight(PW:    float,
                        V:     float,
                        eta_p: float = 0.8) -> float:
    """
    Converte Tracao-Peso em Potencia-Peso.
    Aeronaves a pistão utilizam o conceito de potencia em HP ao inves de tracao em lb.
    
    Args:
        PW    (float): Power-to-Weight ratio [HP/lb]
        eta_p (float): Propeller efficiency  [-]
        V     (float): Airspeed [ft/sec]
    
    Returns:
        TW    (float): Thrust-to-Weight ratio [lb/lb]
    """
    
    TW = 550*eta_p*PW/V
    
    return TW

def Thrust2Power_Weight(TW:    float,
                        V: float,
                        eta_p: float = 0.8) -> float:
    """
    Converte Tracao-Peso em Potencia-Peso.
    Aeronaves a pistão utilizam o conceito de potencia em HP ao inves de tracao em lb.
    
    Args:
        TW    (float): Thrust-to-Weight ratio [lb/lb]
        eta_p (float): Propeller efficiency  [-]
        V     (float): Airspeed [ft/sec]
    
    Returns:
        PW    (float): Power-to-Weight ratio [HP/lb]
    """
    
    PW = TW*V / (550*eta_p)
    
    return PW

def PW_Vmax (V_max: float,
             alfa: float = 0.025,
             C: float = 0.22) -> float:
    
        """
        Tabela 5.4 do Raymer estabelece relacao estatistica de Potencia-Peso 
        com base na velocidade maxima (em kt).
        
        Args:
            alfa  (float): coef Tabel 5.4
            C     (float): coef Tabel 5.4
            V_max (float): airspeed [ft/sec]
        
        Return:
            PW0   (float): takeoff Power-to-Weight ratio [hp/lb]
        """
        # convertendo ft/sec para kt
        V_max_kt = V_max/1.688
        
        PW0 = alfa * (V_max_kt)**C
        
        return PW0
    
def Thrust_Matching_cruise(L_D_cruise: float,
                           V_cruise: float,
                           eta_p: float = 0.8) -> float:
    """
    Equacao 5.2 do Raymer. Verificar Potencia-Peso para cruzeiro.
    L/D_cruise vem do valor calculado na Entrega 1 do trabalho
    
    Args:
        L_D_cruise (float): Lift-to-Drag ratio           [lb/lb]
        eta_p      (float): Propeller efficiency         [-]
        V_cruise   (float): airspeed in cruise           [ft/sec]
    
    Return:
        TW_cruise  (float): cruise Thrust-to-Weight ratio [lb/lb]
        PW_cruise  (float): cruise Power-to-Weight ratio [hp/lb]
    """
    
    TW_cruise = 1 / (L_D_cruise)
    PW_cruise = Thrust2Power_Weight(TW_cruise, eta_p, V_cruise)
    
    return TW_cruise, PW_cruise

def Thrust_Matching_takeoff(PW_cruise: float,
                            TW_cruise: float,
                            W1W0: float = 0.97,
                            W2W1: float = 0.985,
                            Tto_Tcruise: float = 0.70) -> float:
    """
    Calculou-se a tracao em cruzeiro. Necessita-se da tracao na decolagem.
    
    Args:
        PW_cruise   (float): Calculado no Thrust_Matching [hp/lb]
        TW_cruise   (float): Calculado no Thrust_Matching [lb/lb]
        W1W0        (float): #razao da primeira etapa da missao (decolagem), Raymer define 0.97
        W2W1        (float): #razao da segunda etapa da missao (climb), Raymer define 0.985
        Tto_Tcruise (float): #razao tracao de decolagem e tracao de cruzeiro, valores variam de
                              [0.60-0.80], se possivel, verificar se tem dados dos fabricantes
    Return:
        TW_takeoff  (float):  takeoff Thrust-to-Weight ratio [lb/lb]
        PW_takeoff  (float):  takeoff Power-to-Weight ratio  [hp/lb]
    """
    Wcruise_Wtakeoff = W1W0*W2W1
    
    TW_takeoff = TW_cruise * Wcruise_Wtakeoff * Tto_Tcruise
    PW_takeoff = PW_cruise * Wcruise_Wtakeoff * Tto_Tcruise
    
    return TW_takeoff, PW_takeoff

def motorPower(PW: float,
               W0: float)-> float:
    """
    Calcula potencia do motor.
    
    Args:
        PW      (float): higher power-to-weight ratio [hp/lb]
        W0      (float): MTOW                         [lb]
        
    Return:
        P_motor (float): motor power                  [hp]
    """
    P_motor = PW*W0
    
    return P_motor
