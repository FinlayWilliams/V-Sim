import numpy as np
from scipy.integrate import odeint

class Model:
    # Preliminary Constructor to Initialise Variables and Allow for easy class creation
    def __init__(self, n, prcntS, prcntIr, prcntIl, prcntIp, wsnNo, depArea, transRange, cntctRate, irCntctRate,
                 ilCntctRate, ipCntctRate, irPTrans, ilPTrans, ipPTrans, meanMsgSize, meanPwr, ttlBattery, rcvryRate,
                 timesteps):
        self.N = n
        self.percentS = prcntS
        self.percentIr = prcntIr
        self.percentIl = prcntIl
        self.percentIp = prcntIp
        self.WSNnumber = wsnNo
        self.deploymentArea = depArea
        self.transmissionRange = transRange
        self.contactRate = cntctRate
        self.IrContactRate = irCntctRate
        self.IlContactRate = ilCntctRate
        self.IpContactRate = ipCntctRate
        self.IrPTransmission = irPTrans
        self.IlPTransmission = ilPTrans
        self.IpPTransmission = ipPTrans
        self.meanMessageSize = meanMsgSize
        self.meanPower = meanPwr
        self.totalBattery = ttlBattery
        self.recoveryRate = rcvryRate
        self.Timesteps = np.linspace(0, timesteps, 101)

        self.calculateVariables()

    # Method to create all remaining variables and calculate their values based off of the input values
    def calculateVariables(self):
        # SI Population
        self.S = self.N * self.percentS
        self.Ir = self.N * self.percentIr
        self.Il = self.N * self.percentIl
        self.Ip = self.N * self.percentIp
        self.I = self.Ir + self.Il + self.Ip

        # S Local Set Range
        #self.SLoc = self.S / self.WSNnumber
        self.SLoc = 1 / self.WSNnumber

        # S Neighbour Set Range
        self.density = self.N * self.deploymentArea
        #self.SNhb = self.S * (self.N / (self.density * self.transmissionRange))
        self.SNhb = 1 / (self.density * self.transmissionRange)

        # Infection Rates
        self.bR = self.IrContactRate * self.IrPTransmission
        self.bL = self.IlContactRate * self.IlPTransmission
        self.bP = self.IpContactRate * self.IpPTransmission

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

        dSdt = - bR * S * I - bL * Sloc * I - bP * Snhb * I - dthB * S + a * I

        dIrdt = bR * S * I - a * Ir - dthB * Ir - dthR * Ir

        dIldt = bL * Sloc * I - a * Il - dthB * Il - dthL * Il

        dIpdt = bP * Snhb * I - a * Ip - dthB * Ip - dthP * Ip

        return dSdt, dIrdt, dIldt, dIpdt

    def runModel(self):
        y0 = self.S, self.Ir, self.Il, self.Ip

        solution = odeint(self.SISModel, y0, self.Timesteps, args=(self.SLoc, self.SNhb, self.bR, self.bL, self.bP, self.dthB, self.dthR, self.dthL, self.dthP, self.recoveryRate))

        S, Ir, Il, Ip = solution.T

        return S, Ir, Il, Ip

    # All Setters that can be called when changing input values
    def setN(self, n): self.N = n

    def setPercentS(self, prcntS): self.percentS = prcntS

    def setPercentIr(self, prcntIr): self.percentIr = prcntIr

    def setPercentIl(self, prcntIl): self.percentIl = prcntIl

    def setPercentIp(self, prcntIp): self.percentIp = prcntIp

    def setWSNnumber(self, WSNno): self.WSNnumber = WSNno

    def setDeploymentArea(self, depArea): self.deploymentArea = depArea

    def setTransmissionRange(self, transRange): self.transmissionRange = transRange

    def setContactRate(self, cntctRate): self.contactRate = cntctRate

    def setIrContactRate(self, irCntctRate): self.IrContactRate = irCntctRate

    def setIlContactRate(self, ilCntctRate): self.IlContactRate = ilCntctRate

    def setIpContactRate(self, ipCntctRate): self.IpContactRate = ipCntctRate

    def setIrPTransmission(self, irPTrans): self.IrPTransmission = irPTrans

    def setIlPTransmission(self, ilPTrans): self.IlPTransmission = ilPTrans

    def setIpPTransmission(self, ipPTrans): self.IpPTransmission = ipPTrans

    def setMeanMessageSize(self, meanMsgSize): self.meanMessageSize = meanMsgSize

    def setMeanPower(self, meanPwr): self.meanPower = meanPwr

    def setTotalBattery(self, ttlBattery): self.totalBattery = ttlBattery

    def setRecoveryRate(self, rcvryRate): self.recoveryRate = rcvryRate

    def setTimesteps(self, timesteps): self.Timesteps = np.linspace(0, timesteps, 101)
