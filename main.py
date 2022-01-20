#<-------------------------------------------------- All Imports ------------------------------------------------------>
import model
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


#<------------------------------------------------------- Model ------------------------------------------------------->

# #VAR:                                                        deply    tran  cntc     scan     P         irP      ilP      ipP     mean   mean
# #VAR:                  N      S     Ir      Il     Ip    W   area     rng    rte      rte    trans      suc      suc      suc      msg    pwr      ttlbat    rcvo    time
# myModel = model.Model(10000, 0.99, 0.003, 0.003, 0.004, 10, 50 * 50,  10,     1,      27,     0.3,    0.00002,   0.06,    0.09,   50,     0.75,    864000,    0.75,    100)
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

# Base Window Settings
base = tk.Tk()
base.title("IoT-SIS Model Simulation")

screen_width = base.winfo_screenwidth()
screen_height = base.winfo_screenheight()

center_x = int(screen_width / 2 - 1536 / 2)
center_y = int(screen_height / 2 - 864 / 2)

base.geometry(f"1536x864+{center_x}+{center_y}")
base.resizable(0, 0)
base.configure(background="#453354")
base.attributes("-transparentcolor", "grey")

base.iconbitmap('./assets/virus_icon.ico')



### Frame 1 ( first screen )
frame_1 = tk.Frame(base, bg="#453354")
frame_1.place(relheight=1, relwidth=1)

## Frame 1 Top Half
frame_1_top = tk.Frame(frame_1, bg="red")
frame_1_top.place(relheight=0.80, relwidth=1)

## Frame 1 Bottom Half
frame_1_bot = tk.Frame(frame_1, bg="green")
frame_1_bot.place(y=691, relheight=0.2, relwidth=1)

# Creating labels and entry boxes for all initial variables
lbl_N = tk.Label(frame_1_bot, text="Starting Population Size (N):"); entry_N = tk.Entry(frame_1_bot)
lbl_S = tk.Label(frame_1_bot, text="Starting S Size (% of N):"); entry_S = tk.Entry(frame_1_bot)
lbl_IR = tk.Label(frame_1_bot, text="Starting IR Size (% of N):"); entry_IR = tk.Entry(frame_1_bot)
lbl_IL = tk.Label(frame_1_bot, text="Starting IL Size (% of N):"); entry_IL = tk.Entry(frame_1_bot)
lbl_IP = tk.Label(frame_1_bot, text="Starting IP Size (% of N):"); entry_IP = tk.Entry(frame_1_bot)
lbl_WSN = tk.Label(frame_1_bot, text="Wireless Sensor Network Count:"); entry_WSN = tk.Entry(frame_1_bot)
lbl_DEP = tk.Label(frame_1_bot, text="Node Deployment Area (m^2):"); entry_DEP = tk.Entry(frame_1_bot)
lbl_TRNS = tk.Label(frame_1_bot, text="Node Transmission Range (m):"); entry_TRNS = tk.Entry(frame_1_bot)
lbl_CNTCT = tk.Label(frame_1_bot, text="Node Contact Rate:"); entry_CNTCT = tk.Entry(frame_1_bot)
lbl_SCAN = tk.Label(frame_1_bot, text="Botnet Scanning Rate (/sec):"); entry_SCAN = tk.Entry(frame_1_bot)
lbl_Ptrns = tk.Label(frame_1_bot, text="PTransmission Rate:"); entry_Ptrns = tk.Entry(frame_1_bot)
lbl_IrPsu = tk.Label(frame_1_bot, text="IR PSuccess Rate:"); entry_IrPsu = tk.Entry(frame_1_bot)
lbl_IlPsu = tk.Label(frame_1_bot, text="IL PSuccess Rate:"); entry_IlPsu = tk.Entry(frame_1_bot)
lbl_IpPsu = tk.Label(frame_1_bot, text="IP PSuccess Rate:"); entry_IpPsu = tk.Entry(frame_1_bot)
lbl_MSG = tk.Label(frame_1_bot, text="Mean Message Size (Bytes):"); entry_MSG = tk.Entry(frame_1_bot)
lbl_PWR = tk.Label(frame_1_bot, text="Mean Power to Send Message (mA):"); entry_PWR = tk.Entry(frame_1_bot)
lbl_BTRY = tk.Label(frame_1_bot, text="Total Node Battery Capacity (mAs):"); entry_BTRY = tk.Entry(frame_1_bot)
lbl_RR = tk.Label(frame_1_bot, text="Recovery rate:"); entry_RR = tk.Entry(frame_1_bot)
lbl_T = tk.Label(frame_1_bot, text="Days to Observe:"); entry_T = tk.Entry(frame_1_bot)
btn_RUN = tk.Button(frame_1_bot, text="Run Model HERE 4 NOW")
btn_INSP = tk.Button(frame_1_bot, text="Inspect Model")
btn_SAVE = tk.Button(frame_1_bot, text="Save Configuration")
btn_NEW = tk.Button(frame_1_bot, text="New Simulation")

# Placing them
# 1st Block
lbl_N.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e"); entry_N.grid(row=0, column=1, padx=5, pady=(10, 5))
lbl_S.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="e"); entry_S.grid(row=1, column=1, padx=5, pady=5)
lbl_IR.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e"); entry_IR.grid(row=2, column=1, padx=5, pady=5)
lbl_IL.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="e"); entry_IL.grid(row=3, column=1, padx=5, pady=5)
lbl_IP.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="e"); entry_IP.grid(row=4, column=1, padx=5, pady=5)
# 2nd Block
lbl_WSN.grid(row=0, column=2, padx=5, pady=(10, 5), sticky="e"); entry_WSN.grid(row=0, column=3, padx=5, pady=(10, 5))
lbl_DEP.grid(row=1, column=2, padx=5, pady=5, sticky="e"); entry_DEP.grid(row=1, column=3, padx=5, pady=5)
lbl_TRNS.grid(row=2, column=2, padx=5, pady=5, sticky="e"); entry_TRNS.grid(row=2, column=3, padx=5, pady=5)
lbl_CNTCT.grid(row=3, column=2, padx=5, pady=5, sticky="e"); entry_CNTCT.grid(row=3, column=3, padx=5, pady=5)
lbl_SCAN.grid(row=4, column=2, padx=5, pady=5, sticky="e"); entry_SCAN.grid(row=4, column=3, padx=5, pady=5)
# 3rd Block
lbl_Ptrns.grid(row=0, column=4, padx=5, pady=(10, 5), sticky="e"); entry_Ptrns.grid(row=0, column=5, padx=5, pady=(10, 5))
lbl_IrPsu.grid(row=1, column=4, padx=5, pady=5, sticky="e"); entry_IrPsu.grid(row=1, column=5, padx=5, pady=5)
lbl_IlPsu.grid(row=2, column=4, padx=5, pady=5, sticky="e"); entry_IlPsu.grid(row=2, column=5, padx=5, pady=5)
lbl_IpPsu.grid(row=3, column=4, padx=5, pady=5, sticky="e"); entry_IpPsu.grid(row=3, column=5, padx=5, pady=5)
# 4th Block
lbl_MSG.grid(row=0, column=6, padx=5, pady=(10, 5), sticky="e"); entry_MSG.grid(row=0, column=7, padx=5, pady=(10, 5))
lbl_PWR.grid(row=1, column=6, padx=5, pady=5, sticky="e"); entry_PWR.grid(row=1, column=7, padx=5, pady=5)
lbl_BTRY.grid(row=2, column=6, padx=5, pady=5, sticky="e"); entry_BTRY.grid(row=2, column=7, padx=5, pady=5)
lbl_RR.grid(row=3, column=6, padx=5, pady=5, sticky="e"); entry_RR.grid(row=3, column=7, padx=5, pady=5)
lbl_T.grid(row=4, column=6, padx=5, pady=5, sticky="e"); entry_T.grid(row=4, column=7, padx=5, pady=5)
# 5th Block
btn_RUN.grid(row=0, column=8, padx=5, pady=(10, 4))
btn_INSP.grid(row=1, column=8, padx=5, pady=4)
btn_SAVE.grid(row=2, column=8, padx=5, pady=4)
btn_NEW.grid(row=3, column=8, padx=5, pady=4)

# Runnit
base.mainloop()


