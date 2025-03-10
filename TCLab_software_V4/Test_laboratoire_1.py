# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 19:24:03 2025

@author: Baptiste
"""
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import package_DBR 
import package_DBR_Advanced
from importlib import reload 
from package_DBR import myRound


package_DBR = reload(package_DBR)
package_DBR_Advanced = reload(package_DBR_Advanced)

#init E
if len(PV) == 0:
    E.append(SP[-1] - PVInit)
else: 
    E.append(SP[-1] - PV[-1])

#int MV
if len(MVI) == 0:
    MVI.append((Kc*Ts/Ti)*E[-1])
else: 
    if methodI == 'TRAP':
        MVI.append(MVI[-1] + (0.5*Kc*Ts/Ti)*(E[-1]+E[-2]))
    else: 
        MVI.append(MVI[-1] + (Kc*Ts/Ti)*E[-1])



















