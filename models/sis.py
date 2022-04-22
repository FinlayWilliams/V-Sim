import numpy as np
from scipy.integrate import odeint


class SIS:
    # Preliminary Constructor to Initialise Variables and Allow for easy class creation
    def __init__(self, name, n, i, wsnNo, depArea, transRange, cntctRate, scanRate, Ptrans, irPsuc, ilPsuc, ipPsuc, meanMsgSize, meanPwr, ttlBattery, rcvryRate, timesteps, ids):
        self.Name = name
        self.N = n
        self.I = i
        self.WSNnumber = wsnNo
        self.deploymentArea = depArea
        self.transmissionRange = transRange
        self.contactRate = cntctRate
        self.botScanningRate = scanRate
        self.Ptransmission = Ptrans
        self.IrPsuccess = irPsuc
        self.IlPsuccess = ilPsuc
        self.IpPsuccess = ipPsuc
        self.meanMessageSize = meanMsgSize
        self.meanPower = meanPwr
        self.totalBattery = ttlBattery
        self.recoveryRate = rcvryRate
        self.Timesteps = timesteps
        self.IDS = ids

        # Starting population sizes
        self.S = self.N - self.I
        self.Ir = self.I / 3
        self.Il = self.I / 3
        self.Ip = self.I / 3

        # Starting S Local Set Range
        self.StartSLoc = self.S * (1 / self.WSNnumber)

        # Starting S Neighbour Set Range
        self.density = (self.N / self.WSNnumber) / (self.deploymentArea / self.WSNnumber)

        self.StartSNhb = self.S * (1 / (self.density * self.transmissionRange))

        self.IrContactRate = self.botScanningRate * self.IrPsuccess
        self.IlContactRate = self.botScanningRate * self.IlPsuccess
        self.IpContactRate = self.botScanningRate * self.IpPsuccess

        # Infection Rates
        self.bR = self.IrContactRate * self.Ptransmission
        self.bL = self.IlContactRate * self.Ptransmission
        self.bP = self.IpContactRate * self.Ptransmission

        # Death Rates
        self.distance = (self.deploymentArea / self.WSNnumber) / (self.N / self.WSNnumber)

        self.powerMessage = self.meanPower * self.meanMessageSize * self.distance

        self.regularPowerTime = self.powerMessage * self.contactRate
        self.randomPowerTime = self.powerMessage * self.IrContactRate
        self.localPowerTime = self.powerMessage * self.IlContactRate
        self.peerToPeerPowerTime = self.powerMessage * self.IpContactRate

        self.regularLifespan = self.totalBattery / self.regularPowerTime
        self.randomLifespan = self.totalBattery / self.randomPowerTime
        self.localLifespan = self.totalBattery / self.localPowerTime
        self.peerToPeerLifespan = self.totalBattery / self.peerToPeerPowerTime

        self.dthB = 1 / self.regularLifespan
        self.dthR = 1 / self.randomLifespan
        self.dthL = 1 / self.localLifespan
        self.dthP = 1 / self.peerToPeerLifespan

    def SISModel(self, y, t, bR, bL, bP, dthB, dthR, dthL, dthP, a):
        S, Ir, Il, Ip = y
        I = Ir + Il + Ip

        Sloc = S * (1 / self.WSNnumber)

        Snhb = S * (1 / (self.density * self.transmissionRange))

        dSdt = -bR * S * I - bL * Sloc * I - bP * Snhb * I - dthB * S + a * I

        dIrdt = bR * S * I - a * Ir - dthB * Ir - dthR * Ir

        dIldt = bL * Sloc * I - a * Il - dthB * Il - dthL * Il

        dIpdt = bP * Snhb * I - a * Ip - dthB * Ip - dthP * Ip

        return dSdt, dIrdt, dIldt, dIpdt

    def SISModelIDS(self, y, t, bR, bL, bP, dthB, dthR, dthL, dthP, a, IDS):
        S, Ir, Il, Ip = y
        I = Ir + Il + Ip

        Sloc = S * (1 / self.WSNnumber)

        Snhb = S * (1 / (self.density * self.transmissionRange))

        dSdt = -bR * S * I - bL * Sloc * I - bP * Snhb * I - dthB * S + a * I + IDS * I

        dIrdt = bR * S * I - a * Ir - IDS * Ir - dthB * Ir - dthR * Ir

        dIldt = bL * Sloc * I - a * Il - IDS * Il - dthB * Il - dthL * Il

        dIpdt = bP * Snhb * I - a * Ip - IDS * Ip - dthB * Ip - dthP * Ip

        return dSdt, dIrdt, dIldt, dIpdt

    def runSimulation(self):
        y0 = self.S, self.Ir, self.Il, self.Ip

        if self.IDS:
            solution = odeint(self.SISModelIDS, y0, np.linspace(0, self.Timesteps, 500), args=(self.bR, self.bL, self.bP, self.dthB, self.dthR, self.dthL, self.dthP, self.recoveryRate, 0.25))
        else:
            solution = odeint(self.SISModel, y0, np.linspace(0, self.Timesteps, 500), args=(self.bR, self.bL, self.bP, self.dthB, self.dthR, self.dthL, self.dthP, self.recoveryRate))

        S1, Ir1, Il1, Ip1 = solution.T

        return S1, Ir1, Il1, Ip1

    # Method to calculate the score of the models used in the inspection page
    def calculateScores(self):
        # The scores are broken down into their categories with an overall score as well as individual scores

        S1, Ir1, Il1, Ip1 = self.runSimulation()
        I1 = Ir1 + Il1 + Ip1

        ovrMiscellaneousScore, startingPopScore, rrScore, idsScore, ovrNeighbourScore, slocScore, snhbScore, ovrBotContactRateScore, ovrEffortScore, ovrPhysicalSizeScore, ovrInfectionRateScore, ovrDeathRateScoreOvr = 0

        return 1

    # Method to obtain the name from each models allowing the list to access an attribute for identification
    def __str__(self):
        return self.Name