import numpy as np
from scipy.integrate import odeint
from sklearn.linear_model import LinearRegression

class SIS:
    # Preliminary Constructor to Initialise Variables and Allow for easy class creation
    def __init__(self, name, n, prcntS, prcntI, wsnNo, depArea, transRange, cntctRate, scanRate, Ptrans,
                 irPsuc, ilPsuc, ipPsuc, meanMsgSize, meanPwr, ttlBattery, rcvryRate, timesteps):
        self.Name = name
        self.N = n
        self.percentS = prcntS
        self.percentI = prcntI
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

    # Method to obtain the name from each model allowing the list to access an attribute for identification
    def __str__(self):
        return self.Name

    # Method to create all remaining variables and calculate their values based off of the input values
    def calculateVariables(self):
        # SI Population
        self.S = self.N * self.percentS
        self.Ir = (self.N * self.percentI) / 3
        self.Il = (self.N * self.percentI) / 3
        self.Ip = (self.N * self.percentI) / 3
        self.I = self.Ir + self.Il + self.Ip

        # S Local Set Range
        self.SLoc = self.S * (1 / self.WSNnumber)

        # S Neighbour Set Range
        self.density = self.N / (self.deploymentArea * self.deploymentArea)
        self.SNhb = self.S * (1 / (self.density * self.transmissionRange))

        # Contact rates
        self.IrContactRate = self.botScanningRate * self.IrPsuccess
        self.IlContactRate = self.botScanningRate * self.IlPsuccess
        self.IpContactRate = self.botScanningRate * self.IpPsuccess

        # Infection Rates
        self.bR = self.IrContactRate * self.botPtransmission
        self.bL = self.IlContactRate * self.botPtransmission
        self.bP = self.IpContactRate * self.botPtransmission

        # Death Rates
        self.distance = (self.deploymentArea * self.deploymentArea) / self.N
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

        dSdt = -bR * S * I - bL * Sloc * I - bP * Snhb * I - dthB * S + a * I

        dIrdt = bR * S * I - a * Ir - dthB * Ir - dthR * Ir

        dIldt = bL * Sloc * I - a * Il - dthB * Il - dthL * Il

        dIpdt = bP * Snhb * I - a * Ip - dthB * Ip - dthP * Ip

        return dSdt, dIrdt, dIldt, dIpdt

    def runModel(self):
        y0 = self.S, self.Ir, self.Il, self.Ip

        solution = odeint(self.SISModel, y0, np.linspace(0, self.Timesteps, 101), args=(self.SLoc, self.SNhb, self.bR, self.bL, self.bP, self.dthB, self.dthR, self.dthL, self.dthP, self.recoveryRate))

        self.S1, self.Ir1, self.Il1, self.Ip1 = solution.T

        return self.S1, self.Ir1, self.Il1, self.Ip1

    # Method to calculate the score of the model used in the inspection page
    def calculateScores(self):
        # The scores are broken down into their categories with an overall score as well as individual scores
        S1, Ir1, Il1, Ip1 = self.runModel()

        ovrSizeScore = 0

        # Calculating the population scores
        startPopScore = 0
        endPopScore = 0

        if self.percentS >= 0.9:
            startPopScore = startPopScore + 100
        elif 0.8 <= self.percentS < 0.9:
            startPopScore = startPopScore + 200
        elif 0.7 <= self.percentS < 0.8:
            startPopScore = startPopScore + 300
        elif self.percentS < 0.7:
            startPopScore = startPopScore + 400

        S2 = S1[len(S1) - 1]
        Ir2 = Ir1[len(Ir1) - 1]
        Il2 = Il1[len(Il1) - 1]
        Ip2 = Ip1[len(Ip1) - 1]
        I2 = Ir2 + Il2 + Ip2

        if S2 <= 0.25 * I2:
            endPopScore = 400
        elif 0.25 * I2 <= S2 < 0.5 * I2:
            endPopScore = 350
        elif 0.5 * I2 <= S2 < 0.75 * I2:
            endPopScore = 300
        elif 0.75 * I2 <= S2 < I2:
            endPopScore = 250
        elif I2 <= S2 < 2 * I2:
            endPopScore = 200
        elif 2 * I2 <= S2 < 3 * I2:
            endPopScore = 150
        elif S2 >= 3 * I2:
            endPopScore = 100

        ovrPopulationScore = startPopScore + endPopScore

        # Calculating the size score

        # Calculating the neighbour score
        slocNeighbourScore = 0
        snhbNeighbourScore = 0

        if self.SLoc == 1 / 1:
            slocNeighbourScore = 300
        if self.SLoc == 1 / 5:
            slocNeighbourScore = 250
        if self.SLoc == 1 / 10:
            slocNeighbourScore = 200
        if self.SLoc == 1 / 20:
            slocNeighbourScore = 150
        if self.SLoc == 1 / 50:
            slocNeighbourScore = 100

        if self.SNhb == self.N / 150:
            snhbNeighbourScore = 250
        if self.SNhb == self.N / 100:
            snhbNeighbourScore = 200
        if self.SNhb == self.N / 50:
            snhbNeighbourScore = 150
        if self.SNhb == self.N / 25:
            snhbNeighbourScore = 100

        ovrNeighbourScore = slocNeighbourScore + snhbNeighbourScore

        # Calculating the infection rate score
        brInfectionScore = 0
        blInfectionScore = 0
        bpInfectionScore = 0

        ovrInfectionRateScore = brInfectionScore + blInfectionScore + bpInfectionScore

        # Calculating the death rate score
        dthbDeathScore = 0
        dthrDeathScore = 0
        dthlDeathScore = 0
        dthpDeathScore = 0

        ovrDeathRateScore = dthbDeathScore + dthrDeathScore + dthlDeathScore + dthpDeathScore

        # Calculating the miscellaneous score
        rrMiscScore = 0

        if self.recoveryRate == 0.25:
            rrMiscScore = 400
        if self.recoveryRate == 0.5:
            rrMiscScore = 300
        if self.recoveryRate == 0.75:
            rrMiscScore = 200
        if self.recoveryRate == 1:
            rrMiscScore = 100

        ######## REMOVE? This method attempts to predict future S curves and state whether it was a good thing the
        #                virus was "stopped" in x amount of days because the S would have dropped further ...
        #                but it isnt very accurate :(
        # tMiscScore = 0
        # S1A = np.array(S1).reshape(-1, 1)
        # TA = np.array(np.linspace(0, self.Timesteps, 101)).reshape(-1, 1)
        # tFraction = int(self.Timesteps * 0.25)
        # tFutureList = []
        # for timestep in range(tFraction):
        #     tFutureList.append(self.Timesteps + timestep)
        # tFuture = np.array(tFutureList)
        # tFuture = np.array(tFuture).reshape(-1, 1)
        # regressor = LinearRegression()
        # regressor.fit(TA, S1A)
        # sPredicted = regressor.predict(tFuture)
        # sPredicted.flatten()
        # sPredictedList = sPredicted.tolist()
        # if np.mean(S1[-tFraction:]) > np.mean(sPredictedList):
        #     print("Good thing you stopped there because S was averaging {} and it would have been averaging {} at {} steps later".
        #           format(np.mean(S1[-tFraction:]), np.mean(sPredictedList), tFraction))

        ovrMiscScore = rrMiscScore

        return ovrPopulationScore, startPopScore, endPopScore, ovrSizeScore, ovrNeighbourScore, ovrInfectionRateScore, ovrDeathRateScore, ovrMiscScore
