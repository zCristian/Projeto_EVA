from constraints_data import ConstraintCurves
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

def stall_speed_WS(rho,v_stall,cl_max):
    """ 
    Calcula a máxima carga alar imposta pela velocidade de stall

    curves:
            rho:        air density [slug/ft³],
            v_stall:    stall speed [ft/s],
            cl_max:     maximum lift coefficient [-]

    return:
            maximum wing loading [lbf/ft²]
    """

    return 0.5*rho*(v_stall**2)*cl_max


def rate_of_climb_TW(wing_loading,v_vertical,v_inf,q_climb,cd_min,k_ind):
    """
    Calcula a curva de taxa de subida

    params:
            wing_loading:   wing loading, W/S [lbf/ft²],
            v_vertical:     vertical speed [ft/s],
            v_inf:          airspeed, usually an estimate of the best rate-of-climb airspeed (V_Y) [ft/s],
            q_climb:        dynamic pressure at the selected altitude and speed [lbf/ft²],
            cd_min:         minimun drag coefficient [-],
            k_ind:          indeced drag factor[-]

    return:
            thrust-to-weight curve [-]
    """

    return (v_vertical/v_inf) + (q_climb*cd_min/wing_loading) + (k_ind*wing_loading/q_climb) # Gudmundsson (3-2)


def level_constant_velocity_turn_TW(wing_loading, q_turn, n, cd_min,k_ind):
    """
    Calcula a curva de curva a velocidade e nível constante

    params:
            wing_loading:   wing loading, W/S [lbf/ft²],
            q_turn:         dynamic pressure at the selected altitude and speed [lbf/ft²],
            n:              load factor (1/cos(phi)) [-],
            cd_min:         minimun drag coefficient [-],
            k_ind:          indeced drag factor[-]

    return:
            thrust-to-weight curve [-]
    """
    return q_turn*((cd_min/wing_loading) + k_ind*((n/q_turn)**2)*wing_loading) #Gudmundsson (3-7)


def cruise_speed_TW(wing_loading,q_cruise,cd_min,k_ind): 
    """ 
    Calcula a curva de velocidade de cruzeiro

    params:
            wing_loading:   wing loading, W/S [lbf/ft²],
            q_cruise:              dynamic pressure in cruise [lbf/ft²],
            cd_min:         minimun drag coefficient [-],
            k_ind:          indeced drag factor[-]

    return:
            thrust-to-weight curve [-]
    """

    return (q_cruise * cd_min) / wing_loading + (k_ind / q_cruise) * wing_loading # Gudmundsson (3-10)


def service_ceiling_TW(wing_loading,v_y,q_ceiling,cd_min,k_ind): 
    """
    Calcula a curva de teto de serviço

    params:
            wing_loading:   wing loading, W/S [lbf/ft²],
            v_y:            expected best rate of climb airspeed[ft/s],
            q_ceiling:      dynamic pressure at the selected altitude and speed [lbf/ft²],
            cd_min:         minimun drag coefficient [-],
            k_ind:          indeced drag factor[-]

    return:
            thrust-to-weight curve [-]
    """
    return (1.667/v_y) + (q_ceiling*cd_min/wing_loading) + (k_ind*wing_loading/q_ceiling) # Gudmundsson (3-11)


''' Decidir qual função utilizar para o teto de serviço
def service_ceiling_TW(wing_loading,v_vertical,rho_ceiling,cd_min,k_ind): 
    """
    Calcula a curva de teto de serviço

    params:
            wing_loading:   wing loading, W/S [lbf/ft²],
            v_vertical:     vertical speed [ft/s],
            rho_ceiling:    air density at the desired altitude [slug/ft³],
            cd_min:         minimun drag coefficient [-],
            k_ind:          indeced drag factor[-]

    return:
            thrust-to-weight curve [lb/ft²]
    """
    return (v_vertical/np.sqrt(np.sqrt(k_ind/(3*cd_min))*2*wing_loading/rho_ceiling)) + 4*np.sqrt(k_ind*cd_min/3) # Slide
'''

def calc_curves(ws,params):
        
        ws_stall = stall_speed_WS(params.rho_stall, params.v_stall, params.cl_max_stall)

        tw_climb = rate_of_climb_TW(
                ws,
                params.v_vertical_climb,
                params.v_inf_climb,
                params.q_climb,
                params.cd_min_climb,
                params.k_ind_climb
        )

        tw_cruise = cruise_speed_TW(
                ws,
                params.q_cruise,
                params.cd_min_cruise,
                params.k_ind_drag
        )

        tw_ceiling = service_ceiling_TW(
                ws,
                params.v_y_ceiling,
                params.q_ceiling,
                params.cd_min_cruise,
                params.k_ind_drag
        )

        tw_turn = level_constant_velocity_turn_TW(
                ws,
                params.q_turn,
                params.n_turn,
                params.cd_min_turn,
                params.k_ind_turn
        )

        curves = ConstraintCurves(ws=params.WS, tw_cruise=tw_cruise,tw_climb=tw_climb,tw_turn=tw_turn,tw_ceiling=tw_ceiling,ws_stall=ws_stall)
        return curves

def find_tw_required(ws,params):
        curves = calc_curves(ws,params)
        tw = np.maximum.reduce([curves.tw_climb,curves.tw_cruise,curves.tw_turn,curves.tw_ceiling])
        return tw

def find_optmumPoint(params):
        ws_stall=stall_speed_WS(params.rho_stall,params.v_stall,params.cl_max_stall)
        res = minimize(
                fun=lambda x: find_tw_required(x[0],params),
                x0=[50],
                bounds=[(5,ws_stall)]
        )

        ws_opt = res.x[0]
        tw_opt = res.fun
        return ws_opt,tw_opt

def plot_ConstraintsDiagram(params,curves):
        ws_opt,tw_opt = find_optmumPoint(params)
        plt.figure(figsize=(8, 6))

        
        plt.plot(curves.ws, curves.tw_climb, 'b', label='Rate of Climb', linewidth=2)
        plt.plot(curves.ws, curves.tw_turn, 'm', label='Level Turn', linewidth=2)
        plt.plot(curves.ws, curves.tw_ceiling, 'g', label='Service Ceiling', linewidth=2)
        plt.plot(curves.ws, curves.tw_cruise, 'c', label='Cruise', linewidth=2)
        plt.axvline(curves.ws_stall, color='k', label='Stall', linewidth=2)
        plt.plot(ws_opt,tw_opt, 'ko', color='red',label='Desing Point')

        

        plt.title('Constraints Diagram')
        plt.xlabel('W/S [lbf/ft²]')
        plt.ylabel('T/W [-]')
        plt.xlim(0, 100)
        plt.ylim(0,max(np.max(curves.tw_cruise),np.max(curves.tw_climb),np.max(curves.tw_turn),np.max(curves.tw_ceiling)) * 1.1)
        plt.grid(True)
        plt.legend()
        plt.show()