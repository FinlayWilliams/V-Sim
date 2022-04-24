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
        self.SLocFraction = 1 / (self.N / (self.N / self.WSNnumber))

        # Starting S Neighbour Set Range
        self.density = (self.N / self.WSNnumber) / ((self.deploymentArea * self.deploymentArea) / self.WSNnumber)

        self.SNhbFraction = 1 / (self.N / (self.density * self.transmissionRange))

        self.IrContactRate = self.botScanningRate * self.IrPsuccess
        self.IlContactRate = self.botScanningRate * self.IlPsuccess
        self.IpContactRate = self.botScanningRate * self.IpPsuccess

        # Infection Rates
        self.bR = self.IrContactRate * self.Ptransmission
        self.bL = self.IlContactRate * self.Ptransmission
        self.bP = self.IpContactRate * self.Ptransmission

        # Death Rates
        self.distance = ((self.deploymentArea * self.deploymentArea) / self.WSNnumber) / (self.N / self.WSNnumber)

        self.powerMessage = self.meanPower * self.meanMessageSize * self.distance

        self.regularPowerTime = self.powerMessage * self.contactRate
        self.randomPowerTime = self.powerMessage * self.IrContactRate
        self.localPowerTime = self.powerMessage * self.IlContactRate
        self.peerToPeerPowerTime = self.powerMessage * self.IpContactRate

        self.benignLifespan = self.totalBattery / self.regularPowerTime
        self.randomLifespan = self.totalBattery / self.randomPowerTime
        self.localLifespan = self.totalBattery / self.localPowerTime
        self.peerToPeerLifespan = self.totalBattery / self.peerToPeerPowerTime

        self.dthB = 1 / self.benignLifespan
        self.dthR = 1 / self.randomLifespan
        self.dthL = 1 / self.localLifespan
        self.dthP = 1 / self.peerToPeerLifespan

    def SISModel(self, y, t, SlocFr, SNhbFr, bR, bL, bP, dthB, dthR, dthL, dthP, a):
        S, Ir, Il, Ip = y
        I = Ir + Il + Ip

        Sloc = S * SlocFr

        Snhb = S * SNhbFr

        dSdt = -bR * S * I - bL * Sloc * I - bP * Snhb * I - dthB * S + a * I

        dIrdt = bR * S * I - a * Ir - dthB * Ir - dthR * Ir

        dIldt = bL * Sloc * I - a * Il - dthB * Il - dthL * Il

        dIpdt = bP * Snhb * I - a * Ip - dthB * Ip - dthP * Ip

        return dSdt, dIrdt, dIldt, dIpdt

    def SISModelIDS(self, y, t, SlocFr, SNhbFr, bR, bL, bP, dthB, dthR, dthL, dthP, a, IDS):
        S, Ir, Il, Ip = y
        I = Ir + Il + Ip

        Sloc = S * SlocFr

        Snhb = S * SNhbFr

        dSdt = -bR * S * I - bL * Sloc * I - bP * Snhb * I - dthB * S + a * I + IDS * I

        dIrdt = bR * S * I - a * Ir - IDS * Ir - dthB * Ir - dthR * Ir

        dIldt = bL * Sloc * I - a * Il - IDS * Il - dthB * Il - dthL * Il

        dIpdt = bP * Snhb * I - a * Ip - IDS * Ip - dthB * Ip - dthP * Ip

        return dSdt, dIrdt, dIldt, dIpdt

    def runSimulation(self):
        y0 = self.S, self.Ir, self.Il, self.Ip

        if self.IDS:
            solution = odeint(self.SISModelIDS, y0, np.linspace(0, self.Timesteps, 500), args=(self.SLocFraction, self.SNhbFraction, self.bR, self.bL, self.bP, self.dthB, self.dthR, self.dthL, self.dthP, self.recoveryRate, 0.25))
        else:
            solution = odeint(self.SISModel, y0, np.linspace(0, self.Timesteps, 500), args=(self.SLocFraction, self.SNhbFraction, self.bR, self.bL, self.bP, self.dthB, self.dthR, self.dthL, self.dthP, self.recoveryRate))

        S1, Ir1, Il1, Ip1 = solution.T

        return S1, Ir1, Il1, Ip1

    # Method to calculate the score of the models used in the inspection page
    def calculateScores(self):
        # The scores are broken down into their categories with an overall score as well as individual scores

        S1, Ir1, Il1, Ip1 = self.runSimulation()

        ovrSingleFactorScore = 0
        startingPopScore = 0
        rrScore = 0
        idsScore = 0

        ovrNeighbourScore = 0
        slocScore = 0
        snhbScore = 0

        ovrInfectionScore = 0
        scanningScore = 0
        irPScore = 0
        ilPScore = 0
        ipPScore = 0
        PTrScore = 0

        ovrEffortScore = 0
        tranRangeScore = 0
        msgSizeScore = 0
        msgPowerScore = 0
        bttryScore = 0
        depAreaScore = 0

        ovrDeathRateScore = 0
        benignLifespanScore = 0
        IrLifespanScore = 0
        IlLifespanScore = 0
        IpLifespanScore = 0

        # Make not that given enough time, all will reduce to 0 due to the nature of... death.... so this is based off of the chosen 12 hour span to observe

        if self.I == 0:
            startingPopScore = 5 # Well done no botnet!
        elif self.I == 1:
            startingPopScore = 4
        elif self.I == 3:
            startingPopScore = 3
        elif self.I == 10:
            startingPopScore = 2
        elif self.I == 100:
            startingPopScore = 1
        else:
            startingPopScore = 0

        if self.recoveryRate == 0.25:
            rrScore = 1
        elif self.recoveryRate == 0.5:
            rrScore = 2
        else:
            rrScore = 3

        if self.IDS == False:
            idsScore = 0
        else:
            idsScore = 2

        ovrSingleFactorScore = startingPopScore + rrScore + idsScore

        # as you make more wsn the sloc attack cap minimizes greatly, 1 single wsn allows mad spread of Il (1 is at the bottom)
        if self.SLocFraction == 0.02:
            slocScore = 5
        elif self.SLocFraction == 0.05:
            slocScore = 4
        elif self.SLocFraction == 0.1:
            slocScore = 3
        elif self.SLocFraction == 0.2:
            slocScore = 2
        else:
            slocScore = 1

        # LARGE deployment and TINY transmission range means the SMALLEST snhb size which neutralises Ip (good), tiny deployment and huge trans range allows mad spread of Ip (bad)
        if self.SNhbFraction == 0.000044444444444444447:
            snhbScore = 4
        elif 0.000044444444444444448 <= self.SNhbFraction <= 0.0005:
            snhbScore = 3
        elif 0.0005 <= self.SNhbFraction <= 0.004:
            snhbScore = 2
        else: # (0.024)
            snhbScore = 1

        ovrNeighbourScore = slocScore + snhbScore

        if 1 <= self.botScanningRate >= 10:
            scanningScore = 5
        elif 11 <= self.botScanningRate >= 21:
            scanningScore = 4
        elif 21 <= self.botScanningRate >= 40:
            scanningScore = 3
        elif 41 <= self.botScanningRate >= 100:
            scanningScore = 2
        else: # (100-250)
            scanningScore = 1

        if self.IrPsuccess == 0.00000000001:
            irPScore = 5
        elif self.IrPsuccess == 0.005:
            irPScore = 4
        elif self.IrPsuccess == 0.02:
            irPScore = 3
        elif self.IrPsuccess == 0.05:
            irPScore = 2
        else:
            irPScore = 1

        if self.IlPsuccess == 0.00000000001:
            ilPScore = 5
        elif self.IlPsuccess == 0.05:
            ilPScore = 4
        elif self.IlPsuccess == 0.1:
            ilPScore = 3
        elif self.IlPsuccess == 0.25:
            ilPScore = 2
        else:
            ilPScore = 1

        if self.IpPsuccess == 0.00000000001:
            ipPScore = 5
        elif self.IpPsuccess == 0.45:
            ipPScore = 4
        elif self.IpPsuccess == 0.8:
            ipPScore = 3
        elif self.IpPsuccess == 0.95:
            ipPScore = 2
        else:
            ipPScore = 1

        if self.Ptransmission == 0.00000000001:
            PTrScore = 5
        elif self.Ptransmission == 0.001:
            PTrScore = 4
        elif self.Ptransmission == 0.01:
            PTrScore = 3
        elif self.Ptransmission == 0.03:
            PTrScore = 2
        else:
            PTrScore = 1

        ovrInfectionScore = scanningScore + irPScore + ilPScore + ipPScore + PTrScore

        if self.transmissionRange == 1:
            tranRangeScore = 4
        elif self.transmissionRange == 5:
            tranRangeScore = 3
        elif self.transmissionRange == 10:
            tranRangeScore = 2
        else:
            tranRangeScore = 1

        if self.meanMessageSize == 16:
            msgSizeScore = 3
        elif self.meanMessageSize == 50:
            msgSizeScore = 2
        else:
            msgSizeScore = 1

        if self.meanPower == 0.25:
            msgPowerScore = 3
        elif self.meanPower == 0.75:
            msgPowerScore = 2
        else:
            msgPowerScore = 1

        if self.totalBattery == 3456000:
            bttryScore = 3
        elif self.totalBattery == 864000:
            bttryScore = 2
        else:
            bttryScore = 1

        if self.deploymentArea == 150:
            depAreaScore = 3
        elif self.deploymentArea == 100:
            depAreaScore = 2
        elif self.deploymentArea == 50:
            depAreaScore = 2
        else:
            depAreaScore = 1

        ovrEffortScore = tranRangeScore + msgSizeScore + msgPowerScore + bttryScore + depAreaScore

        if 3456000.0 <= self.benignLifespan <= 13824000.0: # (lergest) you dont want a lot of deaths but typically, the longer the lifespan means less malicious activity ... and you dont really want node death and huge nalicious activity
            benignLifespanScore = 5
        elif 115200.0 <= self.benignLifespan < 3456000.0:
            benignLifespanScore = 4
        elif 1843.2 <= self.benignLifespan < 115200.0:
            benignLifespanScore = 3
        elif 184.32 <= self.benignLifespan < 1843.2:
            benignLifespanScore = 2
        elif 18.432 <= self.benignLifespan < 184.32:
            benignLifespanScore = 1
        else: # 0.1024 (Shortest)
            benignLifespanScore = 0

        if 73728000.0 <= self.randomLifespan <= 1.3824e+18: #This means the bots literally do nothing and do not spread infection ... like they dont exist
            IrLifespanScore = 5
        elif 7372800.0 <= self.randomLifespan < 73728000.0:
            IrLifespanScore = 4
        elif 273066.6666666667 <= self.randomLifespan < 7372800.0:
            IrLifespanScore = 3
        elif 16384.0 <= self.randomLifespan < 273066.6666666667:
            IrLifespanScore = 2
        elif 85.33333333333333 <= self.randomLifespan < 16384.0:
            IrLifespanScore = 2
        else:
            IrLifespanScore = 1

        if 5120000000000000.0 <= self.localLifespan <= 1.3824e+18:
            IlLifespanScore = 5
        elif 27306.666666666664 <= self.localLifespan < 5120000000000000.0:
            IlLifespanScore = 4
        elif 3413.333333333333 <= self.localLifespan < 27306.666666666664:
            IlLifespanScore = 3
        elif 170.66666666666666 <= self.localLifespan < 3413.333333333333:
            IlLifespanScore = 2
        elif 7.111111111111111 <= self.localLifespan < 170.66666666666666:
            IlLifespanScore = 1
        else:
            IlLifespanScore = 0

        if 1920000.0 <= self.peerToPeerLifespan <= 1.3824e+18:
            IpLifespanScore = 5
        elif 10666.666666666666 <= self.peerToPeerLifespan < 1920000.0:
            IpLifespanScore = 4
        elif 426.66666666666663 <= self.peerToPeerLifespan < 10666.666666666666:
            IpLifespanScore = 3
        elif 21.333333333333332 <= self.peerToPeerLifespan < 426.66666666666663:
            IpLifespanScore = 2
        elif 1.3395348837209302 <= self.peerToPeerLifespan < 21.333333333333332:
            IpLifespanScore = 1
        else:
            IpLifespanScore = 0

        ovrDeathRateScore = benignLifespanScore + IrLifespanScore + IlLifespanScore + IpLifespanScore

        return ovrSingleFactorScore, startingPopScore, rrScore, idsScore, ovrNeighbourScore, slocScore, \
               snhbScore, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore, ovrEffortScore, \
               tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, depAreaScore, ovrDeathRateScore, \
               benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore

    # Method to obtain the name from each models allowing the list to access an attribute for identification
    def __str__(self):
        return self.Name