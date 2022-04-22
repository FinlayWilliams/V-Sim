from interfaces.base import BaseApp


theApplication = BaseApp()
theApplication.mainloop()



# from models.sis import SIS
# from matplotlib import pyplot as plt
#
# models = SIS("IoT-SIS: Default", 1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.95, 50, 0.75, 864000, 0.5, 12, False)
#
# print("meanPower ({}) x meanMsg ({}) x distance ({}) = powerMsg ({})".format(models.meanPower, models.meanMessageSize, models.distance, models.powerMessage))
# print("")
# print("powerMsg ({}) x randomContactRate ({}) = powerMsg ({})".format(models.powerMessage, models.IrContactRate, models.randomPowerTime))
# print("")
# print("totalBattery ({}) x powerTime ({}) = randomLifespan ({})".format(models.totalBattery, models.randomPowerTime, models.randomLifespan))
# print("")
# print("1 / randomLifespan ({}) = dthR ({})".format(models.randomLifespan, models.dthR))
#
# S1, Ir1, Il1, Ip1 = models.runSimulation()
# I1 = Ir1 + Il1 + Ip1
# T1 = np.linspace(0, models.Timesteps, 500)
#
# plt.plot(T1, S1, "#2ca02c", label="Susceptible")
# plt.plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
# plt.plot(T1, Il1, "#1f77b4", label="Local Scanning Infected")
# plt.plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
#
# plt.show()
