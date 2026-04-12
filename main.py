# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:45:14 2026

@author: Vinícius Soares
"""
from parameters import *
from equations import *
from ConstrainstsDiagram import *
import matplotlib.pyplot as plt

'''
W0_initial_guess = 1000  # adjust based on your problem

ldmax_list, wfw0_list, wew0_list, wcruise_list, w0_list = [], [], [], [], []
#AR_list = np.arange(4, 17, 1)
AR_list = [10]
for ar in AR_list:
    AR.value = ar

    W0_solution = fsolve(func, W0_initial_guess)
    results.w0 = W0_solution

    ldmax_list.append(results.ldmax)
    wfw0_list.append(results.wfw0)
    wew0_list.append((W0_solution ** C) * A * Kvs)
    results.wew0 = (W0_solution ** C) * A * Kvs
    wcruise_list.append(results.wcruise)
    w0_list.append(results.w0)

    print(results)

leg = ["Wf/W0", "Wcruise/W0", "We/W0"]
figSize = (10, 6)

plt.figure(figsize=figSize)
for idx, list in enumerate([wfw0_list, wcruise_list, wew0_list]):
    plt.plot(AR_list, list, "o", label = leg[idx])

plt.xlabel("AR")
plt.legend(loc = "best", fontsize = 11)
plt.savefig("fuelFracs.png")
##################################33
plt.figure(figsize=figSize)
plt.plot(AR_list, ldmax_list, "o")

plt.ylabel("L/Dmax")
plt.xlabel("AR")
plt.savefig("LDmax.png")
##################################33
plt.figure(figsize=figSize)
plt.plot(AR_list, w0_list, "o")

plt.ylabel("W0")
plt.xlabel("AR")
plt.savefig("W0.png")
'''

params = ConstraintsParameters()
curves = calc_curves(params.WS,params)
plot_ConstraintsDiagram(params,curves)



