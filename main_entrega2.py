import numpy as np
import PotenciaPeso
import CargaAlar

################################# PARAMETROS ###########################################
# Pesos
W0 = 523 # [lb]
W1 = 507 # [lb]
W2 = 500 # [lb]

# Geometria
AR = 10 # [-]

# Velocidades
V_cruise = 250     # [km/h]
Vmax     = 280     # [km/h]. Se = None, aparecera grafico de estudo para definicao

# Aerodinamica
LD_cr = 18.6       # [-] - razao sustentacao-arrasto em cruzeiro
LD_cl = 0.9*LD_cr  # [-] - razao sustentacao-arrasto em subida
CL_max = 1.5       # [-] - coef de sustentacao maximo

# Desempenho
S_G          = 60            # [m] - Distancia de decolagem
h_dec        = 1000          # [m] - altitude máxima de decolagem

h_cr         = 2000          # [m] - teto de serviço
Pcr_Pto      = 0.75          # [-] - razao potencia em cruzeiro por decolagem
eta_P_cruise = 0.8           # [-] - eficiencia de helice em cruise

V_stall      = 96            # [ft/s] - velocidade de estol

V_inf        = 1.2*V_stall   # [ft/s] - módulo da velocidade durante subida
G            = 0.10          # [ft/min] - gradiente de climb
V_vert_climb = V_inf*G*60    # [ft/min] - velocidade vertical de subida
eta_P_climb  = 0.7           # [-] - eficiencia de helice em subida
Pcl_Pto      = 1.0           # [-] - razao potencia em subida por decolagem

Vend = 1.1*V_stall           # [ft/sec] - velocidade final apos decolagem assistida

########################################################################################

PW_selected, TW_cl = PotenciaPeso.powerEstimate(W0 = W0, W1 = W1, W2 = W2, 
                                              V_cruise_fts = V_cruise/1.097,
                                              LD_cruise= LD_cr,
                                              Pcr_Pto = Pcr_Pto,
                                              eta_cruise = eta_P_cruise,
                                              LD_climb = LD_cl,
                                              Vv_climb = V_vert_climb,
                                              V_inf_climb = V_inf,
                                              etaP_climb = eta_P_climb,
                                              Pcl_Pto = Pcl_Pto,
                                              V_max=Vmax/1.097) # [hp]

Area = CargaAlar.WS_estimate(W0=W0, W1=W1, W2=W2, 
                             CLmax = CL_max, V_stall_fts=V_stall, 
                             V_inf=V_inf, h_ft_dec=h_dec/0.3048,
                             SG_m=S_G, PW=PW_selected,
                             AR=AR, h_cruise=h_cr/0.3048, V_cruise=V_cruise,
                             G=G, TW_cl=TW_cl)

print()
print(f'Potência selecionada de {PW_selected*W0:.2f} HP')
print()
print(f'Area selecionada de {Area:.2f} ft2 [{Area*0.3048**2:.2f} m2]')
print(f'Razao de Aspecto: {AR}')
print(f'Envergadura: {np.sqrt(AR*Area):.2f} ft [{np.sqrt(AR*Area) * 0.3048:.2f} m]')