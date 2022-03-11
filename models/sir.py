import numpy as np
from scipy.integrate import odeint
from sklearn.linear_model import LinearRegression

class SIR:
    # Preliminary Constructor to Initialise Variables and Allow for easy class creation
    def __init__(self, name, n, prcntS, prcntI, beta, gamma, timesteps):
        self.Name = name
        self.N = n
        self.percentS = prcntS
        self.percentI = prcntI
        self.Beta = beta
        self.Gamma = gamma
        self.Timesteps = timesteps

        self.calculateVariables()

    # Method to create all remaining variables and calculate their values based off of the input values
    def calculateVariables(self):
        self.S = self.N * self.percentS
        self.I = self.N * self.percentI

    def SIRModel(self, y, t, B, G, N):
        S, Ir, Il, Ip = y
        I = Ir + Il + Ip

        dSdt = -B * S * I / N

        dIdt = B * S * I / N - G * I

        dRdt = G * I

        return dSdt, dIdt, dRdt

    def runModel(self):
        y0 = self.S, self.I, self.R

        solution = odeint(self.SIRModel, y0, np.linspace(0, self.Timesteps, 101), args=(self.Beta, self.Gamma, self.N))

        self.S1, self.I1, self.R1 = solution.T

        return self.S1, self.I1, self.R1

    # Method to calculate the score of the models used in the inspection page
    def calculateScores(self):
        return 1

    # Method to obtain the name from each model allowing the list to access an attribute for identification
    def __str__(self):
        return self.Name