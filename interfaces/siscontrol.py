import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
from models import sis


class SISControlInterface(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.activeConfiguration = controller.activeConfiguration

        ######################################## Instantiating ALL elements ############################################
        frameTop = tk.Frame(self, bg="#453354")
        # Button: Resets configuration to the last saved state and refreshes graphs
        btnReset = tk.Button(frameTop, wraplength=40, width=5, text="Reset Config", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: [self.updateVariables(controller), self.updateGraphs(self.activeConfiguration)])
        # Button: overwrites the current configuration "saving" it
        btnSave = tk.Button(frameTop, wraplength=40, width=5, text="Save Config", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                            command=lambda: [self.updateConfiguration(1),
                                             controller.overwriteConfiguration(self.activeConfigurationIndex, self.activeConfiguration),
                                             controller.setActiveConfiguration(self.activeConfigurationIndex)])
        # Button: add this configuration to the controller list as a new save
        btnSaveNew = tk.Button(frameTop, wraplength=40, width=5, text="Save New", font=("Arial", 7), bg="#6e6e6e", relief="ridge", fg="white",
                               command=lambda: [self.updateConfiguration(1), controller.addConfiguration(self.activeConfiguration),
                                                controller.setActiveConfiguration(len(controller.configurations) - 1)])
        # Button: opens the inspect page with the currently selected configuration
        btnInspect = tk.Button(frameTop, wraplength=40, width=5, text="Inspect Config", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                               command=lambda: self.checkConfigurationSaved(controller, 0))
        # Button: takes the user to the home page
        btnReturn = tk.Button(frameTop, wraplength=40, width=5, text="Return Home", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                             command=lambda: self.checkConfigurationSaved(controller, 1))
        # This frame holds the graphs
        canvasFrame = tk.Frame(frameTop, bg="#654e78")

        # Configuration Name Options
        lblConfigurationName = tk.Label(frameTop, text="Configuration Name :", bg="#453354", font=("Calibri", 14), fg="white")
        self.entryName = tk.Entry(frameTop, font=("Arial", 12), width=32)

        # Frame for the legend to sit in + legend labels
        lblLegendTitle = tk.Label(frameTop, bg="#453354", width=25, pady=4, text="Legend :", font=("Calibri", 14, "bold"), fg="white")
        lblLegend1 = tk.Label(frameTop, bg="#2ca02c", width=25, pady=4, text="(S) Susceptible", font=("Arial", 12), fg="white")
        lblLegend2 = tk.Label(frameTop, bg="#9467bd", width=25, pady=4, text="(IR) Random-Scanning", font=("Arial", 12), fg="white")
        lblLegend3 = tk.Label(frameTop, bg="#1f77b4", width=25, pady=4, text="(IL) Local Scanning", font=("Arial", 12), fg="white")
        lblLegend4 = tk.Label(frameTop, bg="#17becf", width=25, pady=4, text="(IP) Peer-to-Peer", font=("Arial", 12), fg="white")
        lblLegend5 = tk.Label(frameTop, bg="#d62728", width=25, pady=4, text="(I) Infection Types Grouped", font=("Arial", 12), fg="white")

        # Frame to display configuration statistics
        lblConfigurationStatistics = tk.Label(frameTop, text="Configuration Statistics :", bg="#453354", font=("Calibri", 14), fg="white")
        frameConfigurationStats = tk.Frame(frameTop, width=305, height=285, bg="#654e78")
        frameConfigurationStats.grid_propagate(False)
        lblCurrentSLoc = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="SLoc Count / S Population : ")
        self.currentSLoc = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentSNhb = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="SNhb Count / S Population : ")
        self.currentSNhb = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentBr = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="IR Infection Rate : ")
        self.currentBr = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentBl = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="IL Infection Rate : ")
        self.currentBl = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentBp = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="IP Infection Rate : ")
        self.currentBp = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentDthB = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="Benign Death Rate : ")
        self.currentDthB = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentDthR = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="IR Node Death Rate : ")
        self.currentDthR = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentDthL = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="IL Node Death Rate : ")
        self.currentDthL = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")
        lblCurrentDthP = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12), text="IP Node Death Rate : ")
        self.currentDthP = tk.Label(frameConfigurationStats, bg="#654e78", font=("Calibri", 12, "bold"), fg="white")

        # Separates graphs from the controls
        frameMid = tk.Frame(self, bg="#6e6e6e")
        lblOptions = tk.Label(frameMid, text="Starting Conditions", bg="#6e6e6e", font=("Arial", 10), fg="white")

        # Lower area for the controls
        frameBot = tk.Frame(self, bg="#a8a8a8")
        # All labels and widgets for inputting variables
        lblN = tk.Label(frameBot, text="Total Node Population Size (N):")
        NOptions = ["500", "1000", "2000", "10000"]
        self.cmbN = ttk.Combobox(frameBot, values=NOptions, state="readonly")
        lblBotCount = tk.Label(frameBot, text="Bot Population Size (I):")
        IOptions = ["0", "1", "3", "10", "100", "1000"]
        self.cmbBotCount = ttk.Combobox(frameBot, values=IOptions, state="readonly")
        lblS = tk.Label(frameBot, text="Susceptible Population Size (S):")
        self.lblSMatch = tk.Label(frameBot, bg="white")
        lblWSN = tk.Label(frameBot, text="Wireless Sensor Network Count:")
        WSNOptions = ["1", "5", "10", "20", "50"]
        self.cmbWSN = ttk.Combobox(frameBot, values=WSNOptions, state="readonly")
        lblDEP = tk.Label(frameBot, text="Node Deployment Area (m²)")
        DEPOptions = ["25", "50", "100", "150"]
        self.cmbDEP = ttk.Combobox(frameBot, values=DEPOptions, state="readonly")
        lblTRNS = tk.Label(frameBot, text="Node Transmission Range (m):")
        TRNSOptions = ["1", "5", "10", "15", "100"]
        self.cmbTRNS = ttk.Combobox(frameBot, values=TRNSOptions, state="readonly")
        lblCNTCT = tk.Label(frameBot, text="S Node Contact Rate:")
        CNTCTOptions = ["1", "5", "10", "20", "50", "75", "100", "250"]
        self.cmbCNTCT = ttk.Combobox(frameBot, values=CNTCTOptions, state="readonly")
        lblSCAN = tk.Label(frameBot, text="Bot Scanning Rate (/sec):")
        self.sclSCAN = tk.Scale(frameBot, from_=1, to=250, resolution=1, orient="horizontal")
        POptions = ["0%", "Low", "Expected", "High", "100%"]
        lblIrPsu = tk.Label(frameBot, text="IR PSuccess Rate:")
        self.cmbIrPsu = ttk.Combobox(frameBot, values=POptions, state="readonly")
        lblIlPsu = tk.Label(frameBot, text="IL PSuccess Rate:")
        self.cmbIlPsu = ttk.Combobox(frameBot, values=POptions, state="readonly")
        lblIpPsu = tk.Label(frameBot, text="IP PSuccess Rate:")
        self.cmbIpPsu = ttk.Combobox(frameBot, values=POptions, state="readonly")
        lblPtrns = tk.Label(frameBot, text="PTransmission Rate:")
        self.cmbPtrns = ttk.Combobox(frameBot, values=POptions, state="readonly")
        lblMSG = tk.Label(frameBot, text="Mean Message Size (Bytes):")
        MSGOptions = ["16", "50", "150"]
        self.cmbMSG = ttk.Combobox(frameBot, values=MSGOptions, state="readonly", width=15)
        lblPWR = tk.Label(frameBot, text="Mean Power per Message (mA):")
        PWROptions = ["0.25", "0.75", "1.25"]
        self.cmbPWR = ttk.Combobox(frameBot, values=PWROptions, state="readonly", width=15)
        lblBTRY = tk.Label(frameBot, text="Node Battery Capacity (mAs):")
        BTRYOptions = ["216000", "864000", "3456000"]
        self.cmbBTRY = ttk.Combobox(frameBot, values=BTRYOptions, state="readonly", width=15)
        lblRR = tk.Label(frameBot, text="Security:")
        RROptions = ["Low", "Medium", "High"]
        self.cmbRR = ttk.Combobox(frameBot, values=RROptions, state="readonly")
        lblIDS = tk.Label(frameBot, text="IDS Active:")
        self.checkIDSBool = BooleanVar()
        self.checkIDS = tk.Checkbutton(frameBot, onvalue=True, offvalue=False, bg="#a8a8a8", activebackground="#a8a8a8", variable=self.checkIDSBool, command=lambda:self.updateConfiguration(1))
        lblT = tk.Label(frameBot, text="Hours to Observe:")
        self.sclT = tk.Scale(frameBot, from_=1, to=30, resolution=1, orient="horizontal")
        lblTPlus = tk.Label(frameBot, text="Add 250 Hours: ")
        self.checkTimeBool = BooleanVar()
        self.checkTime = tk.Checkbutton(frameBot, onvalue=True, offvalue=False, bg="#a8a8a8", activebackground="#a8a8a8", variable=self.checkTimeBool, command=lambda: self.updateConfiguration(1))

        # Setting up the canvas area for the graphs in frameTop
        figure = plt.figure(facecolor="#654e78")
        self.canvas = FigureCanvasTkAgg(figure, canvasFrame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = [figure.add_subplot(2, 1, x + 1, facecolor="#453354") for x in range(2)]
        for x in range(2):
            self.ax[x].ticklabel_format(style="plain")
        figure.tight_layout(rect=[0.01, 0.03, 1, 0.95], h_pad=3)

        ########################################### Placing ALL elements ###############################################
        ## Frame Top Half
        frameTop.place(relheight=0.70, relwidth=1)
        btnReturn.place(x=10, y=13)
        btnInspect.place(x=10, y=64)
        btnReset.place(x=10, y=608)
        btnSave.place(x=10, y=659)
        btnSaveNew.place(x=10, y=710)
        canvasFrame.place(relheight=1, relwidth=0.73, x=58)
        lblLegendTitle.place(x=1554, y=47)
        lblLegend1.place(x=1572, y=80)
        lblLegend2.place(x=1572, y=113)
        lblLegend3.place(x=1572, y=146)
        lblLegend4.place(x=1572, y=179)
        lblLegend5.place(x=1572, y=212)
        lblConfigurationStatistics.place(x=1591, y=278)
        frameConfigurationStats.place(x=1535, y=307)
        lblCurrentSLoc.grid(row=0, column=0, sticky="e", padx=3, pady=3)
        self.currentSLoc.grid(row=0, column=1, sticky="w", padx=3, pady=3)
        lblCurrentSNhb.grid(row=1, column=0, sticky="e", padx=3, pady=3)
        self.currentSNhb.grid(row=1, column=1, sticky="w", padx=3, pady=3)
        lblCurrentBr.grid(row=2, column=0, sticky="e", padx=3, pady=3)
        self.currentBr.grid(row=2, column=1, sticky="w", padx=3, pady=3)
        lblCurrentBl.grid(row=3, column=0, sticky="e", padx=3, pady=3)
        self.currentBl.grid(row=3, column=1, sticky="w", padx=3, pady=3)
        lblCurrentBp.grid(row=4, column=0, sticky="e", padx=3, pady=3)
        self.currentBp.grid(row=4, column=1, sticky="w", padx=3, pady=3)
        lblCurrentDthB.grid(row=5, column=0, sticky="e", padx=3, pady=3)
        self.currentDthB.grid(row=5, column=1, sticky="w", padx=3, pady=3)
        lblCurrentDthR.grid(row=6, column=0, sticky="e", padx=3, pady=3)
        self.currentDthR.grid(row=6, column=1, sticky="w", padx=3, pady=3)
        lblCurrentDthL.grid(row=7, column=0, sticky="e", padx=3, pady=3)
        self.currentDthL.grid(row=7, column=1, sticky="w", padx=3, pady=3)
        lblCurrentDthP.grid(row=8, column=0, sticky="e", padx=3, pady=3)
        self.currentDthP.grid(row=8, column=1, sticky="w", padx=3, pady=3)
        lblConfigurationName.place(x=1600, y=630)
        self.entryName.place(x=1540, y=660)
        ## Frame Mid
        frameMid.place(y=755, relheight=0.05, relwidth=1)
        lblOptions.pack()
        ## Frame Bottom Half
        frameBot.place(y=778, relheight=0.30, relwidth=1)
        # 1st Block
        lblN.grid(row=0, column=0, padx=(95, 10), pady=(15, 10), sticky="e")
        self.cmbN.grid(row=0, column=1, padx=10, pady=(15, 10))
        self.cmbN.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblS.grid(row=1, column=0, padx=(95, 10), pady=10, sticky="e")
        self.lblSMatch.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        lblBotCount.grid(row=2, column=0, padx=(95, 10), pady=10, sticky="e")
        self.cmbBotCount.grid(row=2, column=1, padx=10, sticky="ew")
        self.cmbBotCount.bind("<<ComboboxSelected>>", self.updateConfiguration)
        # 2nd Block
        lblWSN.grid(row=0, column=2, padx=(30, 10), pady=(15, 10), sticky="e")
        self.cmbWSN.grid(row=0, column=3, padx=10, pady=(15, 10))
        self.cmbWSN.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblDEP.grid(row=1, column=2, padx=5, pady=10, sticky="e")
        self.cmbDEP.grid(row=1, column=3, padx=10, pady=10)
        self.cmbDEP.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblTRNS.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.cmbTRNS.grid(row=2, column=3, padx=10, pady=10)
        self.cmbTRNS.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblCNTCT.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.cmbCNTCT.grid(row=3, column=3, padx=10, pady=10, sticky="ew")
        self.cmbCNTCT.bind("<<ComboboxSelected>>", self.updateConfiguration)
        # 3rd Block
        lblSCAN.grid(row=0, column=4, padx=(30, 10), pady=(15, 10), sticky="e")
        self.sclSCAN.grid(row=0, column=5, padx=10, pady=(15, 0), sticky="ew")
        self.sclSCAN.bind("<ButtonRelease-1>", self.updateConfiguration)
        lblIrPsu.grid(row=1, column=4, padx=10, pady=10, sticky="e")
        self.cmbIrPsu.grid(row=1, column=5, padx=(0, 10), sticky="ew")
        self.cmbIrPsu.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblIlPsu.grid(row=2, column=4, padx=10, pady=10, sticky="e")
        self.cmbIlPsu.grid(row=2, column=5, padx=10, sticky="ew")
        self.cmbIlPsu.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblIpPsu.grid(row=3, column=4, padx=10, pady=10, sticky="e")
        self.cmbIpPsu.grid(row=3, column=5, padx=10, sticky="ew")
        self.cmbIpPsu.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblPtrns.grid(row=4, column=4, padx=10, pady=10, sticky="e")
        self.cmbPtrns.grid(row=4, column=5, padx=10)
        self.cmbPtrns.bind("<<ComboboxSelected>>", self.updateConfiguration)
        # 4th Block
        lblMSG.grid(row=0, column=6, padx=(30, 10), pady=(15, 10), sticky="e")
        self.cmbMSG.grid(row=0, column=7, padx=10, pady=(15, 10))
        self.cmbMSG.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblPWR.grid(row=1, column=6, padx=10, pady=10, sticky="e")
        self.cmbPWR.grid(row=1, column=7, padx=10, pady=10)
        self.cmbPWR.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblBTRY.grid(row=2, column=6, padx=10, pady=10, sticky="e")
        self.cmbBTRY.grid(row=2, column=7, padx=10, pady=10)
        self.cmbBTRY.bind("<<ComboboxSelected>>", self.updateConfiguration)
        # 5th Block
        lblRR.grid(row=0, column=8, padx=(30, 10), pady=(15, 10), sticky="e")
        self.cmbRR.grid(row=0, column=9, padx=(10, 0), sticky="ew")
        self.cmbRR.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblIDS.grid(row=1, column=8, padx=10, pady=10, sticky="e")
        self.checkIDS.grid(row=1, column=9, padx=10, pady=10, sticky="w")
        lblT.grid(row=2, column=8, padx=10, pady=10, sticky="e")
        self.sclT.grid(row=2, column=9, padx=10, sticky="ew")
        self.sclT.bind("<ButtonRelease-1>", self.updateConfiguration)
        lblTPlus.grid(row=3, column=8, padx=10, pady=10, sticky="e")
        self.checkTime.grid(row=3, column=9, padx=10, pady=10, sticky="w")
        # Calling the method to align the variables and populate all fields
        self.updateVariables(controller)
        self.updateConfiguration(False)

    # Method to update the onscreen graphs to the current configurations variables
    def updateGraphs(self, configuration):
        S1, Ir1, Il1, Ip1 = configuration.runSimulation()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, configuration.Timesteps, 500)

        print("Distance = {}".format(configuration.distance))

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(2)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
        self.ax[0].plot(T1, Il1, "#1f77b4", label="Local-Scanning Infected")
        self.ax[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
        self.ax[0].set_xlabel("Timesteps (Hours)")
        self.ax[0].set_ylabel("Node Count")
        self.ax[0].set_title("Node Population Sizes Over Time - Individual Infection Types - S, IR, IL, IP")
        self.ax[0].axvline(linewidth=0.5, color="#a8a8a8", x=configuration.Timesteps / 2, linestyle="--")
        # Plotting the second graph
        self.ax[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.ax[1].plot(T1, I1, '#d62728', label="All Infected")
        self.ax[1].set_xlabel("Timesteps (Hours)")
        self.ax[1].set_ylabel("Node Count")
        self.ax[1].set_title("Node Population Sizes Over Time - Grouped Infection Types - S, I = (IR + IL + IP)")
        self.ax[1].axvline(linewidth=0.5, color="#a8a8a8", x=configuration.Timesteps / 2, linestyle="--")
        self.ax[1].axhline(linewidth=0.5, color="#d62728", y=max(I1), linestyle="--", label="Peak I: {}".format(max(I1)))
        self.canvas.draw()

    # Called when a value option is changed, to automatically update the active configurations parameters to match any changes
    def updateConfiguration(self, time):
        if len(self.entryName.get()) == 0:
            self.controller.popup("Invalid Save", "Please Enter a Name for the Configuration!")
        if len(self.entryName.get()) > 30:
            self.controller.popup("Invalid Save", "Please Enter a Shorter Name for the Configuration!")
        else:
            Name = str("IoT-SIS: " + self.entryName.get())
            N = int(self.cmbN.get())
            I = int(self.cmbBotCount.get())
            self.lblSMatch.config(text="{}".format(N - I))
            WSN = int(self.cmbWSN.get())
            DEP = int(self.cmbDEP.get())
            TRNS = int(self.cmbTRNS.get())
            CNTCT = int(self.cmbCNTCT.get())
            SCAN = int(self.sclSCAN.get())
            if self.cmbIrPsu.get() == "0%":
                IrPsu = float(0.00000000001)
            elif self.cmbIrPsu.get() == "Low":
                IrPsu = float(0.005)
            elif self.cmbIrPsu.get() == "Expected":
                IrPsu = float(0.02)
            elif self.cmbIrPsu.get() == "High":
                IrPsu = float(0.05)
            else:
                IrPsu = float(1)
            if self.cmbIlPsu.get() == "0%":
                IlPsu = float(0.00000000001)
            elif self.cmbIlPsu.get() == "Low":
                IlPsu = float(0.05)
            elif self.cmbIlPsu.get() == "Expected":
                IlPsu = float(0.1)
            elif self.cmbIlPsu.get() == "High":
                IlPsu = float(0.25)
            else:
                IlPsu = float(1)
            if self.cmbIpPsu.get() == "0%":
                IpPsu = float(0.00000000001)
            elif self.cmbIpPsu.get() == "Low":
                IpPsu = float(0.45)
            elif self.cmbIpPsu.get() == "Expected":
                IpPsu = float(0.8)
            elif self.cmbIpPsu.get() == "High":
                IpPsu = float(0.95)
            else:
                IpPsu = float(1)
            if self.cmbPtrns.get() == "0%":
                PTrns = float(0.00000000001)
            elif self.cmbPtrns.get() == "Low":
                PTrns = float(0.001)
            elif self.cmbPtrns.get() == "Expected":
                PTrns = float(0.01)
            elif self.cmbPtrns.get() == "High":
                PTrns = float(0.03)
            else:
                PTrns = float(1)
            MSG = int(self.cmbMSG.get())
            PWR = float(self.cmbPWR.get())
            BTRY = int(self.cmbBTRY.get())
            if self.cmbRR.get() == "Low":
                RR = float(0.25)
            elif self.cmbRR.get() == "Medium":
                RR = float(0.5)
            else:
                RR = float(0.75)
            if bool(self.checkTimeBool.get()) == 1:
                T = 250
            else:
                T = int(self.sclT.get())
            IDS = bool(self.checkIDSBool.get())

            newActiveConfiguration = sis.SIS(Name, N, I, WSN, DEP, TRNS, CNTCT, SCAN, PTrns, IrPsu, IlPsu, IpPsu, MSG, PWR, BTRY, RR, T, IDS)
            self.updateGraphs(newActiveConfiguration)
            newActiveConfiguration.Timesteps = 12
            self.updateStatistics(newActiveConfiguration)
            self.activeConfiguration = newActiveConfiguration

    # Called to update the configuration statistics displayed on the left of the page
    def updateStatistics(self, activeConfiguration):
        self.currentSLoc.config(
            text="{:.0f} / {:.0f}".format(activeConfiguration.SLocFraction * activeConfiguration.S,
                                          activeConfiguration.S))
        self.currentSNhb.config(
            text="{:.0f} / {:.0f}".format(activeConfiguration.SNhbFraction * activeConfiguration.S,
                                          activeConfiguration.S))
        self.currentBr.config(text="{:.8f}".format(activeConfiguration.bR))
        self.currentBl.config(text="{:.8f}".format(activeConfiguration.bL))
        self.currentBp.config(text="{:.8f}".format(activeConfiguration.bP))
        self.currentDthB.config(text="{:.8f}".format(activeConfiguration.dthB))
        self.currentDthR.config(text="{:.8f}".format(activeConfiguration.dthR))
        self.currentDthL.config(text="{:.8f}".format(activeConfiguration.dthL))
        self.currentDthP.config(text="{:.8f}".format(activeConfiguration.dthP))

    # Called once when this interfaces is created + everytime this interfaces is opened to ensure all variable
    # control widgets are updated and correct
    def updateVariables(self, controller):
        self.activeConfiguration = controller.activeConfiguration
        self.activeConfigurationIndex = controller.activeConfigurationIndex

        self.entryName.delete(0, 'end')
        self.entryName.insert(END, self.activeConfiguration.Name[9:])
        self.cmbN.set(self.activeConfiguration.N)
        self.cmbBotCount.set(self.activeConfiguration.I)
        self.cmbWSN.set(self.activeConfiguration.WSNnumber)
        self.cmbDEP.set(self.activeConfiguration.deploymentArea)
        self.cmbTRNS.set(self.activeConfiguration.transmissionRange)
        self.cmbCNTCT.set(self.activeConfiguration.contactRate)
        self.sclSCAN.set(self.activeConfiguration.botScanningRate)
        if self.activeConfiguration.IrPsuccess == 0.00000000001:
            self.cmbIrPsu.set("0%")
        elif self.activeConfiguration.IrPsuccess == 0.005:
            self.cmbIrPsu.set("Low")
        elif self.activeConfiguration.IrPsuccess == 0.02:
            self.cmbIrPsu.set("Expected")
        elif self.activeConfiguration.IrPsuccess == 0.05:
            self.cmbIrPsu.set("High")
        elif self.activeConfiguration.IrPsuccess == 1:
            self.cmbIrPsu.set("100%")
        if self.activeConfiguration.IlPsuccess == 0.00000000001:
            self.cmbIlPsu.set("0%")
        elif self.activeConfiguration.IlPsuccess == 0.05:
            self.cmbIlPsu.set("Low")
        elif self.activeConfiguration.IlPsuccess == 0.1:
            self.cmbIlPsu.set("Expected")
        elif self.activeConfiguration.IlPsuccess == 0.25:
            self.cmbIlPsu.set("High")
        elif self.activeConfiguration.IlPsuccess == 1:
            self.cmbIlPsu.set("100%")
        if self.activeConfiguration.IpPsuccess == 0.00000000001:
            self.cmbIpPsu.set("0%")
        elif self.activeConfiguration.IpPsuccess == 0.45:
            self.cmbIpPsu.set("Low")
        elif self.activeConfiguration.IpPsuccess == 0.8:
            self.cmbIpPsu.set("Expected")
        elif self.activeConfiguration.IpPsuccess == 0.95:
            self.cmbIpPsu.set("High")
        elif self.activeConfiguration.IpPsuccess == 1:
            self.cmbIpPsu.set("100%")
        if self.activeConfiguration.Ptransmission == 0.00000000001:
            self.cmbPtrns.set("0")
        elif self.activeConfiguration.Ptransmission == 0.001:
            self.cmbPtrns.set("Low")
        elif self.activeConfiguration.Ptransmission == 0.01:
            self.cmbPtrns.set("Expected")
        elif self.activeConfiguration.Ptransmission == 0.03:
            self.cmbPtrns.set("High")
        elif self.activeConfiguration.Ptransmission == 1:
            self.cmbPtrns.set("100%")
        self.cmbMSG.set(self.activeConfiguration.meanMessageSize)
        self.cmbPWR.set(self.activeConfiguration.meanPower)
        self.cmbBTRY.set(self.activeConfiguration.totalBattery)
        if self.activeConfiguration.recoveryRate == 0.25:
            self.cmbRR.set("Low")
        elif self.activeConfiguration.recoveryRate == 0.5:
            self.cmbRR.set("Medium")
        else:
            self.cmbRR.set("High")
        self.sclT.set(self.activeConfiguration.Timesteps)
        if self.activeConfiguration.IDS:
            self.checkTime.select()
        else:
            self.checkTime.deselect()

    # Checks whether the configuration is saved or not before the user proceeds to another screen and looses
    # the current configuration
    def checkConfigurationSaved(self, controller, page):
        if self.activeConfiguration != controller.activeConfiguration:
            self.controller.popup("Warning", "Current Configuration Not Saved!")
        else:
            if page == 0:
                controller.display("SISControlInterface", "SISInspectInterface")
            else:
                controller.display("SISControlInterface", "HomeInterface")

    # Checks if the current configuration is valid by checking no population size reaches below zero
    def checkValid(self, newActiveConfig):
        S1, Ir1, Il1, Ip1 = newActiveConfig.runSimulation()
        populations = [S1, Ir1, Il1, Ip1]
        for P in populations:
            for value in P:
                if value < 0:
                    return False
        return True
