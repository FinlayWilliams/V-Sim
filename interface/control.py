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

        # Frame Top (Upper area for displaying and model option buttons)
        frame_top = tk.Frame(self, bg="#453354")
        # This button serves as a refresh button for the graphs (as doing it live is slow)
        btn_Refresh_Graph = tk.Button(frame_top, wraplength=40, width=5, text="Refresh Graphs", font=("Arial", 7), command=self.updateGraphs)
        # This button will reset the current configuration to that of the activemodel at the time of opening the window
        # and then resets the graphs too
        btn_Reset = tk.Button(frame_top, wraplength=40, width=5, text="Reset Model", font=("Arial", 7), command= lambda: [self.updateVariables(controller), self.updateGraphs()])
        # This button will open the inspect model page with the currently selected model
        btn_Inspect = tk.Button(frame_top, wraplength=40, width=5, text="Inspect model", font=("Arial", 7))
        # This button overwrites the current model "saving" it
        btn_Save = tk.Button(frame_top, wraplength=40, width=5, text="Save Model", font=("Arial", 7),
                             command=lambda: [self.updateModel(1),
                                              controller.overwriteModel(self.activeModelIndex, self.activeModel)])
        # This button take the current model configuration and adds a new model to the list
        btn_Save_New = tk.Button(frame_top, wraplength=40, width=5, text="Save New", font=("Arial", 7),
                                 command=lambda: [self.updateModel(1), controller.addModel(self.activeModel)])
        # This button takes the user to the home page
        btn_Return = tk.Button(frame_top, wraplength=40, width=5, text="Return Home", font=("Arial", 7),
                             command=lambda: controller.display("ControlInterface", "HomeInterface"))

        # Top buffer (visual improvement to lower the graphs)
        buffer_frame = tk.Frame(frame_top, bg="#654e78")
        # Canvas frame (to hold the graphs)
        canvas_frame = tk.Frame(frame_top, bg="#6e6e6e")

        # Frame Mid (For a single label)
        frame_mid = tk.Frame(self, bg="#6e6e6e")
        lbl_Options = tk.Label(frame_mid, text="Model Variables", bg="#6e6e6e", font=("Arial", 10), fg="white")

        # Frame Bottom (Lower area for the controls)
        frame_bot = tk.Frame(self, bg="#a8a8a8")

        # Creating labels and entry boxes for all initial variables
        lbl_Model_Name = tk.Label(frame_bot, text="Model Name:", bg="#a8a8a8", font=("Arial", 10))
        self.entry_Name = tk.Entry(frame_bot)

        lbl_N = tk.Label(frame_bot, text="Initial Node Population Size (N):")
        N_Options = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"]
        self.cmb_N = ttk.Combobox(frame_bot, values=N_Options, state="readonly")

        lbl_S = tk.Label(frame_bot, text="Initial S Size (% of N):")
        self.scl_S = tk.Scale(frame_bot, from_=0, to=1, resolution=0.01, orient="horizontal",
                              command=self.updateModel)

        lbl_IR = tk.Label(frame_bot, text="Initial IR Size (% of N):")
        self.scl_IR = tk.Scale(frame_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)

        lbl_IL = tk.Label(frame_bot, text="Initial IL Size (% of N):")
        self.scl_IL = tk.Scale(frame_bot, from_=0, to=1, resolution=0.001, orient="horizontal",
                               command=self.updateModel)

        lbl_IP = tk.Label(frame_bot, text="Initial IP Size (% of N):")
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
        BTRY_Options = ["432000", "864000", "1728000"]
        self.cmb_BTRY = ttk.Combobox(frame_bot, values=BTRY_Options, state="readonly")

        lbl_RR = tk.Label(frame_bot, text="Recovery rate:")
        self.scl_RR = tk.Scale(frame_bot, from_=0.250, to=1, digits=3, resolution=0.250, orient="horizontal",
                               command=self.updateModel)

        lbl_T = tk.Label(frame_bot, text="Days to Observe:")
        self.scl_T = tk.Scale(frame_bot, from_=1, to=900, resolution=1, orient="horizontal",
                              command=self.updateModel)

        # Placing all elements
        ## Frame Top Half
        buffer_frame.place(relheight=0.05, relwidth=1, x=58, y=0)
        frame_top.place(relheight=0.70, relwidth=1)
        btn_Refresh_Graph.place(x=10, y=13)
        btn_Reset.place(x=10, y=64)
        btn_Inspect.place(x=10, y=115)
        btn_Save.place(x=10, y=166)
        btn_Save_New.place(x=10, y=217)
        btn_Return.place(x=10, y=560)
        canvas_frame.place(relheight=0.95, relwidth=0.963, x=58, y=30)
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
        self.ax = [figure.add_subplot(2, 2, x + 1, facecolor="#453354") for x in range(4)]

        for x in range(4):
            self.ax[x].ticklabel_format(style="plain")

        figure.tight_layout()

    # Method to update the onscreen graphs to whatever the current model configuration is
    def updateGraphs(self):
        S1, Ir1, Il1, Ip1 = self.activeModel.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.activeModel.Timesteps, 101)

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

            self.activeModel = sis.SIS(Name, N, S, IR, IL, IP, WSN, DEP, TRNS, CNTCT, SCAN, PTrns, IrPsu, IlPsu, IpPsu,
                                       MSG, PWR, BTRY, RR, T)
            # Good to have it here but it makes it really slow so it is for now, #### out and the R button is in place
            #self.updateGraphs()

    # This method is called once when this interface is created and is called everytime this interface
    # is opened to ensure all variables are updated and correct
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
