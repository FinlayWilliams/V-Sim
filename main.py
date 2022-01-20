#<-------------------------------------------------- All Imports ------------------------------------------------------>
import model
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
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
frame_1_top.place(relheight=0.75, relwidth=1)

## Frame 1 Bottom Half
frame_1_bot = tk.Frame(frame_1, bg="green")
frame_1_bot.place(y=648, relheight=0.27, relwidth=1)

# Creating labels and entry boxes for all initial variables
lbl_N = tk.Label(frame_1_bot, text="Initial Node Population Size (N):"); N_Options = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"]; cmb_N = ttk.Combobox(frame_1_bot, values=N_Options, state="readonly")
lbl_S = tk.Label(frame_1_bot, text="Initial S Size (% of N):"); scl_S = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_IR = tk.Label(frame_1_bot, text="Initial IR Size (% of N):"); scl_IR = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_IL = tk.Label(frame_1_bot, text="Initial IL Size (% of N):"); scl_IL = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_IP = tk.Label(frame_1_bot, text="Initial IP Size (% of N):"); scl_IP = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_WSN = tk.Label(frame_1_bot, text="Wireless Sensor Network Count:"); WSN_Options = ["1", "5", "10", "20", "50"]; cmb_WSN = ttk.Combobox(frame_1_bot, values=WSN_Options, state="readonly")
lbl_DEP = tk.Label(frame_1_bot, text="Node Deployment Area: (m x m)"); DEP_Options = ["25", "50", "100", "150"]; cmb_DEP = ttk.Combobox(frame_1_bot, values=DEP_Options, state="readonly")
lbl_TRNS = tk.Label(frame_1_bot, text="Node Transmission Range (m):"); TRNS_Options = ["1", "5", "10", "15"]; cmb_TRNS = ttk.Combobox(frame_1_bot, values=TRNS_Options, state="readonly")
lbl_CNTCT = tk.Label(frame_1_bot, text="S Node Contact Rate:"); entry_CNTCT = tk.Entry(frame_1_bot)
lbl_SCAN = tk.Label(frame_1_bot, text="Botnet Scanning Rate (/sec):"); entry_SCAN = tk.Entry(frame_1_bot)
lbl_Ptrns = tk.Label(frame_1_bot, text="PTransmission Rate:"); scl_Ptrns = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_IrPsu = tk.Label(frame_1_bot, text="IR PSuccess Rate:"); scl_IrPsu = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_IlPsu = tk.Label(frame_1_bot, text="IL PSuccess Rate:"); scl_IlPsu = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_IpPsu = tk.Label(frame_1_bot, text="IP PSuccess Rate:"); scl_IpPsu = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal")
lbl_MSG = tk.Label(frame_1_bot, text="Mean Message Size (Bytes):"); entry_MSG = tk.Entry(frame_1_bot)
lbl_PWR = tk.Label(frame_1_bot, text="Mean Power to Send Message (mA):"); entry_PWR = tk.Entry(frame_1_bot)
lbl_BTRY = tk.Label(frame_1_bot, text="Total Node Battery Capacity (mAs):"); entry_BTRY = tk.Entry(frame_1_bot)
lbl_RR = tk.Label(frame_1_bot, text="Recovery rate:"); scl_RR = tk.Scale(frame_1_bot, from_=0, to=1, digits=3, resolution=0.250, orient="horizontal")
lbl_T = tk.Label(frame_1_bot, text="Days to Observe:"); scl_T = tk.Scale(frame_1_bot, from_=0, to=900, resolution=1, orient="horizontal")
btn_RUN = tk.Button(frame_1_bot, text="Run Model HERE 4 NOW")
btn_INSP = tk.Button(frame_1_bot, text="Inspect Model")
btn_SAVE = tk.Button(frame_1_bot, text="Save Configuration")
btn_NEW = tk.Button(frame_1_bot, text="New Simulation")
btn_CMPR = tk.Button(frame_1_bot, text="Compare Configurations")

# Placing them
# 1st Block
lbl_N.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e"); cmb_N.grid(row=0, column=1, padx=5, pady=(10, 0))
lbl_S.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="e"); scl_S.grid(row=1, column=1, padx=5)
lbl_IR.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e"); scl_IR.grid(row=2, column=1, padx=5)
lbl_IL.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="e"); scl_IL.grid(row=3, column=1, padx=5)
lbl_IP.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="e"); scl_IP.grid(row=4, column=1, padx=5)
# 2nd Block
lbl_WSN.grid(row=0, column=2, padx=5, pady=(10, 5), sticky="e"); cmb_WSN.grid(row=0, column=3, padx=5, pady=(10, 5))
lbl_DEP.grid(row=1, column=2, padx=5, pady=5, sticky="e"); cmb_DEP.grid(row=1, column=3, padx=5, pady=5)
lbl_TRNS.grid(row=2, column=2, padx=5, pady=5, sticky="e"); cmb_TRNS.grid(row=2, column=3, padx=5, pady=5)
lbl_CNTCT.grid(row=3, column=2, padx=5, pady=5, sticky="e"); entry_CNTCT.grid(row=3, column=3, padx=5, pady=5)
lbl_SCAN.grid(row=4, column=2, padx=5, pady=5, sticky="e"); entry_SCAN.grid(row=4, column=3, padx=5, pady=5)
# 3rd Block
lbl_Ptrns.grid(row=0, column=4, padx=5, pady=(10, 5), sticky="e"); scl_Ptrns.grid(row=0, column=5, padx=5, pady=(10, 0))
lbl_IrPsu.grid(row=1, column=4, padx=5, pady=5, sticky="e"); scl_IrPsu.grid(row=1, column=5, padx=5)
lbl_IlPsu.grid(row=2, column=4, padx=5, pady=5, sticky="e"); scl_IlPsu.grid(row=2, column=5, padx=5)
lbl_IpPsu.grid(row=3, column=4, padx=5, pady=5, sticky="e"); scl_IpPsu.grid(row=3, column=5, padx=5)
# 4th Block
lbl_MSG.grid(row=0, column=6, padx=5, pady=(10, 5), sticky="e"); entry_MSG.grid(row=0, column=7, padx=5, pady=(10, 5))
lbl_PWR.grid(row=1, column=6, padx=5, pady=5, sticky="e"); entry_PWR.grid(row=1, column=7, padx=5, pady=5)
lbl_BTRY.grid(row=2, column=6, padx=5, pady=5, sticky="e"); entry_BTRY.grid(row=2, column=7, padx=5, pady=5)
lbl_RR.grid(row=3, column=6, padx=5, pady=5, sticky="e"); scl_RR.grid(row=3, column=7, padx=5)
lbl_T.grid(row=4, column=6, padx=5, pady=5, sticky="e"); scl_T.grid(row=4, column=7, padx=5)
# 5th Block
btn_RUN.grid(row=0, column=8, padx=5, pady=(10, 4))
btn_INSP.grid(row=1, column=8, padx=5, pady=4)
btn_SAVE.grid(row=2, column=8, padx=5, pady=4)
btn_NEW.grid(row=3, column=8, padx=5, pady=4)
btn_CMPR.grid(row=4, column=8, padx=5, pady=4)







# Runnit
base.mainloop()


