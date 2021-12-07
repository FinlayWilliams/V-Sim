### All Imported Python Packages to be Used ###
import model
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
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


def setContactRate(contRate): return contRate


def setPtransmission(pTransmission): return pTransmission


def setInfectionRate(contRate, pTransmission):
    infRate = contRate * pTransmission
    return infRate


def setDistance(depArea, n):
    dist = depArea * n
    return dist


def setMeanMessageSize(mMsgSize): return mMsgSize


def setMeanPower(meanpower): return meanpower


def setPowerMsg(meanpower, mMsgSize, dist):
    pwrMsg = meanpower * mMsgSize * dist
    return pwrMsg


def setPowerTime(pwrMsg, contRate):
    pwrTime = pwrMsg * contRate
    return pwrTime


def setTotalBatteryCapacity(ttlBatCap): return ttlBatCap


def setNodeLifespan(ttlBatCap, pwrTime):
    nLifespan = ttlBatCap * pwrTime
    return nLifespan


def setDeathrate(nLifespan):
    return 1 / nLifespan


def setARecoveryRate(recoveryRate): return recoveryRate


def setTimesteps(t):
    timesteps = np.linspace(0, t, 101)
    return timesteps


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
WSNno = setWSN(5)
Sloc = setSloc(WSNno, S0)

## S Neighbours Value
depArea = setDepArea(10)
density = setDensity(N, depArea)
transRange = setTransRange(10)
Snhb = setSnhb(N, S0, density, transRange)

## Infection Rates
contactRate = setContactRate(4)
bRcontactRate = setContactRate(3)
bLcontactRate = setContactRate(2)
bPcontactRate = setContactRate(1)

brPtransmission = setPtransmission(5)
blPtransmission = setPtransmission(4)
bpPtransmission = setPtransmission(3)

bR = setInfectionRate(bRcontactRate, brPtransmission)
bL = setInfectionRate(bLcontactRate, blPtransmission)
bP = setInfectionRate(bPcontactRate, bpPtransmission)

## Death Rates
distance = setDistance(depArea, N)
meanMessageSize = setMeanMessageSize(50)
meanPower = setMeanPower(0.5)
powerMsg = setPowerMsg(meanPower, meanMessageSize, distance)

regPowerTime = setPowerTime(powerMsg, contactRate)
rndPowerTime = setPowerTime(powerMsg, bRcontactRate)
lclPowerTime = setPowerTime(powerMsg, bLcontactRate)
p2pPowerTime = setPowerTime(powerMsg, bPcontactRate)

totalBatteryCapacity = setTotalBatteryCapacity(864000)

regNodeLifespan = setNodeLifespan(totalBatteryCapacity, regPowerTime)
rndNodeLifespan = setNodeLifespan(totalBatteryCapacity, rndPowerTime)
lclNodeLifespan = setNodeLifespan(totalBatteryCapacity, lclPowerTime)
p2pNodeLifespan = setNodeLifespan(totalBatteryCapacity, p2pPowerTime)

dthB = setDeathrate(regNodeLifespan)
dthR = setDeathrate(rndNodeLifespan)
dthL = setDeathrate(lclNodeLifespan)
dthP = setDeathrate(p2pNodeLifespan)

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
plt.title("IoT-SIS Model")
plt.xlabel('Timesteps')
plt.ylabel('Population Size')
plt.grid()
plt.show()

myModel = model.Model(10000, 0.7, 0.1, 0.1, 0.1, 5, 10, 10, 5, 5, 5, 5, 4, 4, 4, 50, 0.5, 864000, 0.5, 10)
myModel.newVariable(10)
print(myModel.Jeff)

#<-------------------------------------------------------- GUI -------------------------------------------------------->
