### All Imported Python Packages to be Used ###
import tkinter as tk
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


#<------------------------------------------------------- Model ------------------------------------------------------->
### All Setters to Set and / or Calculate Variable Values ###
def setN(n): return n


def setPercentS(percS): return percS


def setPercentIr(percIr): return percIr


def setPercentIl(percIl): return percIl


def setPercentIp(percIp): return percIp


def setWSN(wsnno): return wsnno


def setSI(n, sStartPercent, irStartPercent, ilStartPercent, ipStartPercent):
    s = n * sStartPercent
    ir = n * irStartPercent
    il = n * ilStartPercent
    ip = n * ipStartPercent

    return s, ir, il, ip


def setSloc(wsnno, s):
    sloc = s / wsnno
    return sloc


def setDepArea(depArea): return depArea


def setDensity(n, depArea):
    density = n * depArea
    return density


def setTransRange(transRange): return transRange


def setSnhb(n, s, density, transRange):
    nhb = density * transRange
    snhb = s / (n / nhb)
    return snhb


def setARecoveryRate(recoveryRate): return recoveryRate


def setTimesteps(t):
    t = np.linspace(0, t)
    return t


### Instantiating Variables and Their Default Values ###
##  Population
N = setN(10000)
percentS = setPercentS(0.7)
percentIr = setPercentIr(0.1)
percentIl = setPercentIl(0.1)
percentIp = setPercentIp(0.1)
S0, Ir0, Il0, Ip0 = setSI(N, percentS, percentIr, percentIl, percentIp)
I0 = Ir0 + Il0 + Ip0

## S local Value
WSNno = setWSN(10)
Sloc = setSloc(WSNno, S0)

## S Neighbours Value
depArea = setDepArea(10)
density = setDensity(N, depArea)
transRange = setTransRange(10)
Snhb = setSnhb(N, S0, density, transRange)

## Infection Rates
bR = 0.2
bL = 0.15
bP = 0.20

## Death Rates
dthB = 0.05
dthR = 0.01
dthL = 0.01
dthP = 0.01

## Recovery rate
A = setARecoveryRate(0.5)

## Timesteps
T = setTimesteps(10)

### Initial Conditions
y0 = S0, Ir0, Il0, Ip0


### Function that solves the differentials
def SIModel(y, t, Sloc, Snhb, bR, bL, bP, dthB, dthR, dthL, dthP, a):
    S, Ir, Il, Ip = y
    I = Ir + Il + Ip

    # Not sure if any of these should be in brackets - or if the alpha * I should be in brackets of any description ...

    dSdt = -(bR * S * I) - (bL * Sloc * I) - (bP * Snhb * I) - (dthB * S) + (a * I)

    dIrdt = (bR * S * I) - (a * Ir) - (dthB * Ir) - (dthR * Ir)

    dIldt = (bL * Sloc * I) - (a * Il) - (dthB * Il) - (dthL * Il)

    dIpdt = (bP * Snhb * I) - (a * Ip) - (dthB * Ip) - (dthP * Ip)

    return dSdt, dIrdt, dIldt, dIpdt


### Getting the final solution through running the model
solution = odeint(SIModel, y0, T, args=(Sloc, Snhb, bR, bL, bP, dthB, dthR, dthL, dthP, A))

### Assigning final SI Values
S, Ir, Il, Ip = solution.T
I = Ir + Il + Ip

### Testing Plot
plt.plot(T, S, 'g', label='Susceptible')
plt.plot(T, I, 'r', label='All Infected')
plt.plot(T, Ir, 'y', label='Random-Scanning Infected')
plt.plot(T, Il, 'b', label='Local Infected')
plt.plot(T, Ip, 'c', label='P2P Infected')
plt.legend(loc='best')
plt.xlabel('Timesteps')
plt.grid()
plt.show()

#<-------------------------------------------------------- GUI -------------------------------------------------------->
