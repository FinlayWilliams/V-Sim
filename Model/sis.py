import numpy as np
from scipy.integrate import odeint

class SIS:
    # Preliminary Constructor to Initialise Variables and Allow for easy class creation
    def __init__(self, name, n, prcntS, prcntIr, prcntIl, prcntIp, wsnNo, depArea, transRange, cntctRate, scanRate, Ptrans,
                 irPsuc, ilPsuc, ipPsuc, meanMsgSize, meanPwr, ttlBattery, rcvryRate, timesteps):
        self.Name = name
        self.N = n
        self.percentS = prcntS
        self.percentIr = prcntIr
        self.percentIl = prcntIl
        self.percentIp = prcntIp
        self.WSNnumber = wsnNo
        self.deploymentArea = depArea
        self.transmissionRange = transRange
        self.contactRate = cntctRate
        self.botScanningRate = scanRate
        self.botPtransmission = Ptrans
        self.IrPsuccess = irPsuc
        self.IlPsuccess = ilPsuc
        self.IpPsuccess = ipPsuc
        self.meanMessageSize = meanMsgSize
        self.meanPower = meanPwr
        self.totalBattery = ttlBattery
        self.recoveryRate = rcvryRate
        self.Timesteps = timesteps

        self.calculateVariables()

    def __str__(self):
        return self.Name

    # Method to create all remaining variables and calculate their values based off of the input values
    def calculateVariables(self):
        # SI Population
        self.S = self.N * self.percentS
        self.Ir = self.N * self.percentIr
        self.Il = self.N * self.percentIl
        self.Ip = self.N * self.percentIp
        self.I = self.Ir + self.Il + self.Ip

        # S Local Set Range
        self.SLoc = 1 / self.WSNnumber

        # S Neighbour Set Range
        self.density = self.N / self.deploymentArea
        self.SNhb = 1 / (self.density * self.transmissionRange)

        # Contact rates
        self.IrContactRate = self.botScanningRate * self.IrPsuccess
        self.IlContactRate = self.botScanningRate * self.IlPsuccess
        self.IpContactRate = self.botScanningRate * self.IpPsuccess

        # Infection Rates
        self.bR = self.IrContactRate * self.botPtransmission
        self.bL = self.IlContactRate * self.botPtransmission
        self.bP = self.IpContactRate * self.botPtransmission

        # Death Rates
        self.distance = self.deploymentArea / self.N
        self.powerMessage = self.meanPower * self.meanMessageSize * self.distance

        self.regularPowerTime = self.powerMessage * self.contactRate
        self.randomPowerTime = self.powerMessage * self.IrContactRate
        self.localPowerTime = self.powerMessage * self.IlContactRate
        self.peerToPeerPowerTime = self.powerMessage * self.IpContactRate

        self.regularLifespan = self.totalBattery * self.regularPowerTime
        self.randomLifespan = self.totalBattery * self.randomPowerTime
        self.localLifespan = self.totalBattery * self.localPowerTime
        self.peerToPeerLifespan = self.totalBattery * self.peerToPeerPowerTime

        self.dthB = 1 / self.regularLifespan
        self.dthR = 1 / self.randomLifespan
        self.dthL = 1 / self.localLifespan
        self.dthP = 1 / self.peerToPeerLifespan

    def SISModel(self, y, t, Sloc, Snhb, bR, bL, bP, dthB, dthR, dthL, dthP, a):
        S, Ir, Il, Ip = y
        I = Ir + Il + Ip

        #Sloc = S * Sloc
        #Snhb = S * Snhb

        dSdt = -bR * S * I - bL * Sloc * I - bP * Snhb * I - dthB * S + a * I

        dIrdt = bR * S * I - a * Ir - dthB * Ir - dthR * Ir

        dIldt = bL * Sloc * I - a * Il - dthB * Il - dthL * Il

        dIpdt = bP * Snhb * I - a * Ip - dthB * Ip - dthP * Ip

        #print(dthR)

        return dSdt, dIrdt, dIldt, dIpdt

    def runModel(self):
        y0 = self.S, self.Ir, self.Il, self.Ip

        solution = odeint(self.SISModel, y0, np.linspace(0, self.Timesteps, 101), args=(self.SLoc, self.SNhb, self.bR, self.bL, self.bP, self.dthB, self.dthR, self.dthL, self.dthP, self.recoveryRate))

        S, Ir, Il, Ip = solution.T

        return S, Ir, Il, Ip
