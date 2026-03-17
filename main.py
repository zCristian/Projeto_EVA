# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:45:14 2026

@author: Vinícius Soares
"""

from parameters import *
from equations import *

W0_initial_guess = 10  # adjust based on your problem

W0_solution = fsolve(func, W0_initial_guess)

print(W0_solution)