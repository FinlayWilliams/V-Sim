import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
from model import sis


class SISControlInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        ####################################### Instantiating ALL elements ############################################

        # Upper area for displaying and model option buttons
        frame_top = tk.Frame(self, bg="#453354")
        # Button: refreshes graphs to current model config
        btn_Refresh_Graph = tk.Button(frame_top, wraplength=40, width=5, text="Refresh Graphs", font=("Arial", 7),
                                      command=self.updateGraphs)
        # Button: Resets model config and refreshes graphs
        btn_Reset = tk.Button(frame_top, wraplength=40, width=5, text="Reset Model", font=("Arial", 7),
                              command=lambda: [self.updateVariables(controller), self.updateGraphs()])
        # Button: opens the inspect model page with the currently selected model
        btn_Inspect = tk.Button(frame_top, wraplength=40, width=5, text="Inspect model", font=("Arial", 7))
        # Button: overwrites the current model "saving" it
        btn_Save = tk.Button(frame_top, wraplength=40, width=5, text="Save Model", font=("Arial", 7),
                             command=lambda: [self.updateModel(1),
                                              controller.overwriteModel(self.activeModelIndex, self.activeModel)])
        # Button: add this model configuration to the list
        btn_Save_New = tk.Button(frame_top, wraplength=40, width=5, text="Save New", font=("Arial", 7),
                                 command=lambda: [self.updateModel(1), controller.addModel(self.activeModel)])
        # Button: takes the user to the home page
        btn_Return = tk.Button(frame_top, wraplength=40, width=5, text="Return Home", font=("Arial", 7),
                             command=lambda: controller.display("SISControlInterface", "HomeInterface"))

        # This frame holds the graphs
        canvas_frame = tk.Frame(frame_top, bg="#6e6e6e")
        # Frame for the legend to sit in + legend labels
        canvas_info_frame_border = tk.Frame(frame_top, bg="#453354")
        canvas_info_frame = tk.Frame(frame_top, bg="#654e78")
        lbl_legend_title = tk.Label(canvas_info_frame, bg="#654e78", width=25, pady=4, text="Legend :",
                                    font=("Arial", 14))
        lbl_legend1 = tk.Label(canvas_info_frame, bg="#2ca02c", width=25, pady=4, text="(S) Susceptible",
                               font=("Arial", 12), fg="white")
        lbl_legend2 = tk.Label(canvas_info_frame, bg="#9467bd", width=25, pady=4, text="(IR) Random-Scanning",
                               font=("Arial", 12), fg="white")
        lbl_legend3 = tk.Label(canvas_info_frame, bg="#1f77b4", width=25, pady=4, text="(IL) Local Scanning",
                               font=("Arial", 12), fg="white")
        lbl_legend4 = tk.Label(canvas_info_frame, bg="#17becf", width=25, pady=4, text="(IP) Peer-to-Peer",
                               font=("Arial", 12), fg="white")
        lbl_legend5 = tk.Label(canvas_info_frame, bg="#d62728", width=25, pady=4,
                               text="(I) All Infection Types Grouped", font=("Arial", 12), fg="white")

        # Separates graphs from the controls
        frame_mid = tk.Frame(self, bg="#6e6e6e")
        lbl_Options = tk.Label(frame_mid, text="Model Variables", bg="#6e6e6e", font=("Arial", 10), fg="white")

        # Lower area for the controls
        frame_bot = tk.Frame(self, bg="#a8a8a8")
        # All labels and widgets for inputting variables
        lbl_Model_Name = tk.Label(frame_bot, text="Model Name:", bg="#a8a8a8", font=("Arial", 10))
        self.entry_Name = tk.Entry(frame_bot)
        lbl_N = tk.Label(frame_bot, text="Initial Node Population Size (N):")
        N_Options = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"]
        self.cmb_N = ttk.Combobox(frame_bot, values=N_Options, state="readonly")
        lbl_S = tk.Label(frame_bot, text="Initial S Size (%):")
        self.scl_S = tk.Scale(frame_bot, from_=0, to=1, resolution=0.01, orient="horizontal",
                              command=self.updateModel)
        lbl_IR = tk.Label(frame_bot, text="Initial IR Size (%):")
        self.scl_IR = tk.Scale(frame_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)
        lbl_IL = tk.Label(frame_bot, text="Initial IL Size (%):")
        self.scl_IL = tk.Scale(frame_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)
        lbl_IP = tk.Label(frame_bot, text="Initial IP Size (%):")
        self.scl_IP = tk.Scale(frame_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)
        lbl_WSN = tk.Label(frame_bot, text="Wireless Sensor Network Count:")
        WSN_Options = ["1", "5", "10", "20", "50"]
        self.cmb_WSN = ttk.Combobox(frame_bot, values=WSN_Options, state="readonly")
        lbl_DEP = tk.Label(frame_bot, text="Node Deployment Area: (m x m)")
        DEP_Options = ["25", "50", "100", "150"]
        self.cmb_DEP = ttk.Combobox(frame_bot, values=DEP_Options, state="readonly")
        lbl_TRNS = tk.Label(frame_bot, text="Node Transmission Range (m):")
        TRNS_Options = ["1", "5", "10", "15"]
        self.cmb_TRNS = ttk.Combobox(frame_bot, values=TRNS_Options, state="readonly")
        lbl_CNTCT = tk.Label(frame_bot, text="S Node Contact Rate:")
        CNTCT_Options = ["1", "5", "10", "20", "50", "75", "100", "250"]
        self.cmb_CNTCT = ttk.Combobox(frame_bot, values=CNTCT_Options, state="readonly")
        lbl_SCAN = tk.Label(frame_bot, text="Botnet Scanning Rate (/sec):")
        self.scl_SCAN = tk.Scale(frame_bot, from_=1, to=250, resolution=1, orient="horizontal",
                                 command=self.updateModel)
        lbl_Ptrns = tk.Label(frame_bot, text="PTransmission Rate:")
        self.scl_Ptrns = tk.Scale(frame_bot, from_=0.01, to=1, resolution=0.01, orient="horizontal",
                                  command=self.updateModel)
        lbl_IrPsu = tk.Label(frame_bot, text="IR PSuccess Rate:")
        self.scl_IrPsu = tk.Scale(frame_bot, from_=0.00001, to=1, resolution=0.00001, orient="horizontal",
                                  command=self.updateModel)
        lbl_IlPsu = tk.Label(frame_bot, text="IL PSuccess Rate:")
        self.scl_IlPsu = tk.Scale(frame_bot, from_=0.01, to=1, resolution=0.01, orient="horizontal",
                                  command=self.updateModel)
        lbl_IpPsu = tk.Label(frame_bot, text="IP PSuccess Rate:")
        self.scl_IpPsu = tk.Scale(frame_bot, from_=0.01, to=1, resolution=0.01, orient="horizontal",
                                  command=self.updateModel)
        lbl_MSG = tk.Label(frame_bot, text="Mean Message Size (Bytes):")
        MSG_Options = ["10", "20", "50", "100"]
        self.cmb_MSG = ttk.Combobox(frame_bot, values=MSG_Options, state="readonly")
        lbl_PWR = tk.Label(frame_bot, text="Mean Power to Send Message (mA):")
        PWR_Options = ["0.25", "0.5", "0.75", "1", "1.25"]
        self.cmb_PWR = ttk.Combobox(frame_bot, values=PWR_Options, state="readonly")
        lbl_BTRY = tk.Label(frame_bot, text="Total Node Battery Capacity (mAs):")
        BTRY_Options = ["216000", "432000", "864000", "1728000", "3456000"]
        self.cmb_BTRY = ttk.Combobox(frame_bot, values=BTRY_Options, state="readonly")
        lbl_RR = tk.Label(frame_bot, text="Recovery rate:")
        self.scl_RR = tk.Scale(frame_bot, from_=0.250, to=1, digits=3, resolution=0.250, orient="horizontal",
                               command=self.updateModel)
        lbl_T = tk.Label(frame_bot, text="Days to Observe:")
        self.scl_T = tk.Scale(frame_bot, from_=1, to=365, resolution=1, orient="horizontal",
                              command=self.updateModel)

        ####################################### Placing ALL elements ############################################

        ## Frame Top Half
        frame_top.place(relheight=0.70, relwidth=1)
        btn_Refresh_Graph.place(x=10, y=13)
        btn_Reset.place(x=10, y=64)
        btn_Inspect.place(x=10, y=115)
        btn_Save.place(x=10, y=166)
        btn_Save_New.place(x=10, y=217)
        btn_Return.place(x=10, y=560)
        canvas_frame.place(relheight=1, relwidth=0.963, x=58)
        canvas_info_frame_border.place(relheight=0.5, relwidth=0.47, x=814, y=303)
        canvas_info_frame.place(relheight=0.485, relwidth=0.465, x=824, y=312)
        lbl_legend_title.pack()
        lbl_legend1.pack()
        lbl_legend2.pack()
        lbl_legend3.pack()
        lbl_legend4.pack()
        lbl_legend5.pack()

        ## Frame Mid
        frame_mid.place(y=605, relheight=0.05, relwidth=1)
        lbl_Options.pack()

        ## Frame Bottom Half
        frame_bot.place(y=628, relheight=0.30, relwidth=1)
        # 1st Block
        lbl_Model_Name.grid(row=0, column=0, padx=30, sticky="w")
        self.entry_Name.grid(row=1, column=0, padx=30, sticky="nw")
        # 2nd Block
        lbl_N.grid(row=0, column=1, padx=(10, 5), pady=(7, 0), sticky="e")
        self.cmb_N.grid(row=0, column=2, padx=5, pady=(7, 0))
        self.cmb_N.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_S.grid(row=1, column=1, padx=(10, 5), pady=5, sticky="e")
        self.scl_S.grid(row=1, column=2, padx=5, sticky="ew")
        lbl_IR.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="e")
        self.scl_IR.grid(row=2, column=2, padx=5, sticky="ew")
        lbl_IL.grid(row=3, column=1, padx=(10, 5), pady=5, sticky="e")
        self.scl_IL.grid(row=3, column=2, padx=5, sticky="ew")
        lbl_IP.grid(row=4, column=1, padx=(10, 5), pady=5, sticky="e")
        self.scl_IP.grid(row=4, column=2, padx=5, sticky="ew")
        # 3rd Block
        lbl_WSN.grid(row=0, column=3, padx=5, pady=(7, 0), sticky="e")
        self.cmb_WSN.grid(row=0, column=4, padx=5, pady=(7, 0))
        self.cmb_WSN.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_DEP.grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.cmb_DEP.grid(row=1, column=4, padx=5, pady=5)
        self.cmb_DEP.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_TRNS.grid(row=2, column=3, padx=5, pady=5, sticky="e")
        self.cmb_TRNS.grid(row=2, column=4, padx=5, pady=5)
        self.cmb_TRNS.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_CNTCT.grid(row=3, column=3, padx=5, pady=5, sticky="e")
        self.cmb_CNTCT.grid(row=3, column=4, padx=5, pady=5, sticky="ew")
        self.cmb_CNTCT.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_SCAN.grid(row=4, column=3, padx=5, pady=5, sticky="e")
        self.scl_SCAN.grid(row=4, column=4, padx=5, sticky="ew")
        # 4th Block
        lbl_Ptrns.grid(row=0, column=5, padx=5, pady=(7, 0), sticky="e")
        self.scl_Ptrns.grid(row=0, column=6, padx=5, pady=(7, 0))
        lbl_IrPsu.grid(row=1, column=5, padx=5, pady=5, sticky="e")
        self.scl_IrPsu.grid(row=1, column=6, padx=5, sticky="ew")
        lbl_IlPsu.grid(row=2, column=5, padx=5, pady=5, sticky="e")
        self.scl_IlPsu.grid(row=2, column=6, padx=5, sticky="ew")
        lbl_IpPsu.grid(row=3, column=5, padx=5, pady=5, sticky="e")
        self.scl_IpPsu.grid(row=3, column=6, padx=5, sticky="ew")
        # 5th Block
        lbl_MSG.grid(row=0, column=7, padx=5, pady=(7, 0), sticky="e")
        self.cmb_MSG.grid(row=0, column=8, padx=5, pady=(7, 0))
        self.cmb_MSG.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_PWR.grid(row=1, column=7, padx=5, pady=5, sticky="e")
        self.cmb_PWR.grid(row=1, column=8, padx=5, pady=5)
        self.cmb_PWR.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_BTRY.grid(row=2, column=7, padx=5, pady=5, sticky="e")
        self.cmb_BTRY.grid(row=2, column=8, padx=5, pady=5)
        self.cmb_BTRY.bind("<<ComboboxSelected>>", self.updateModel)
        lbl_RR.grid(row=3, column=7, padx=5, pady=5, sticky="e")
        self.scl_RR.grid(row=3, column=8, padx=5, sticky="ew")
        lbl_T.grid(row=4, column=7, padx=5, pady=5, sticky="e")
        self.scl_T.grid(row=4, column=8, padx=5, sticky="ew")

        # Calling the method to allign the variables and populate all fields
        self.updateVariables(controller)

        # Setting up the canvas area for the graphs in frame_top #a983c9
        figure = plt.figure(facecolor="#654e78")
        self.canvas = FigureCanvasTkAgg(figure, canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = [figure.add_subplot(2, 2, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(3):
            self.ax[x].ticklabel_format(style="plain")
        figure.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=3)

    # Method to update the onscreen graphs to whatever the current model configuration is
    def updateGraphs(self):
        S1, Ir1, Il1, Ip1 = self.activeModel.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.activeModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(3)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
        self.ax[0].plot(T1, Il1, "#1f77b4", label="Local Scanning Infected")
        self.ax[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
        self.ax[0].set_xlabel("Timesteps (Days)")
        self.ax[0].set_ylabel("Node Count")
        self.ax[0].set_title("Population Sizes Over Time - Individual Infection Types - S, IR, IL, IP")
        # Plotting the second graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning Infected: {:.0f}".format(pop[1]),
                  "Local Scanning Infected: {:.0f}".format(pop[2]), "Peer-to-Peer Infected: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
        self.ax[1].pie(pop, explode=explode, labels=labels, colors=colours)
        self.ax[1].set_title("Population Sizes on the Final Recorded Day")
        # Plotting the third graph
        self.ax[2].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.ax[2].plot(T1, I1, '#d62728', label="All Infected")
        self.ax[2].set_xlabel("Timesteps (Days)")
        self.ax[2].set_ylabel("Node Count")
        self.ax[2].set_title("Node Population Sizes Over Time - Grouped Infection Types - S, I = (IR + IL + IP)")

        self.canvas.draw()

    # Method: called when a value option is changed, to automatically update the active models parameters
    def updateModel(self, Stub):
        if len(self.entry_Name.get()) == 0:
            self.controller.popup("Invalid Save", "Please enter a name for the model!")
        else:
            Name = str("SIS: " + self.entry_Name.get())
            N = int(self.cmb_N.get())
            S = float(self.scl_S.get())
            IR = float(self.scl_IR.get())
            IL = float(self.scl_IL.get())
            IP = float(self.scl_IP.get())
            WSN = int(self.cmb_WSN.get())
            DEP = int(self.cmb_DEP.get())
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

            newActiveModel = sis.SIS(Name, N, S, IR, IL, IP, WSN, DEP, TRNS, CNTCT, SCAN, PTrns, IrPsu, IlPsu, IpPsu,
                                       MSG, PWR, BTRY, RR, T)

            if not self.checkValid(newActiveModel):
                self.controller.popup("Invalid Model Configuration", "Population Sizes will reach negative values!")
            else:
                self.activeModel = newActiveModel

    # Good to have it here but it makes it really slow so it is for now, #### out and the R button is in place
    # self.updateGraphs()

    # Method: called once when this interface is created + everytime this interface is opened to ensure all variables
    # are updated and correct
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

    # Method: checks if the current configuration is valid by checking no population size dips below zero
    def checkValid(self, newActiveModel):
        S1, Ir1, Il1, Ip1 = newActiveModel.runModel()
        populations = [S1, Ir1, Il1, Ip1]
        for P in populations:
            for value in P:
                if value < 0:
                    return False
        return True
