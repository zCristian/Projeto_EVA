# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:45:14 2026

@author: Vinícius Soares
"""

from parameters import *
from equations import *
from functions import *
import matplotlib.pyplot as plt

W0_initial_guess = 500  # adjust based on your problem

ldmax_list, wfw0_list, wew0_list, wcruise_list, w0_list = [], [], [], [], []
#AR_list = np.arange(4, 17, 1)
AR_list = [10]
for ar in AR_list:
    AR.value = ar

    W0_solution = fsolve(func, W0_initial_guess)
    results.w0 = W0_solution
    results.wew0 = (W0_solution ** C) * A * Kvs

    weightCalc(results)
    

    """
    ldmax_list.append(results.ldmax)
    wfw0_list.append(results.wfw0)
    wew0_list.append((W0_solution ** C) * A * Kvs)
    
    wcruise_list.append(results.wcruise)
    w0_list.append(results.w0)
    """
    
    W0_solution_updated = fsolve(func_updated, W0_initial_guess)
    results_updated.w0 = W0_solution_updated

print(results)
print("##########################")
print(results_updated)  