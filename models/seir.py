import numpy as np
from scipy.integrate import odeint
from sklearn.linear_model import LinearRegression

class SEIR:
    # Preliminary Constructor to Initialise Variables and Allow for easy class creation
    def __init__(self, name, n, prcntS, prcntI, beta, gamma, mu, alpha, timesteps):
        self.Name = name
        self.N = n
        self.percentS = prcntS
        self.percentI = prcntI
        self.Beta = beta
        self.Gamma = gamma
        self.Mu = mu
        self.Alpha = alpha
        self.Timesteps = timesteps

        self.calculateVariables()

    # Method to create all remaining variables and calculate their values based off of the input values
    def calculateVariables(self):
        self.S = self.N * self.percentS
        self.E = 0
        self.I = self.N * self.percentI
        self.R = 0

    def SEIRModel(self, y, t, B, G, N, Mu, A):
        S, E, I, R = y

        dSdt = Mu * N - Mu * S - ((B * I * S) / N)

        dEdt = ((B * I * S) / N) - ((Mu + A) * E)

        dIdt = A * E - ((G + Mu) * I)

        dRdt = G * I - Mu * R

        return dSdt, dEdt, dIdt, dRdt

    def runModel(self):
        y0 = self.S, self.E, self.I, self.R

        solution = odeint(self.SEIRModel, y0, np.linspace(0, self.Timesteps, 101), args=(self.Beta, self.Gamma, self.N, self.Mu, self.Alpha))

        self.S1, self.E1, self.I1, self.R1 = solution.T

        return self.S1, self.E1, self.I1, self.R1

    # Method to calculate the score of the models used in the inspection page
    def calculateScores(self):
        return 1

    # Method to obtain the name from each model allowing the list to access an attribute for identification
    def __str__(self):
        return self.Name