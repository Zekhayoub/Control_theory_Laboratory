import numpy as np
import sys
import subprocess
import time
import tclab
import threading

import matplotlib.pyplot as plt
from package_DBR import Process, SelectPath_RT, Delay_RT, FO_RT

#----------------------------------Laboratoire 2----------------------------------------------------------------------#





def LL_RT(MV, Kp, TLead, TLag, Ts, PV, PVInit=0, method='EBD'):
  
    if (TLag != 0):
        K = Ts/TLag
        if len(PV) == 0:
            PV.append(PVInit)
        else: # MV[k+1] is MV[-1] and MV[k] is MV[-2]
            if method == 'EBD':
                PV.append((1/(1+K))*PV[-1] + (K*Kp/(1+K))*((1+TLead/Ts)*MV[-1] - (TLead/Ts)*MV[-2]))
            elif method == 'EFD':
                PV.append((1-K)*PV[-1] + K*Kp*((TLead/Ts)*MV[-1] + (1- TLead/Ts)*MV[-2]))
            # elif method == 'TRAP':
            #     PV.append((1/(2*T+Ts))*((2*T-Ts)*PV[-1] + Kp*Ts*(MV[-1] + MV[-2])))            
            else:
                PV.append((1/(1+K))*PV[-1] + (K*Kp/(1+K))*MV[-1])
    else:
        PV.append(Kp*MV[-1]) 



def IMC_Tuning(Kp,theta,T,T2=0,gamma=0.1,order=1):
    #the function doesn't need to be included in a loop

    #for a first or second order process
    Tclp = gamma*T
   
    if order == 1: 
        Kc = ((T+(theta/2))/(Tclp+(theta/2))) /Kp
        Ti = T+(theta/2)
        Td = T*theta/((2*T)+theta)
        return Kc, Ti, Td
    else:
        Kc = ((T+T2)/(Tclp+theta)) /Kp
        Ti = T+T2
        Td = (T*T2)/(T+T2)
        return Kc, Ti, Td



def PID_RT(SP, PV, Man, MVMan, MVFF, Kc, Ti, Td, alpha, Ts, MVmin, MVmax, MV, MVP, MVI, MVD, E, ManFF=False, PVinit=0, method ='EBD-EBD'):
#the function "PID_RT" need to be included in a "for or while loop".


# SP = setpoint vector
# PV = process value vector
# Man = manual controller mode vector : bool
# MVMan = Manual value for MV vector
# MVFF = feedforward vector

# Kc = controller gain
# Ti= integral time constant [s]
# Td = derivative time constant [s]
# alpha = Tfd = alpha*Td = where Tfd is derivative filter time constant [s]
# Ts = sampling period [s]

# MVMin = min value for MV for saturation and anti-windup
# MVMax = max value for MV for saturation and anti-windup

# MV = Maniplated value vector
# MVP = proportional part of MV vector
# MVI =  integral part of MV vector
# MVD = derivative part of MV vector
# E = control error vector

# ManFF = activated FF in manuel mode
# PVInit = initial value of PV

# Method : discreditisation value for PV
#     EBD-EBD: Euler Backward difference
#     EBD-TRAP: EBD for integral action and TRAP for derivative action
#     TRAP-EBD: TRAP for integral action and EBD for derivative action
#     TRAP-TRAP: Trapezoïdal method

# The function PID_RT appends new values to the vector MV, MVP, MVI, MVD.
    
    

    # E initialization
    if len(E) == 0:
        E.append(SP[-1]- PVinit)
    else:
        E.append(SP[-1]-PV[-1])

    methodI = method.split('-')[0]
    methodD = method.split('-')[1]
    Tfd = alpha*Td
        


    # MVP initialization
    if len(MVP)==0:
        MVP.append(Kc*E[-1])
    else:
        MVP.append(Kc * E[-1])


    # MVI initialization
    if len(MVI)==0: 
        MVI.append((Kc*Ts/Ti)*E[-1])
    else:
        if methodI=='TRAP':
            MVI.append(MVI[-1]+(0.5*Kc*Ts/Ti)*(E[-2]-E[-1]))
        else : 
            MVI.append(MVI[-1]+(Kc*Ts/Ti)*E[-1])

        
    # MVD initialization
    if len(MVD)==0:
        MVD.append(0)
    else:
        if methodD=='TRAP':
            MVD.append((Tfd-(Ts/2)/(Tfd+(Ts/2)))*MVD[-1]+(Kc*Td/(Tfd+(Ts/2)))*(E[-2]-E[-1]))
        else:
            MVD.append((Tfd/(Tfd+Ts))*MVD[-1]+(Kc*Td/(Tfd+Ts))*(E[-2]-E[-1]))

    #FeedForward calculation
    if ManFF:
        MVFFD = MVFF[-1]
    else:
        MVFFD = 0

    #integrator reset/wind-up management
    if Man[-1] ==True:
        if ManFF:
            MVI[-1] = MVMan[-1] - MVP[-1] - MVD[-1]
        else: 
            MVI[-1] = MVMan[-1] - MVP[-1] - MVD[-1] - MVFFD


    #MV saturation
    MVfinal = MVP[-1]+ MVI[-1]+MVD[-1]+MVFFD

    if MVfinal > MVmax:
        MVI[-1] = MVmax - MVP[-1] - MVD[-1] - MVFFD
        MVfinal = MVmax
        

    if MVfinal < MVmin:
        MVI[-1] = MVmin - MVP[-1] - MVD[-1] - MVFFD
        MVfinal = MVmin
        
    MV.append(MVfinal)

    return MV, MVP, MVI, MVD