from interfaces.base import BaseApp


theApplication = BaseApp()
theApplication.mainloop()




import numpy as np
import math

# print(np.mean(np.random.poisson(13, 27)))
# print(np.mean(np.random.poisson(13, 27)))
# print(np.mean(np.random.poisson(13, 27)))
# print(np.mean(np.random.poisson(13, 27)))
# print(np.mean(np.random.poisson(13, 27)))

#     ScnRte          PSucc
#print((27 * (np.random.poisson(27 * 0.2))))
# = Contact rate
# n = 27
# fact = 1
# for i in range(1,n+1):
#     fact = fact * i
#
# print((2.71828**-27)*(27**3/fact))
#






# from models.sis import SIS
# from matplotlib import pyplot as plt
#
# models = SIS("IoT-SIS: Default Configuration", 10000, 0.99, 0.01, 10, 50, 10, 250, 250, 0.3, 0.00002, 0.00006, 0.00009, 50, 0.75, 864000, 0.75, 14)
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
# T1 = np.linspace(0, models.Timesteps, 1001)
#
# plt.plot(T1, S1, "#2ca02c", label="Susceptible")
# plt.plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
# plt.plot(T1, Il1, "#1f77b4", label="Local Scanning Infected")
# plt.plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
#
# plt.show()
