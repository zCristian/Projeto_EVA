import numpy as np
import PotenciaPeso
import CargaAlar

# Pesos
W0 = 523 # [lb]
W1 = 507 # [lb]
W2 = 500 # [lb]

# Geometria
AR = 10 #[-]

# Velocidades
V_cruise = 250 # [km/h]
Vmax = 260 # [km/h]. Se = None, aparecera grafico de estudo para definicao

# Aerodinamica
LD_cr = 18.6 #[-]

# Desempenho
S_G = 60 # [m] - Distancia de decolagem
ROC = 10 # [ft/min] - Rate of Climb
h_cr = 2000 # [m] - teto de serviço

############################################################################

Power, PW, TW_cl = PotenciaPeso.powerEstimate(W0=W0, W1 = W1, W2=W2, V_cruise_fts=V_cruise/1.097,
                           LD_cruise= LD_cr, V_max=Vmax/1.097) # [hp]

Area = CargaAlar.WS_estimate(W0=W0, W1=W1, W2=W2, SG_m=S_G, PW=PW,
                             AR=AR, h_cruise=h_cr, V_cruise=V_cruise,
                             ROC=ROC, TW_cl=TW_cl)

print()
print(f'Potência selecionada de {Power:.2f} HP')
print()
print(f'Area selecionada de {Area:.2f} ft2 = {Area*0.3048**2:.2f} m2.')
print(f'Razao de Aspecto: f{AR}')
print(f'Envergadura: {np.sqrt(AR*Area):.2f} = `{np.sqrt(AR*Area) * 0.3048:.2f} m')