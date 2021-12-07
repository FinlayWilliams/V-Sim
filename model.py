class Model:
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
        self.Timesteps = timesteps

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

    def setTimesteps(self, timesteps): self.Timesteps = timesteps

    # Method to create all remaining variables and calculate their values based off of the input values
    def calculateVariables(self):
        ligmaballs
