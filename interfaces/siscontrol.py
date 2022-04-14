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
        # Button: Resets models config and refreshes graphs
        btnReset = tk.Button(frameTop, wraplength=40, width=5, text="Reset Config", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: [self.updateVariables(controller), self.updateGraphs()])
        # Button: overwrites the current models "saving" it
        btnSave = tk.Button(frameTop, wraplength=40, width=5, text="Save Config", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                            command=lambda: [self.updateConfiguration(1),
                                             controller.overwriteConfiguration(self.activeConfigurationIndex, self.activeConfiguration),
                                             controller.setActiveConfiguration(self.activeConfigurationIndex)])
        # Button: add this models configuration to the controller list
        btnSaveNew = tk.Button(frameTop, wraplength=40, width=5, text="Save New", font=("Arial", 7), bg="#6e6e6e", relief="ridge", fg="white",
                               command=lambda: [self.updateConfiguration(1), controller.addConfiguration(self.activeConfiguration),
                                                controller.setActiveConfiguration(len(controller.configurations) - 1)])
        # Button: opens the inspect models page with the currently selected models
        btnInspect = tk.Button(frameTop, wraplength=40, width=5, text="Inspect Config", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                               command=lambda: self.checkConfigurationSaved(controller, 1))
        # Button: takes the user to the home page
        btnReturn = tk.Button(frameTop, wraplength=40, width=5, text="Return Home", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                             command=lambda: controller.display("SISControlInterface", "HomeInterface"))

        # This frame holds the graphs
        canvasFrame = tk.Frame(frameTop, bg="#654e78")
        # Frame for the legend to sit in + legend labels
        lblLegendTitle = tk.Label(frameTop, bg="#453354", width=25, pady=4, text="Legend :", font=("Calibri", 14, "bold"), fg="white")
        lblLegend1 = tk.Label(frameTop, bg="#2ca02c", width=25, pady=4, text="(S) Susceptible", font=("Arial", 12), fg="white")
        lblLegend2 = tk.Label(frameTop, bg="#9467bd", width=25, pady=4, text="(IR) Random-Scanning", font=("Arial", 12), fg="white")
        lblLegend3 = tk.Label(frameTop, bg="#1f77b4", width=25, pady=4, text="(IL) Local Scanning", font=("Arial", 12), fg="white")
        lblLegend4 = tk.Label(frameTop, bg="#17becf", width=25, pady=4, text="(IP) Peer-to-Peer", font=("Arial", 12), fg="white")
        lblLegend5 = tk.Label(frameTop, bg="#d62728", width=25, pady=4, text="(I) Infection Types Grouped", font=("Arial", 12), fg="white")

        # Separates graphs from the controls
        frameMid = tk.Frame(self, bg="#6e6e6e")
        lblOptions = tk.Label(frameMid, text="Model Variable Controls", bg="#6e6e6e", font=("Arial", 10), fg="white")

        # Lower area for the controls
        frameBot = tk.Frame(self, bg="#a8a8a8")
        # All labels and widgets for inputting variables
        lblConfigurationName = tk.Label(frameBot, text="Configuration Name:", bg="#a8a8a8", font=("Arial", 10))
        self.entryName = tk.Entry(frameBot)
        lblN = tk.Label(frameBot, text="Initial Node Population Size (N):")
        NOptions = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"]
        self.cmbN = ttk.Combobox(frameBot, values=NOptions, state="readonly")
        lblS = tk.Label(frameBot, text="Initial S Size (% of N):")
        self.sclS = tk.Scale(frameBot, from_=0, to=100, resolution=0.1, orient="horizontal")
        lblI = tk.Label(frameBot, text="Initial I Size (% of N):")
        self.lblIMatch = tk.Label(frameBot, bg="white", bd=3)
        lblWSN = tk.Label(frameBot, text="Wireless Sensor Network Count:")
        WSNOptions = ["1", "5", "10", "20", "50"]
        self.cmbWSN = ttk.Combobox(frameBot, values=WSNOptions, state="readonly")
        lblDEP = tk.Label(frameBot, text="Node Deployment Area: (m x m)")
        DEPOptions = ["25", "50", "100", "150"]
        self.cmbDEP = ttk.Combobox(frameBot, values=DEPOptions, state="readonly")
        lblTRNS = tk.Label(frameBot, text="Node Transmission Range (m):")
        TRNSOptions = ["1", "5", "10", "15"]
        self.cmbTRNS = ttk.Combobox(frameBot, values=TRNSOptions, state="readonly")
        lblCNTCT = tk.Label(frameBot, text="S Node Contact Rate:")
        CNTCTOptions = ["1", "5", "10", "20", "50", "75", "100", "250"]
        self.cmbCNTCT = ttk.Combobox(frameBot, values=CNTCTOptions, state="readonly")
        lblSCAN = tk.Label(frameBot, text="Botnet Scanning Rate (/sec):")
        self.sclSCAN = tk.Scale(frameBot, from_=1, to=250, resolution=1, orient="horizontal")
        lblPtrns = tk.Label(frameBot, text="PTransmission Rate:")
        self.sclPtrns = tk.Scale(frameBot, from_=0.0001, to=1, resolution=0.0001, orient="horizontal")
        lblIrPsu = tk.Label(frameBot, text="IR PSuccess Rate:")
        self.sclIrPsu = tk.Scale(frameBot, from_=0.00001, to=1, resolution=0.00001, orient="horizontal")
        lblIlPsu = tk.Label(frameBot, text="IL PSuccess Rate:")
        self.sclIlPsu = tk.Scale(frameBot, from_=0.00001, to=1, resolution=0.00001, orient="horizontal")
        lblIpPsu = tk.Label(frameBot, text="IP PSuccess Rate:")
        self.sclIpPsu = tk.Scale(frameBot, from_=0.00001, to=1, resolution=0.00001, orient="horizontal")
        lblMSG = tk.Label(frameBot, text="Mean Message Size (Bytes):")
        MSGOptions = ["10", "20", "50", "100"]
        self.cmbMSG = ttk.Combobox(frameBot, values=MSGOptions, state="readonly")
        lblPWR = tk.Label(frameBot, text="Mean Power to Send Message (mA):")
        PWROptions = ["0.25", "0.5", "0.75", "1", "1.25"]
        self.cmbPWR = ttk.Combobox(frameBot, values=PWROptions, state="readonly")
        lblBTRY = tk.Label(frameBot, text="Total Node Battery Capacity (mAs):")
        BTRYOptions = ["216000", "432000", "864000", "1728000", "3456000"]
        self.cmbBTRY = ttk.Combobox(frameBot, values=BTRYOptions, state="readonly")
        lblRR = tk.Label(frameBot, text="Recovery rate:")
        self.sclRR = tk.Scale(frameBot, from_=0.250, to=1, digits=3, resolution=0.250, orient="horizontal")
        lblT = tk.Label(frameBot, text="Days to Observe:")
        self.sclT = tk.Scale(frameBot, from_=1, to=2700, resolution=1, orient="horizontal")

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
        btnReset.place(x=10, y=458)
        btnSave.place(x=10, y=509)
        btnSaveNew.place(x=10, y=560)
        canvasFrame.place(relheight=1, relwidth=0.73, x=58)
        lblLegendTitle.place(x=1229, y=194)
        lblLegend1.place(x=1243, y=227)
        lblLegend2.place(x=1243, y=260)
        lblLegend3.place(x=1243, y=293)
        lblLegend4.place(x=1243, y=326)
        lblLegend5.place(x=1243, y=359)
        ## Frame Mid
        frameMid.place(y=605, relheight=0.05, relwidth=1)
        lblOptions.pack()
        ## Frame Bottom Half
        frameBot.place(y=628, relheight=0.30, relwidth=1)
        # 1st Block
        lblConfigurationName.grid(row=0, column=0, padx=30, sticky="w")
        self.entryName.grid(row=1, column=0, padx=30, sticky="nw")
        # 2nd Block
        lblN.grid(row=0, column=1, padx=(10, 5), pady=(7, 0), sticky="e")
        self.cmbN.grid(row=0, column=2, padx=5, pady=(7, 0))
        self.cmbN.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblS.grid(row=1, column=1, padx=(10, 5), pady=5, sticky="e")
        self.sclS.grid(row=1, column=2, padx=5, sticky="ew")
        self.sclS.bind("<ButtonRelease-1>", self.updateConfiguration)
        lblI.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="e")
        self.lblIMatch.grid(row=2, column=2, padx=5, sticky="ew")
        # 3rd Block
        lblWSN.grid(row=0, column=3, padx=5, pady=(7, 0), sticky="e")
        self.cmbWSN.grid(row=0, column=4, padx=5, pady=(7, 0))
        self.cmbWSN.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblDEP.grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.cmbDEP.grid(row=1, column=4, padx=5, pady=5)
        self.cmbDEP.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblTRNS.grid(row=2, column=3, padx=5, pady=5, sticky="e")
        self.cmbTRNS.grid(row=2, column=4, padx=5, pady=5)
        self.cmbTRNS.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblCNTCT.grid(row=3, column=3, padx=5, pady=5, sticky="e")
        self.cmbCNTCT.grid(row=3, column=4, padx=5, pady=5, sticky="ew")
        self.cmbCNTCT.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblSCAN.grid(row=4, column=3, padx=5, pady=5, sticky="e")
        self.sclSCAN.grid(row=4, column=4, padx=5, sticky="ew")
        self.sclSCAN.bind("<ButtonRelease-1>", self.updateConfiguration)
        # 4th Block
        lblPtrns.grid(row=0, column=5, padx=5, pady=(7, 0), sticky="e")
        self.sclPtrns.grid(row=0, column=6, padx=5, pady=(7, 0))
        self.sclPtrns.bind("<ButtonRelease-1>", self.updateConfiguration)
        lblIrPsu.grid(row=1, column=5, padx=5, pady=5, sticky="e")
        self.sclIrPsu.grid(row=1, column=6, padx=5, sticky="ew")
        self.sclIrPsu.bind("<ButtonRelease-1>", self.updateConfiguration)
        lblIlPsu.grid(row=2, column=5, padx=5, pady=5, sticky="e")
        self.sclIlPsu.grid(row=2, column=6, padx=5, sticky="ew")
        self.sclIlPsu.bind("<ButtonRelease-1>", self.updateConfiguration)
        lblIpPsu.grid(row=3, column=5, padx=5, pady=5, sticky="e")
        self.sclIpPsu.grid(row=3, column=6, padx=5, sticky="ew")
        self.sclIpPsu.bind("<ButtonRelease-1>", self.updateConfiguration)
        # 5th Block
        lblMSG.grid(row=0, column=7, padx=5, pady=(7, 0), sticky="e")
        self.cmbMSG.grid(row=0, column=8, padx=5, pady=(7, 0))
        self.cmbMSG.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblPWR.grid(row=1, column=7, padx=5, pady=5, sticky="e")
        self.cmbPWR.grid(row=1, column=8, padx=5, pady=5)
        self.cmbPWR.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblBTRY.grid(row=2, column=7, padx=5, pady=5, sticky="e")
        self.cmbBTRY.grid(row=2, column=8, padx=5, pady=5)
        self.cmbBTRY.bind("<<ComboboxSelected>>", self.updateConfiguration)
        lblRR.grid(row=3, column=7, padx=5, pady=5, sticky="e")
        self.sclRR.grid(row=3, column=8, padx=5, sticky="ew")
        self.sclRR.bind("<ButtonRelease-1>", self.updateConfiguration)
        lblT.grid(row=4, column=7, padx=5, pady=5, sticky="e")
        self.sclT.grid(row=4, column=8, padx=5, sticky="ew")
        self.sclT.bind("<ButtonRelease-1>", self.updateConfiguration)
        # Calling the method to align the variables and populate all fields
        self.updateVariables(controller)

    # Method to update the onscreen graphs to whatever the current models configuration is
    def updateGraphs(self):
        S1, Ir1, Il1, Ip1 = self.activeConfiguration.runSimulation()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.activeConfiguration.Timesteps, 60)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(2)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
        self.ax[0].plot(T1, Il1, "#1f77b4", label="Local-Scanning Infected")
        self.ax[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
        self.ax[0].set_xlabel("Timesteps (Days)")
        self.ax[0].set_ylabel("Node Count")
        self.ax[0].set_title("Node Population Sizes Over Time - Individual Infection Types - S, IR, IL, IP")

        # Plotting the third graph
        self.ax[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.ax[1].plot(T1, I1, '#d62728', label="All Infected")
        self.ax[1].set_xlabel("Timesteps (Days)")
        self.ax[1].set_ylabel("Node Count")
        self.ax[1].set_title("Node Population Sizes Over Time - Grouped Infection Types - S, I = (IR + IL + IP)")

        self.canvas.draw()

    # Called when a value option is changed, to automatically update the active models parameters
    def updateConfiguration(self, Stub):
        if len(self.entryName.get()) == 0:
            self.controller.popup("Invalid Save", "Please Enter a Name for the Configuration!")
        if len(self.entryName.get()) > 24:
            self.controller.popup("Invalid Save", "Please Enter a Shorter Name for the Configuration!")
        else:
            Name = str("IoT-SIS: " + self.entryName.get())
            N = int(self.cmbN.get())
            S = float(self.sclS.get() / 100)
            I = float((100 - self.sclS.get()) / 100)
            WSN = int(self.cmbWSN.get())
            DEP = int(self.cmbDEP.get())
            TRNS = int(self.cmbTRNS.get())
            CNTCT = int(self.cmbCNTCT.get())
            SCAN = int(self.sclSCAN.get())
            PTrns = float(self.sclPtrns.get())
            IrPsu = float(self.sclIrPsu.get())
            IlPsu = float(self.sclIlPsu.get())
            IpPsu = float(self.sclIpPsu.get())
            MSG = int(self.cmbMSG.get())
            PWR = float(self.cmbPWR.get())
            BTRY = int(self.cmbBTRY.get())
            RR = float(self.sclRR.get())
            T = int(self.sclT.get())

            newActiveModel = sis.SIS(Name, N, S, I, WSN, DEP, TRNS, CNTCT, SCAN, PTrns, IrPsu, IlPsu, IpPsu,
                                       MSG, PWR, BTRY, RR, T)

            self.lblIMatch.config(text="{:.0f}".format(I*100))

            # if not self.checkValid(newActiveModel):
            #     self.controller.popup("Invalid Model Configuration", "Population Sizes will reach negative values!")
            # else:
            #     self.activeModel = newActiveModel
            #     self.updateGraphs()

            # delete what is below this and uncomment what is above
            print("=======================================================")

            # print("Il Death Rate: {}".format(newActiveModel.dthL))
            # print("Il Infection Rate: {}".format(newActiveModel.bL))
            # print("Il Contact Rate: {}".format(newActiveModel.IlContactRate))
            # print("")
            # print("Ip Death Rate: {}".format(newActiveModel.dthP))
            # print("Ip Infection Rate: {}".format(newActiveModel.bP))
            # print("Ip Contact Rate: {}".format(newActiveModel.IpContactRate))
            print("PowerMessage: {}".format(newActiveModel.powerMessage))
            print("")
            print("RandomPowerTime: {}".format(newActiveModel.randomPowerTime))
            print("")
            print("S Contact Rate: {}".format(newActiveModel.contactRate))
            print("S Lifespan: {}".format(newActiveModel.regularLifespan))
            print("S Death Rate: {}".format(newActiveModel.dthB))
            print("")
            print("Ir Contact Rate: {}".format(newActiveModel.IrContactRate))
            print("Ir ILifespan: {}".format(newActiveModel.randomLifespan))
            print("Ir Death Rate: {}".format(newActiveModel.dthR))
            print("Ir Infection Rate: {}".format(newActiveModel.bR))
            print("")

            self.activeConfiguration = newActiveModel
            self.updateGraphs()

    # Called once when this interfaces is created + everytime this interfaces is opened to ensure all variables
    # are updated and correct
    def updateVariables(self, controller):
        self.activeConfiguration = controller.activeConfiguration
        self.activeConfigurationIndex = controller.activeConfigurationIndex

        self.cmbN.set(self.activeConfiguration.N)
        self.sclS.set(self.activeConfiguration.percentS * 100)
        self.lblIMatch.config(text="{:.0f}".format(self.activeConfiguration.percentI * 100))
        self.cmbWSN.set(self.activeConfiguration.WSNnumber)
        self.cmbDEP.set(self.activeConfiguration.deploymentArea)
        self.cmbTRNS.set(self.activeConfiguration.transmissionRange)
        self.cmbCNTCT.set(self.activeConfiguration.contactRate)
        self.sclSCAN.set(self.activeConfiguration.botScanningRate)
        self.sclPtrns.set(self.activeConfiguration.botPtransmission)
        self.sclIrPsu.set(self.activeConfiguration.IrPsuccess)
        self.sclIlPsu.set(self.activeConfiguration.IlPsuccess)
        self.sclIpPsu.set(self.activeConfiguration.IpPsuccess)
        self.entryName.delete(0, 'end')
        self.entryName.insert(END, self.activeConfiguration.Name[9:])
        self.cmbMSG.set(self.activeConfiguration.meanMessageSize)
        self.cmbPWR.set(self.activeConfiguration.meanPower)
        self.cmbBTRY.set(self.activeConfiguration.totalBattery)
        self.sclRR.set(self.activeConfiguration.recoveryRate)
        self.sclT.set(self.activeConfiguration.Timesteps)

    # Checks whether the models is saved or not before the user proceeds to the inspect screen and looses
    # the current configuration
    def checkConfigurationSaved(self, controller, stub):
        if self.activeConfiguration != controller.activeConfiguration:
            self.controller.popup("Warning", "Current models configuration not saved")
        else:
            controller.display("SISControlInterface", "SISInspectInterface")

    # Checks if the current configuration is valid by checking no population size dips below zero
    def checkValid(self, newActiveConfig):
        S1, Ir1, Il1, Ip1 = newActiveConfig.runSimulation()
        populations = [S1, Ir1, Il1, Ip1]
        for P in populations:
            for value in P:
                if value < 0:
                    return False
        return True
