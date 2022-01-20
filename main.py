#<-------------------------------------------------- All Imports ------------------------------------------------------>
import model
import gui
from scipy.integrate import odeint
import numpy as np

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


#<------------------------------------------------------- Model ------------------------------------------------------->

# #VAR:                                                        deply    tran  cntc     scan     P         irP      ilP      ipP    mean   mean
# #VAR:                  N      S     Ir      Il     Ip    W   area     rng    rte      rte    trans      suc      suc      suc    msg    pwr      ttlbat    rcvo    time
myModel = model.Model(10000, 0.99, 0.003, 0.003, 0.004, 10, 50 * 50,  10,     1,      27,     0.3,    0.00002,   0.06,    0.09,     50,   0.75,    864000,    0.75,    100)
#
# S1, Ir1, Il1, Ip1 = myModel.runModel()
# I1 = Ir1 + Il1 + Ip1
# T1 = myModel.Timesteps
#
# plt.plot(T1, S1, 'g', label='Susceptible')
# #plt.plot(T1, I1, 'r', label='All Infected')
# plt.plot(T1, Ir1, 'y', label='Random-Scanning Infected')
# plt.plot(T1, Il1, 'b', label='Local Infected')
# plt.plot(T1, Ip1, 'c', label='P2P Infected')
# plt.legend(loc='best')
# plt.title("IoT-SIS Model")
# plt.xlabel('Timesteps')
# plt.ylabel('Population Size')
# plt.grid()
# plt.show()

#<-------------------------------------------------------- GUI -------------------------------------------------------->
interface = gui.ModelInterface(myModel)
interface.displayModelView()
