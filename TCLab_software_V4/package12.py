import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from matplotlib import colors as mcolors

import package_DBR
from package_DBR import myRound, SelectPath_RT, Delay_RT, FO_RT, FOPDT, SOPDT, FOPDT_cost, SOPDT_cost, Process, Bode




# Variable from graphical method 

a = (0.529-0.367)#temp dif
Kp = 0.529 #without unit
T1 = 98 #sec
T2 = 120 #sec
Tu = 45 #sec
Tg = 170 #sec

MV = []


def broida1(MV,Kp,Tg,Tu,Ts): 
    PV = FOPDT(MV,Kp,Tg,Tu,Ts)


def broida2(MV,Kp,T2,T1,Ts): 
    PV = FOPDT(MV,Kp,5.5*(T2-T1),(2.8*T1)-(1.8*T2),Ts)

def VDG(MV,a,Kp,Tu,Tg,Ts):
    pass #a faire

def Strejc(MV,Kp,T2,T1,Ts):
    PV = FOPDT(MV,Kp,5.5*(T2-T1),(2.8*T1)-(1.8*T2),Ts)