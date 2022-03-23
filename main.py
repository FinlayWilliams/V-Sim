from interfaces.base import BaseApp


theApplication = BaseApp()
theApplication.mainloop()

# from models.seir import SEIR
# import numpy as np
# from matplotlib import pyplot as plt
#
# model = SEIR("Jeff", 10000, 0.99, 0.01, 0.8, 0.01, 0.03, 0.03, 300)
#
# s1, e1, i1, r1 = model.runModel()
# t1 = np.linspace(0, model.Timesteps, 101)
#
# plt.plot(t1, s1, "#2ca02c", label="Susceptible")
# plt.plot(t1, e1, "#2ca02c", label="Susceptible")
# plt.plot(t1, i1, "#9467bd", label="Infected")
# plt.plot(t1, r1, "#1f77b4", label="Recovered")
#
# plt.show()

# from models.sis import SIS
# import numpy as np
# from matplotlib import pyplot as plt
#
# models = SIS("SIS: Default Model",
#                             10000, 0.999, 0.001, 10, 50, 10, 1, 27, 0.3, 0.00002, 0.00006, 0.00009, 50, 0.75, 864000, 0.75, 50)
#
# S1, Ir1, Il1, Ip1 = models.runModel()
# I1 = Ir1 + Il1 + Ip1
# T1 = np.linspace(0, models.Timesteps, 101)
#
# plt.plot(T1, S1, "#2ca02c", label="Susceptible")
# plt.plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
# plt.plot(T1, Il1, "#1f77b4", label="Local Scanning Infected")
# plt.plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
#
# plt.show()
