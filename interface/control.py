import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
from model import sis


class ControlInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.activeModel = controller.getActiveModel()
        self.activeModelIndex = controller.getActiveModelIndex()

        # Frame 1 Top (Upper area for displaying graphs)
        frame_1_top = tk.Frame(self, bg="red")

        # Frame 1 Bottom (Lower area for the controls)
        frame_1_bot = tk.Frame(self, bg="green")

        # Creating labels and entry boxes for all initial variables
        lbl_N = tk.Label(frame_1_bot, text="Initial Node Population Size (N):")
        N_Options = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"]
        self.cmb_N = ttk.Combobox(frame_1_bot, values=N_Options, state="readonly")

        lbl_S = tk.Label(frame_1_bot, text="Initial S Size (% of N):")
        self.scl_S = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal",
                              command=self.updateModel)

        lbl_IR = tk.Label(frame_1_bot, text="Initial IR Size (% of N):")
        self.scl_IR = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)

        lbl_IL = tk.Label(frame_1_bot, text="Initial IL Size (% of N):")
        self.scl_IL = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)

        lbl_IP = tk.Label(frame_1_bot, text="Initial IP Size (% of N):")
        self.scl_IP = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)

        lbl_WSN = tk.Label(frame_1_bot, text="Wireless Sensor Network Count:")
        WSN_Options = ["1", "5", "10", "20", "50"]
        self.cmb_WSN = ttk.Combobox(frame_1_bot, values=WSN_Options, state="readonly")

        lbl_DEP = tk.Label(frame_1_bot, text="Node Deployment Area: (m x m)")
        DEP_Options = ["25", "50", "100", "150"]
        self.cmb_DEP = ttk.Combobox(frame_1_bot, values=DEP_Options, state="readonly")

        lbl_TRNS = tk.Label(frame_1_bot, text="Node Transmission Range (m):")
        TRNS_Options = ["1", "5", "10", "15"]
        self.cmb_TRNS = ttk.Combobox(frame_1_bot, values=TRNS_Options, state="readonly")

        lbl_CNTCT = tk.Label(frame_1_bot, text="S Node Contact Rate:")
        CNTCT_Options = ["1", "5", "10", "20", "50", "75", "100", "250"]
        self.cmb_CNTCT = ttk.Combobox(frame_1_bot, values=CNTCT_Options, state="readonly")

        lbl_SCAN = tk.Label(frame_1_bot, text="Botnet Scanning Rate (/sec):")
        self.scl_SCAN = tk.Scale(frame_1_bot, from_=0, to=250, resolution=1, orient="horizontal",
                                 command=self.updateModel)

        lbl_Ptrns = tk.Label(frame_1_bot, text="PTransmission Rate:")
        self.scl_Ptrns = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal",
                                  command=self.updateModel)

        lbl_IrPsu = tk.Label(frame_1_bot, text="IR PSuccess Rate:")
        self.scl_IrPsu = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.00001, orient="horizontal",
                                  command=self.updateModel)

        lbl_IlPsu = tk.Label(frame_1_bot, text="IL PSuccess Rate:")
        self.scl_IlPsu = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal",
                                  command=self.updateModel)

        lbl_IpPsu = tk.Label(frame_1_bot, text="IP PSuccess Rate:")
        self.scl_IpPsu = tk.Scale(frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal",
                                  command=self.updateModel)

        lbl_Name = tk.Label(frame_1_bot, text="model Name:")
        self.entry_Name = tk.Entry(frame_1_bot)

        lbl_MSG = tk.Label(frame_1_bot, text="Mean Message Size (Bytes):")
        MSG_Options = ["10", "20", "50", "100"]
        self.cmb_MSG = ttk.Combobox(frame_1_bot, values=MSG_Options, state="readonly")

        lbl_PWR = tk.Label(frame_1_bot, text="Mean Power to Send Message (mA):")
        PWR_Options = ["0.25", "0.5", "0.75", "1", "1.25"]
        self.cmb_PWR = ttk.Combobox(frame_1_bot, values=PWR_Options, state="readonly")

        lbl_BTRY = tk.Label(frame_1_bot, text="Total Node Battery Capacity (mAs):")
        BTRY_Options = ["432000", "864000", "1728000"]
        self.cmb_BTRY = ttk.Combobox(frame_1_bot, values=BTRY_Options, state="readonly")

        lbl_RR = tk.Label(frame_1_bot, text="Recovery rate:")
        self.scl_RR = tk.Scale(frame_1_bot, from_=0, to=1, digits=3, resolution=0.250, orient="horizontal",
                               command=self.updateModel)

        lbl_T = tk.Label(frame_1_bot, text="Days to Observe:")
        self.scl_T = tk.Scale(frame_1_bot, from_=0, to=900, resolution=1, orient="horizontal",
                              command=self.updateModel)

        btn_RUN = tk.Button(frame_1_bot, text="Run model HERE 4 NOW", command=lambda: self.updateGraphs(self.activeModel))
        btn_INSP = tk.Button(frame_1_bot, text="Inspect model")
        btn_SAVE = tk.Button(frame_1_bot, text="Save model", command=lambda: [self.updateModel(1), controller.overwriteModel(self.activeModelIndex, self.activeModel)])
        btn_SAVE_NEW = tk.Button(frame_1_bot, text="Save New model", command=lambda: [self.updateModel(1), controller.addModel(self.activeModel)])
        btn_RTRN = tk.Button(frame_1_bot, text="Return to Home", command=lambda: controller.display("ControlInterface", "HomeInterface"))

        # Placing all elements
        ## Frame 1 Top Half
        frame_1_top.place(relheight=0.75, relwidth=1)
        ## Frame 1 Bottom Half
        frame_1_bot.place(y=648, relheight=0.27, relwidth=1)
        # 1st Block
        lbl_N.grid(row=0, column=0, padx=(10, 5), pady=(7, 0), sticky="e")
        self.cmb_N.grid(row=0, column=1, padx=5, pady=(7, 0))
        self.cmb_N.set(self.activeModel.N)
        self.cmb_N.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_S.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="e")
        self.scl_S.grid(row=1, column=1, padx=5, sticky="ew")
        self.scl_S.set(self.activeModel.percentS)
        lbl_IR.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e")
        self.scl_IR.grid(row=2, column=1, padx=5, sticky="ew")
        self.scl_IR.set(self.activeModel.percentIr)
        lbl_IL.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="e")
        self.scl_IL.grid(row=3, column=1, padx=5, sticky="ew")
        self.scl_IL.set(self.activeModel.percentIl)
        lbl_IP.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="e")
        self.scl_IP.grid(row=4, column=1, padx=5, sticky="ew")
        self.scl_IP.set(self.activeModel.percentIp)
        # 2nd Block
        lbl_WSN.grid(row=0, column=2, padx=5, pady=(7, 0), sticky="e")
        self.cmb_WSN.grid(row=0, column=3, padx=5, pady=(7, 0))
        self.cmb_WSN.set(self.activeModel.WSNnumber)
        self.cmb_WSN.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_DEP.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.cmb_DEP.grid(row=1, column=3, padx=5, pady=5)
        self.cmb_DEP.set(self.activeModel.deploymentArea)
        self.cmb_DEP.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_TRNS.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.cmb_TRNS.grid(row=2, column=3, padx=5, pady=5)
        self.cmb_TRNS.set(self.activeModel.transmissionRange)
        self.cmb_TRNS.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_CNTCT.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.cmb_CNTCT.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
        self.cmb_CNTCT.set(self.activeModel.contactRate)
        self.cmb_CNTCT.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_SCAN.grid(row=4, column=2, padx=5, pady=5, sticky="e")
        self.scl_SCAN.grid(row=4, column=3, padx=5, sticky="ew")
        self.scl_SCAN.set(self.activeModel.botScanningRate)
        # 3rd Block
        lbl_Ptrns.grid(row=0, column=4, padx=5, pady=(7, 0), sticky="e")
        self.scl_Ptrns.grid(row=0, column=5, padx=5, pady=(7, 0))
        self.scl_Ptrns.set(self.activeModel.botPtransmission)
        lbl_IrPsu.grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.scl_IrPsu.grid(row=1, column=5, padx=5, sticky="ew")
        self.scl_IrPsu.set(self.activeModel.IrPsuccess)
        lbl_IlPsu.grid(row=2, column=4, padx=5, pady=5, sticky="e")
        self.scl_IlPsu.grid(row=2, column=5, padx=5, sticky="ew")
        self.scl_IlPsu.set(self.activeModel.IlPsuccess)
        lbl_IpPsu.grid(row=3, column=4, padx=5, pady=5, sticky="e")
        self.scl_IpPsu.grid(row=3, column=5, padx=5, sticky="ew")
        self.scl_IpPsu.set(self.activeModel.IpPsuccess)
        lbl_Name.grid(row=4, column=4, padx=5, pady=5, sticky="e")
        self.entry_Name.grid(row=4, column=5, padx=5, pady=5, sticky="e")
        self.entry_Name.insert(END, self.activeModel.Name[5:])
        # 4th Block
        lbl_MSG.grid(row=0, column=6, padx=5, pady=(7, 0), sticky="e")
        self.cmb_MSG.grid(row=0, column=7, padx=5, pady=(7, 0))
        self.cmb_MSG.set(self.activeModel.meanMessageSize)
        self.cmb_MSG.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_PWR.grid(row=1, column=6, padx=5, pady=5, sticky="e")
        self.cmb_PWR.grid(row=1, column=7, padx=5, pady=5)
        self.cmb_PWR.set(self.activeModel.meanPower)
        self.cmb_PWR.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_BTRY.grid(row=2, column=6, padx=5, pady=5, sticky="e")
        self.cmb_BTRY.grid(row=2, column=7, padx=5, pady=5)
        self.cmb_BTRY.set(self.activeModel.totalBattery)
        self.cmb_BTRY.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_RR.grid(row=3, column=6, padx=5, pady=5, sticky="e")
        self.scl_RR.grid(row=3, column=7, padx=5, sticky="ew")
        self.scl_RR.set(self.activeModel.recoveryRate)
        lbl_T.grid(row=4, column=6, padx=5, pady=5, sticky="e")
        self.scl_T.grid(row=4, column=7, padx=5, sticky="ew")
        self.scl_T.set(self.activeModel.Timesteps)
        # 5th Block
        btn_RUN.grid(row=0, column=8, padx=(60, 5), pady=(7, 4), sticky="ew")
        btn_INSP.grid(row=1, column=8, padx=(60, 5), pady=4, sticky="ew")
        btn_SAVE.grid(row=2, column=8, padx=(60, 5), pady=4, sticky="ew")
        btn_SAVE_NEW.grid(row=3, column=8, padx=(60, 5), pady=4, sticky="ew")
        btn_RTRN.grid(row=4, column=8, padx=(60, 5), pady=4, sticky="ew")

        # Matching the model to the default figures
        self.updateModel(1)

        # Setting up the canvas area for the graphs in frame_1_top
        figure = plt.figure(facecolor="#453354")
        self.canvas = FigureCanvasTkAgg(figure, frame_1_top)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = [figure.add_subplot(2, 2, x + 1, facecolor="#453354") for x in range(4)]

        for x in range(4):
            self.ax[x].ticklabel_format(style="plain")

        # Calling the graphs
        self.updateGraphs(self.activeModel)

    # Method to update the onscreen graphs to whatever the current model configuration is
    def updateGraphs(self, model):
        S1, Ir1, Il1, Ip1 = model.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, model.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(4)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, 'g', label="Susceptible")
        self.ax[0].plot(T1, Ir1, 'y', label="Random-Scanning Infected")
        self.ax[0].plot(T1, Il1, 'b', label="Local Scanning Infected")
        self.ax[0].plot(T1, Ip1, 'c', label="Peer-to-Peer Infected")
        self.ax[0].set_title("Population Sizes Over Time - Individual Virus Infection Types")

        # Plotting the second graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]
        # Temporary save for every time a population goes negative
        for x in range(len(pop)):
            if pop[x] < 0:
                pop[x] = 0

        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible", "Random-Scanning Infected", "Local Scanning Infected", "Peer-to-Peer Infected"]
        self.ax[1].pie(pop, explode=explode, labels=labels)
        self.ax[1].set_title("Population Sizes on the Final Recorded Day")

        # Plotting the third graph
        self.ax[2].plot(T1, S1, 'g', label="Susceptible")
        self.ax[2].plot(T1, I1, 'r', label="All Infected")
        self.ax[2].set_title("Population Sizes Over Time - Grouped Virus Infection Types")

        # Plotting fourth graph
        self.ax[3].plot(T1, S1, 'g', label="Susceptible")
        self.ax[3].plot(T1, Ir1, 'y', label="Random-Scanning Infected")
        self.ax[3].plot(T1, Il1, 'b', label="Local Scanning Infected")
        self.ax[3].plot(T1, Ip1, 'c', label="Peer-to-Peer Infected")
        self.ax[3].legend(loc="best")
        self.ax[3].set_title("Legend")

        self.canvas.draw()

    # This method is called whenever a value option is changed, to automatically update the active models parameters
    # so that when the model is run and the graphs are shown, they are correct
    def updateModel(self, Stub):

        if len(self.entry_Name.get()) == 0:
            self.controller.popup("Invalid Save", "Please enter a unique name for the model")

        else:
            Name = str("SIS: " + self.entry_Name.get())
            N = int(self.cmb_N.get())
            S = float(self.scl_S.get())
            IR = float(self.scl_IR.get())
            IL = float(self.scl_IL.get())
            IP = float(self.scl_IP.get())
            WSN = int(self.cmb_WSN.get())
            DEP = int(self.cmb_DEP.get()) * int(self.cmb_DEP.get())
            TRNS = int(self.cmb_TRNS.get())
            CNTCT = int(self.cmb_CNTCT.get())
            SCAN = int(self.scl_SCAN.get())
            PTrns = float(self.scl_Ptrns.get())
            IrPsu = float(self.scl_IrPsu.get())
            IlPsu = float(self.scl_IlPsu.get())
            IpPsu = float(self.scl_IpPsu.get())
            MSG = int(self.cmb_MSG.get())
            PWR = float(self.cmb_PWR.get())
            BTRY = int(self.cmb_BTRY.get())
            RR = float(self.scl_RR.get())
            T = int(self.scl_T.get())

            self.activeModel = sis.SIS(Name, N, S, IR, IL, IP, WSN, DEP, TRNS, CNTCT, SCAN, PTrns, IrPsu, IlPsu, IpPsu,
                                       MSG, PWR, BTRY, RR, T)


    def updateVariables(self, controller):
        self.activeModel = controller.getActiveModel()
        self.activeModelIndex = controller.getActiveModelIndex()

        self.cmb_N.set(self.activeModel.N)
        self.scl_S.set(self.activeModel.percentS)
        self.scl_IR.set(self.activeModel.percentIr)
        self.scl_IL.set(self.activeModel.percentIl)
        self.scl_IP.set(self.activeModel.percentIp)
        self.cmb_WSN.set(self.activeModel.WSNnumber)
        self.cmb_DEP.set(self.activeModel.deploymentArea)
        self.cmb_TRNS.set(self.activeModel.transmissionRange)
        self.cmb_CNTCT.set(self.activeModel.contactRate)
        self.scl_SCAN.set(self.activeModel.botScanningRate)
        self.scl_Ptrns.set(self.activeModel.botPtransmission)
        self.scl_IrPsu.set(self.activeModel.IrPsuccess)
        self.scl_IlPsu.set(self.activeModel.IlPsuccess)
        self.scl_IpPsu.set(self.activeModel.IpPsuccess)
        self.entry_Name.delete(0, 'end')
        self.entry_Name.insert(END, self.activeModel.Name[5:])
        self.cmb_MSG.set(self.activeModel.meanMessageSize)
        self.cmb_PWR.set(self.activeModel.meanPower)
        self.cmb_BTRY.set(self.activeModel.totalBattery)
        self.scl_RR.set(self.activeModel.recoveryRate)
        self.scl_T.set(self.activeModel.Timesteps)

        self.updateGraphs(self.activeModel)
