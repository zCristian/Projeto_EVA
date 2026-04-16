import numpy as np
import matplotlib.pyplot as plt
from typing import Optional

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

def PowerWeight_statistical(type_aircraft: str = 'GA-single-engine')-> float:
    """
    Define, através da Tabela 5.2 do Raymer, uma estimativa de Potencia-Peso 
    de acordo com o tipo de aeronave.
    Esses valores são com base em configuração de potência máxima em condições
    estáticas, no nível do mar.
    
    Args:
        type_aircraft (str): Tipo da aeronave.
    Return:
        Valor estatístico da razão Potência-Peso de acordo com o tipo da 
        aeronave. [hp/lb]
        Caso a função não apresente valor estatístico. Retorna -1 e deve-
        se impelemntar outros valores.
    """
    if type_aircraft == 'GA-single-engine':
        return 0.07 # [hp/lb]
    else:
        print('Adicione um novo tipo de aeronave na função.')
        return -1

def PW_Vmax (V_max_fts: float,
             alfa: float = 0.025,
             C: float = 0.22) -> float:
        """
        Tabela 5.4 do Raymer estabelece relacao estatistica de Potencia-Peso 
        com base na velocidade maxima (em kt). Lembrando que é a razão potên-
        cia por peso máximo (W0).
        
        Args:
            alfa  (float): coef Tabel 5.4
            C     (float): coef Tabel 5.4
            V_max_fts (float): max airspeed [ft/sec]
        
        Return:
            PW0   (float): takeoff Power-to-Weight ratio [hp/lb]
        """
        # convertendo ft/sec para kt
        V_max_kt = V_max_fts/1.688
        
        PW0 = alfa * (V_max_kt)**C
        
        return PW0
    
def plot_PW_Vmax(V_max: list,
                 PW: list) -> None:
    
    """
    Plota os gráficos de Potência-Peso por Velocidade Máxima.
    Args:
        V_max (list): Lista das velocidades máximas a serem analisadas.
        PW    (list): Lista das razões Potência-Peso correspondentes.
        
    """
    
    plt.figure(figsize=(10,6))
    plt.plot(V_max, PW, label="Razão Potência-Peso", color="blue", linewidth=2)
    plt.title('Variação da Razão Potência-Peso em função da Velocidade', fontsize=14)
    plt.xlabel('Velocidade (V)', fontsize=12)
    plt.ylabel('Razão Potência-Peso (P/W)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()
    
    return None
    
def Thrust_Matching_cruise(L_D_cruise: float,
                           V_cruise: float,
                           eta_p: float = 0.8) -> float:
    """
    Equacao 5.2 do Raymer. Verificar Potencia-Peso para cruzeiro.
    L/D_cruise vem do valor calculado na Entrega 1 do trabalho.
    
    Args:
        L_D_cruise (float): Lift-to-Drag ratio           [lb/lb]
        eta_p      (float): Propeller efficiency         [-]
        V_cruise   (float): airspeed in cruise           [ft/sec]
    
    Return:
        TW_cruise  (float): cruise Thrust-to-Weight ratio [lb/lb]
        PW_cruise  (float): cruise Power-to-Weight ratio [hp/lb]
    """
    
    TW_cruise = 1 / (L_D_cruise)
    PW_cruise = Thrust2Power_Weight(TW_cruise, V_cruise, eta_p)
    
    return TW_cruise, PW_cruise

def Thrust_Climb(L_D_climb: float,
                 V_vertical: float,
                 V: float):
    """
    Calcula a tracao em subida (climb).
    Args:
        L_D_climb  (float): Razao sustentacao-arrasto na config de subida [-]
        V_vertical (float): Velocidade vertical [ft/min]
        V          (float): Velocidade da aeronave durante subida [ft/sec]
    Return:
        TW_climb   (float): Razao tracao-peso para subida [lb/lb]
        PW_climb   (float): Razao potencia-peso para subida [hp/lb]
    """
    V_vertical = V_vertical/60 # convertendo ft/min para ft/sec
    TW_climb = 1/L_D_climb + V_vertical/V
    PW_climb = Thrust2Power_Weight(TW=TW_climb, V=V, eta_p=0.75)
    
    return TW_climb, PW_climb

def Thrust_Matching_takeoff(PW_cruise: float,
                            TW_cruise: float,
                            W1W0: float = 0.97,
                            W2W1: float = 0.985,
                            Tcruise_Tto: float = 0.70) -> float:
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
    
    TW_takeoff = TW_cruise * Wcruise_Wtakeoff / Tcruise_Tto
    PW_takeoff = PW_cruise * Wcruise_Wtakeoff / Tcruise_Tto # verificar
    
    return TW_takeoff, PW_takeoff

def powerEstimate(W0: float,
                  W1: float,
                  W2: float,
                  V_cruise_fts: float,
                  LD_cruise: float,
                  V_max: Optional[float] = None):
    
    Power_selected = []
    V_selected = [] # velocidade para cada potencia relacionada
    
    # Passo 1: Estimativa com base em dados históricos
    PW_statistical = PowerWeight_statistical(type_aircraft='GA-single-engine')
    
                # PRECISAMOS SABER QUAL PESO É UTLIZADO NESSA FASE (por enquanto vou considerar W0)
    Power_selected.append(PW_statistical * W0)
    V_selected.append(0) # Zero, porque se essa for a maior potencia, iremos desconsiderar, estará 
                         # superestimando o projeto
    ###############################################################################################
    
    # Passo 2: Calculo de acordo com velocidade máxima
    
    if V_max == None:       
            # Como no nosso projeto, a velocidade máxima não é um requisito, mas a velo-
            # cidade de cruzeiro, sim (250 km/h). Iremos fazer um estudo. Irá ser plota-
            # do um gráfico de P/W por Velocidade máxima. 
            
            # Estatisticamente, V_max fica entre 16% e 43% acima da velocidade de cruzeiro.
            # Considere que a velocidade máxima varia entre a velocidade de cruzeiro e 
            # um valor que representa cerca de 54% acima da velocidade de cruzeiro.
        VmaxList = np.linspace(V_cruise_fts, V_cruise_fts/0.65, 20)
        PWlist = PW_Vmax(VmaxList, alfa=0.025, C=0.22)
        plot_PW_Vmax(V_max=VmaxList, PW=PWlist)
        
        V_max = float(input('Selecione a Velocidade Máxima [ft/sec] desejada no projeto: '))
        PW_max_airspeed = PW_Vmax(V_max_fts=V_max, alfa=0.025, C=0.22)
    
    else:
        PW_max_airspeed = PW_Vmax(V_max_fts=V_max, alfa=0.025, C=0.22)
    
    Power_selected.append(PW_max_airspeed * W0)
    V_selected.append(V_max)
    ###############################################################################################
    
    # Passo 3: Calculo de Potencia necessária em cruzeiro
    TW_cruise, PW_cruise = Thrust_Matching_cruise(L_D_cruise = LD_cruise, V_cruise= V_cruise_fts, eta_p=0.8)
    
    Power_selected.append(PW_cruise * W2)
    V_selected.append(V_cruise_fts)
    ###############################################################################################
    # Passo 4: Calculo Potencia necessaria para subida
        # Como escolher L/D para subida? V_vertical? V?
    TW_climb, PW_climb = Thrust_Climb(L_D_climb=15, V_vertical=100, V=190)
    Power_selected.append(PW_climb * W1)
    ###############################################################################################
    
    # Passo 5: Calculo Potencia necessaria na decolagem com base na potencia em cruzeiro
    PW_takeoff = Thrust_Matching_takeoff(PW_cruise= PW_cruise, TW_cruise= TW_cruise, W1W0=0.97, W2W1=0.985, Tcruise_Tto=0.7)[1]
    
    Power_selected.append(PW_takeoff * W0)
    V_selected.append(-1) # se esse for a maior potencia requerida, vamos precisar de algo para calcular a Vstall
    ###############################################################################################
    
    print('##### RAZAO POTENCIA-PESO #####')
    print(f'P/W estatístico:       {PW_statistical:.5f} [hp/lb]')
    print(f'P/W velocidade máxima: {PW_max_airspeed:.5f} [hp/lb], com Velocidade Máxima de {V_max:.1f} ft/s')
    print(f'P/W cruzeiro:          {PW_cruise:.5f} [hp/lb]')
    print(f'P/W subida:            {PW_climb:.5f} [hp/lb]')
    print(f'P/W decolagem:         {PW_takeoff:.5f} [hp/lb]')
    print()
    
    print('##### POTENCIAS CALCULADAS #####')
    print(f'P estatístico:       {Power_selected[0]:.2f} [hp]')
    print(f'P velocidade máxima: {Power_selected[1]:.2f} [hp]')
    print(f'P cruzeiro:          {Power_selected[2]:.2f} [hp]')
    print(f'P subida:            {Power_selected[3]:.2f} [hp]')
    print(f'P decolagem:         {Power_selected[4]:.2f} [hp]')
    
    
    return max(Power_selected), PW_max_airspeed, TW_climb