import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import atmos

def wingLoading_statistical(type_aircraft: str = 'GA-single-engine')-> float:
    """
    Define, através da Tabela 5.5 do Raymer, uma estimativa de carga alar de 
    acordo com o tipo de aeronave.  
    Args:
        type_aircraft (str): Tipo da aeronave.
    Return:
        Valor estatístico da razão Potência-Peso de acordo com o tipo da 
        aeronave. [hp/lb]
        Caso a função não apresente valor estatístico. Retorna -1 e deve-
        se impelemntar outros valores.
    """
    if type_aircraft == 'GA-single-engine':
        return 17 # [lb/ft2]
    else:
        print('Adicione um novo tipo de aeronave na função wingLoading_statistical().')
        return -1
    
def WS_stall_speed(V_stall: float,
                   CLmax: float,
                   h: float) -> float:
    """
    Carga alar necessária, considerando velocidade a qual a sustentação se equilibra
    com o peso da aeronave.
    Args:
        V_stall (float): Velocidade de estol definida [ft/sec]
        CLmax   (float): Coef de sustentação definido [-]
        h       (float): Altitude em que se encontra a aeronave [ft]
    Return:
        WS      (float): Carga alar [lb/ft2]
    """
    rho = atmos.rho_altitude(h_ft= h)[0]
    
    return 0.5 * rho * (V_stall**2) * CLmax

def WS_stall_speed_study()-> None:
    CLmax_values = np.linspace(1.2, 2.4, 6)
    V_stall_kt = np.linspace(5, 61*1.68781, 20)
    h_m_values = np.linspace(0, 1000, 3)
    
    # ── Fatores de conversão ─────────────────────────────────────────────────────
    
    KT_TO_FT_S = 1.68781    # 1 kt = 1.68781 ft/s
    M_TO_FT    = 3.28084    # 1 m  = 3.28084 ft
    
    # Conversões para unidades imperiais
    V_stall_ft_s = V_stall_kt * KT_TO_FT_S   # [ft/s]
    h_ft_values  = h_m_values * M_TO_FT       # [ft]
    
    
    # ── Estilo ───────────────────────────────────────────────────────────────────
    
    colors     = cm.viridis(np.linspace(0.15, 0.9, len(CLmax_values)))
    linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 1))]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    fig.suptitle('Carga Alar W/S em função de V_stall', fontsize=14, y=1.01)
    
    
    # ── Plotagem ─────────────────────────────────────────────────────────────────
    
    for ax, h_m, h_ft in zip(axes, h_m_values, h_ft_values):
    
        for CL, color, ls in zip(CLmax_values, colors, linestyles):
    
            WS_values = np.array([
                WS_stall_speed(V_ft_s, CL, h_ft)
                for V_ft_s in V_stall_ft_s
            ])
    
            ax.plot(
                V_stall_kt,
                WS_values,
                color=color,
                linestyle=ls,
                linewidth=1.8,
                label=f'CLmax = {CL:.2f}'
            )
    
        ax.set_title(f'h = {int(h_m)} m', fontsize=12)
        ax.set_xlabel('V_stall [kt]', fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.set_xlim(V_stall_kt[0], V_stall_kt[-1])
        ax.set_ylim(bottom=0)
        ax.tick_params(labelsize=9)
    
    axes[0].set_ylabel('W/S [lb/ft²]', fontsize=11)
    
    # Legenda única à direita
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc='center right',
        bbox_to_anchor=(1.13, 0.5),
        frameon=True,
        fontsize=9,
        title='CLmax',
        title_fontsize=9
    )
    
    plt.tight_layout()
    plt.savefig('ws_stall_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Gráfico salvo em: ws_stall_analysis.png")
 
def WS_TO_distance(CLmax: float,
                   SG: float,
                   h: float,
                   PW: float)-> float:
    """
    Calcula carga alar necessária confomre distância de decolagem.
    Args:
        CLmax (float): coef de sustentacao max [-]
        SG    (float): distancia de decolagem  [ft]
        h     (float): altitude na decolagem   [ft]
        PW    (float): razao potencia-peso na decolagem [hp/lb]
    Return:
        WS    (float): Carga alar [lb/ft2]
    """
    sigma = atmos.rho_altitude(h_ft=h)[1]
    CL_to = CLmax/1.21
    # Para propeller, temos o parâmetro Takeoff Parameter
    # Dados tirados dos slides do Cuenca
    a, b, c = 12.87, 0.1395, -4.55E-3
    TOP = a + b*SG + c* SG**2
    
    return TOP * sigma * CL_to * PW
    
def WS_catapult_to(h: float,
                   CLmax: float,
                   Vend: float,
                   Vwod: float,
                   Vthurst: float)->float:
    """
    Calcula carga alar para decolagem em uma catapulta.
    Args:
        h       (float): altitude de decolagem [ft]
        CLmax   (float): coef de sustentacao max [-]
        Vend    (float): velocidade de saída da catapulta [ft/sec]
        Vwod    (float): velocidade wind-over-deck [ft/sec]
        Vthrust (float): variacao de velocidade proporcionada pelo motor [ft/sec]
    Return:
        WS      (float): Carga alar [lb/ft2]
    """
    rho = atmos.rho_altitude(h_ft=h)[0]
    
    return 0.5 * rho * (Vend+Vwod+Vthurst)**2 * CLmax/1.21
    
def WS_cruise(AR: float,
              h: float,
              V: float,
              e: float = 0.8)->float:
    """
    Calcula carga alar para aeronave em cruzeiro com máximo alcance.
    Args:
        AR    (float): Razao de aspecto [-]
        h     (float): altitude de cruzeiro [ft]
        V     (float): velocidade de cruzeiro [ft/sec]
        e     (float): Fator de eficiencia de Oswald [-]
    Return:
        WS    (float): Carga alar [lb/ft2]
    """
    CD0 = 0.02 # aproximacao para aeronave propeller limpa
    rho = atmos.rho_altitude(h_ft= h)[0]
    q = 0.5 * rho * V**2
    
    return q * np.sqrt(np.pi * AR * e * CD0)

def WS_climb_glide(TW_climb: float,
                   G: float,
                   CD0: float,
                   AR: float,
                   e: float,
                   h_ft: float,
                   V: float)-> float:
    """
    Calcula carga alar para subida e planeio.
    Note que CD0 e 'e' devem incluir efeitos de flapes e trem de pouso.
    Args:
        TW_climb (float): razao tracao-peso para subida [lb/lb]
        G        (float): taxa de subida [ft/min]
        CD0      (float): arrasto com AoA=0 [-]
        AR       (float): razao de aspecto [-]
        e        (float): fator de eficiencia de Oswald [-]
        h_ft     (float): altitude da operacao [ft]
    Return:
        WS       (float): Carga alar [lb/ft2]
    """
    
    G = G/60 # converte ft/min para ft/sec
    
    assert TW_climb >= G * 2* np.sqrt(CD0 / (np.pi*AR*e)), "Motor nao é suficiente para essa taxa de subida"
    
    rho = atmos.rho_altitude(h_ft=h_ft)[0]
    q = 0.5*rho*V**2
    
    # verificar os valores para +ou- raiz
    return (TW_climb - G + np.sqrt((TW_climb-G)**2 - 4*CD0/(np.pi*AR*e) ) ) / (2 / (q*np.pi*AR*e))

def WS_estimate(W0:float,
                W1: float,
                W2: float,
                SG_m: float,
                PW: float,
                AR: float,
                h_cruise: float,
                V_cruise: float,
                ROC: float, 
                TW_cl: float)-> float:
    
    WS_list =[]
    S_list=[]
    
    # Passo 1: Determinar valores estatísticos para o tipo de aeronave
    WS_statistical = wingLoading_statistical(type_aircraft='GA-single-engine')
    WS_list.append(WS_statistical)
    S_list.append(W0/WS_statistical)
    
    # Passo 2: Determinar WS confrome velocidade de estol
        # Como não temos velocidade de estol e CLmax definidos, iremos fazer um estudo
        # e, após isso, determinar valores que fazem mais sentido ao projeto.
    WS_stall_speed_study()
        # Definir valores de Sustentacao, velocidade de estol e altitude avaliada
    CLmax = float(input('Defina um valor de CLmax: '))
        # Lembrando que aeronaves sem flapes variam CLmax de 1.2 a 1.6 e, com flapes 
        # na parte proxima a raiz, variam em 1.6 a 2.0
    V_stall_fts = float(input('Defina um valor para a velocidade de estol em kt: ')) * 1.68781
    h_ft = float(input('Defina a altitude em metros que mais restrinja a definição de W/S: ')) / 0.3048
    
    WS_stall = WS_stall_speed(V_stall=V_stall_fts, CLmax=CLmax, h=h_ft)
    WS_list.append(WS_stall)
    S_list.append(W2/WS_stall)
    
    # Passo 3: Determinar WS com base na distância de decolagem requerida
    SG_ft = SG_m/0.3048
    WS_TOD = WS_TO_distance(CLmax=CLmax, SG=SG_ft, h=h_ft, PW=PW)
    WS_list.append(WS_TOD)
    S_list.append(W0/WS_TOD)
    
    # Passo 4: De forma alternativa ou complementar, podemos catapultar a aeronave
        # Considerando Vwod=0, ou seja, não há vento.
        # Considerando a variacao de velocidade proporcionada pelo motor nula, ou seja, 
        # a aeronave so ira ligar o motor apos ser catapultada.
        # Essas condições são determinadas por conta da Fig 5.5 do Raymer, verificamos
        # que a nossa aeronave poderá ser lançada para qualquer tipo de catapulta.
    WS_catapult = WS_catapult_to(h=h_ft, CLmax=CLmax, Vend=1.1*V_stall_fts, 
                                 Vwod=0.0, Vthurst=0.0)
    WS_list.append(WS_catapult)
    S_list.append(W0/WS_catapult)
    
    # Passo 5: Calcular WS conforme distancia de pouso.
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 6: Calcular WS conforme pouso em porta-avioes.
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 7: Calcular carga alar para cruzeiro
    WS_cr = WS_cruise(AR=AR, h=h_cruise, V=V_cruise, e=0.8)
    WS_list.append(WS_cr)
    S_list.append(W2/WS_cr)
    
    # Passo 8: Calcular carga alar para Loiter Endurance
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 9: Calcular carga para curva instantânea
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 10: Calcular carga alar para curva sustentada
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 11: Calcular caraga alar para subida e planeio
        # Verificar valores
    WS_climb = WS_climb_glide(TW_climb=TW_cl, G=ROC, CD0=0.02, AR=AR, e=0.75, h_ft=0, V=100)
    WS_list.append(WS_climb)
    S_list.append(W1/WS_climb)
    
    ###############################################################################################
    
    print('##### CARGA ALAR #####')
    print(f'W/S estatístico:       {WS_list[0]:.5f} [lb/ft2]')
    print(f'W/S estol:             {WS_list[1]:.5f} [lb/ft2]')
    print(f'W/S TOD:               {WS_list[2]:.5f} [lb/ft2]')
    print(f'W/S catapulta:         {WS_list[3]:.5f} [lb/ft2]')
    print(f'W/S cruzeiro:          {WS_list[4]:.5f} [lb/ft2]')
    print(f'W/S subida:            {WS_list[5]:.5f} [lb/ft2]')
    print()
    
    print('##### AREAS CALCULADAS #####')
    print(f'S estatístico:       {S_list[0]:.2f} [hp]')
    print(f'S estol:             {S_list[1]:.2f} [hp]')
    print(f'S TOD:               {S_list[2]:.2f} [hp]')
    print(f'S catapulta:         {S_list[3]:.2f} [hp]')
    print(f'S cruzeiro:          {S_list[4]:.2f} [hp]')
    print(f'S subida:            {S_list[4]:.2f} [hp]')
    
    
    
    return max(S_list)



 
