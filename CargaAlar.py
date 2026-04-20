import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    if type_aircraft == 'Agricultural':
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
    KT_TO_FTS = 1.68781  # 1 kt em ft/s
    M_TO_FT   = 3.28084  # 1 m em ft
    
    altitudes_m  = [0, 500, 1000]                        # [m]
    cl_values    = np.arange(1.2, 2.01, 0.2)             # CLmax de 1.2 a 2.0
    v_stall_kt   = np.linspace(0, 100, 500)              # [kt]
    v_stall_fts  = v_stall_kt * KT_TO_FTS               # [ft/s]
    
    # Cores e estilos de linha para cada curva de CLmax
    colors     = ['#378ADD', '#D4537E', '#1D9E75', '#BA7517', '#534AB7']
    linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]
    
    # ──────────────────────────────────────────────
    # Plot
    # ──────────────────────────────────────────────
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    fig.suptitle('Carga Alar  $W/S = \\frac{1}{2}\\,\\rho\\,V_{stall}^{2}\\,CL_{max}$',
                fontsize=14, y=0.98)
    
    for ax, h_m in zip(axes, altitudes_m):
        h_ft  = h_m * M_TO_FT
        rho   = atmos.rho_altitude(h_ft)[0]   # [slug/ft3]
    
        for cl, color, ls in zip(cl_values, colors, linestyles):
            ws = 0.5 * rho * v_stall_fts**2 * cl   # [lb/ft2]
            ax.plot(v_stall_kt, ws,
                    color=color, linestyle=ls, linewidth=1.8,
                    label=f'$CL_{{max}}$ = {cl:.1f}')
    
        # Título com altitude em m e ft
        ax.set_title(f'h = {h_m} m  {{{h_ft:.0f} ft}}', fontsize=12)
    
        # Eixos com unidades entre colchetes
        ax.set_xlabel('$V_{stall}$ [kt]', fontsize=11)
        ax.set_xlim(0, 100)
        ax.set_ylim(bottom=0)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    
    axes[0].set_ylabel('$W/S$ [lb/ft²]', fontsize=11)
    
    # Legenda única à direita do último gráfico
    handles, labels = axes[-1].get_legend_handles_labels()
    axes[-1].legend(handles, labels,
                    title='$CL_{max}$',
                    title_fontsize=10,
                    fontsize=9,
                    loc='upper left',
                    framealpha=0.8)
    
    plt.tight_layout()
    # plt.savefig('carga_alar.png', dpi=150, bbox_inches='tight')
    plt.show()
    return None
 
def WS_TO_distance(CLmax: float,
                   SG: float,
                   h: float,
                   PW: float)-> float:
    """
    Calcula carga alar necessária conforme distância de decolagem.
    Args:
        CLmax (float): coef de sustentacao max [-]
        SG    (float): distancia de decolagem  [ft]
        h     (float): altitude na decolagem   [ft]
        PW    (float): razao potencia-peso na decolagem [hp/lb]
    Return:
        WS    (float): Carga alar [lb/ft2]
    """
    sigma = atmos.rho_altitude(h_ft=h)[1]
    CL_to = CLmax/1.21 # V1 = 1.1*V_stall
    # Para propeller, temos o parâmetro Takeoff Parameter
    # Dados tirados dos slides do Cuenca
    a, b, c = 12.87, 0.1395, -4.55E-6
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
              WtoWcr: float,
              e: float = 0.8)->float:
    """
    Calcula carga alar para aeronave em cruzeiro com máximo alcance.
    Args:
        AR    (float): Razao de aspecto [-]
        h     (float): altitude de cruzeiro [ft]
        V     (float): velocidade de cruzeiro [ft/sec]
        WtoWcr(float): razao carga takeoff-carga cruzeiro [-]
        e     (float): Fator de eficiencia de Oswald [-]
    Return:
        WS    (float): Carga alar [lb/ft2]
    """
    CD0 = 0.02 # aproximacao para aeronave propeller limpa
    rho = atmos.rho_altitude(h_ft= h)[0]
    q = 0.5 * rho * V**2
    WS = q * np.sqrt(np.pi * AR * e * CD0)
    
    return WS*WtoWcr

def WS_climb_glide(TW_climb: float,
                   G: float,
                   CD0: float,
                   AR: float,
                   e: float,
                   h_ft: float,
                   V: float,
                   WtoWcl: float)-> float:
    """
    Calcula carga alar para subida e planeio.
    Note que CD0 e 'e' devem incluir efeitos de flapes e trem de pouso.
    Args:
        TW_climb (float): razao tracao-peso para subida [lb/lb]
        G        (float): gradiente de subida [-]
        CD0      (float): arrasto com AoA=0 [-]
        AR       (float): razao de aspecto [-]
        e        (float): fator de eficiencia de Oswald [-]
        h_ft     (float): altitude da operacao [ft]
        V        (float): modulo da velocidade de subida [ft/sec]
        WtoWcl   (float): razao carga takeoff-carga subida [-]
    Return:
        WS       (float): Carga alar [lb/ft2]
    """
        
    assert TW_climb >= G * 2* np.sqrt(CD0 / (np.pi*AR*e)), "Motor nao é suficiente para essa taxa de subida"
    
    rho = atmos.rho_altitude(h_ft=h_ft)[0]
    q = 0.5*rho*V**2
    
    WS = (TW_climb - G + np.sqrt((TW_climb-G)**2 - 4*CD0/(np.pi*AR*e) ) ) / (2 / (q*np.pi*AR*e))
    if WS<0:
        WS = (TW_climb + G + np.sqrt((TW_climb-G)**2 - 4*CD0/(np.pi*AR*e) ) ) / (2 / (q*np.pi*AR*e))
        
    return WS * WtoWcl

def WS_estimate(W0:float,
                W1: float,
                W2: float,
                CLmax: float,
                V_stall_fts: float,
                V_inf:float,
                h_ft_dec: float,
                SG_m: float,
                PW: float,
                AR: float,
                h_cruise: float,
                V_cruise: float,
                G: float, 
                TW_cl: float)-> float:
    
    WS_list =[]
    
    # Passo 1: Determinar valores estatísticos para o tipo de aeronave
    WS_statistical = wingLoading_statistical(type_aircraft='Agricultural')
    WS_list.append(WS_statistical)
    
    # Passo 2: Determinar WS confrome velocidade de estol
        # Como não temos velocidade de estol e CLmax definidos, iremos fazer um estudo
        # e, após isso, determinar valores que fazem mais sentido ao projeto.
    # WS_stall_speed_study()
        # Definir valores de Sustentacao, velocidade de estol e altitude avaliada
    # CLmax = float(input('Defina um valor de CLmax: '))
        # Lembrando que aeronaves sem flapes variam CLmax de 1.2 a 1.6 e, com flapes 
        # na parte proxima a raiz, variam em 1.6 a 2.0
    # V_stall_fts = float(input('Defina um valor para a velocidade de estol em kt: ')) * 1.68781
    # h_ft_dec = float(input('Defina a altitude em metros que mais restrinja a definição de W/S: ')) / 0.3048
    
    WS_stall = WS_stall_speed(V_stall=V_stall_fts, CLmax=CLmax, h=h_ft_dec)
    WS_list.append(WS_stall)
    
    # Passo 3: Determinar WS com base na distância de decolagem requerida
    SG_ft = SG_m/0.3048
    WS_TOD = WS_TO_distance(CLmax=CLmax, SG=SG_ft, h=h_ft_dec, PW=PW)
    WS_list.append(WS_TOD)
    
    # Passo 4: De forma alternativa ou complementar, podemos catapultar a aeronave
        # Considerando Vwod=0, ou seja, não há vento.
        # Considerando a variacao de velocidade proporcionada pelo motor nula, ou seja, 
        # a aeronave so ira ligar o motor apos ser catapultada.
        # Essas condições são determinadas por conta da Fig 5.5 do Raymer, verificamos
        # que a nossa aeronave poderá ser lançada para qualquer tipo de catapulta.
    WS_catapult = WS_catapult_to(h=h_ft_dec, CLmax=CLmax, Vend=1.1*V_stall_fts, 
                                 Vwod=0.0, Vthurst=0.0)
    WS_list.append(WS_catapult)
    
    # Passo 5: Calcular WS conforme distancia de pouso.
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 6: Calcular WS conforme pouso em porta-avioes.
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 7: Calcular carga alar para cruzeiro
    WS_cr = WS_cruise(AR=AR, h=h_cruise, V=V_cruise, WtoWcr=W0/W2,e=0.8)
    WS_list.append(WS_cr)
    
    # Passo 8: Calcular carga alar para Loiter Endurance
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 9: Calcular carga para curva instantânea
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 10: Calcular carga alar para curva sustentada
        # Como nossa aeronave é kamikaze, é um limite que não restringe nosso projeto.
    
    # Passo 11: Calcular caraga alar para subida e planeio
        # Verificar valores
    WS_climb = WS_climb_glide(TW_climb=TW_cl, G=G, CD0=0.020, AR=AR, e=0.75, h_ft=0, 
                              V=V_inf, WtoWcl=W0/W1)
    
    WS_list.append(WS_climb)
    
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
    print(f'S estatístico:       {W0/WS_list[0]:.2f} [ft2]')
    print(f'S estol:             {W0/WS_list[1]:.2f} [ft2]')
    print(f'S TOD:               {W0/WS_list[2]:.2f} [ft2]')
    print(f'S catapulta:         {W0/WS_list[3]:.2f} [ft2]')
    print(f'S cruzeiro:          {W0/WS_list[4]:.2f} [ft2]')
    print(f'S subida:            {W0/WS_list[5]:.2f} [ft2]')
    
    # retirar valores absurdos para nosso caso
    WS_filtrado = [x for x in WS_list if x >= 10]
    
    return W0/min(WS_filtrado)



 
