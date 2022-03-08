from interface.base import BaseApp


theApplication = BaseApp()
theApplication.mainloop()

# from model.sis import SIS
# import numpy as np
# from matplotlib import pyplot as plt
#
# model = SIS("SIS: Default Model",
#                             10000, 0.999, 0.001, 10, 50, 10, 1, 27, 0.3, 0.00002, 0.00006, 0.00009, 50, 0.75, 864000, 0.75, 50)
#
# S1, Ir1, Il1, Ip1 = model.runModel()
# I1 = Ir1 + Il1 + Ip1
# T1 = np.linspace(0, model.Timesteps, 101)
#
# plt.plot(T1, S1, "#2ca02c", label="Susceptible")
# plt.plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
# plt.plot(T1, Il1, "#1f77b4", label="Local Scanning Infected")
# plt.plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
#
# plt.show()
