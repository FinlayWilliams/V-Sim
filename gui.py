import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import ttk

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import model

class ModelInterface:
    # Constructor
    def __init__(self, model):
        self.activeModel = model
        self.modelList = []
        self.initialiseInterfaceObjects()

    # This method initialises the base window itself
    def initialiseInterfaceObjects(self):
        # Base Interface Settings
        self.base = tk.Tk()
        self.base.title("IoT-SIS Model Simulation")
        screen_width = self.base.winfo_screenwidth()
        screen_height = self.base.winfo_screenheight()
        center_x = int(screen_width / 2 - 1536 / 2)
        center_y = int(screen_height / 2 - 864 / 2)
        self.base.geometry(f"1536x864+{center_x}+{center_y}")
        self.base.resizable(0, 0)
        self.base.configure(background="#453354")
        self.base.attributes("-transparentcolor", "grey")
        self.base.iconbitmap('./assets/virus_icon.ico')

    # This method places and displays the model-control page elements
    def displayModelControls(self):
        ### Frame 1 ( first screen )
        self.frame_1 = tk.Frame(self.base, bg="#453354")
        self.frame_1.place(relheight=1, relwidth=1)

        # Frame 1 Top Widgets
        self.frame_1_top = tk.Frame(self.frame_1, bg="red")

        # Frame 1 Bottom Widgets
        self.frame_1_bot = tk.Frame(self.frame_1, bg="green")
        # Creating labels and entry boxes for all initial variables
        self.lbl_N = tk.Label(self.frame_1_bot, text="Initial Node Population Size (N):");
        self.N_Options = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"];
        self.cmb_N = ttk.Combobox(self.frame_1_bot, values=self.N_Options, state="readonly")

        self.lbl_S = tk.Label(self.frame_1_bot, text="Initial S Size (% of N):");
        self.scl_S = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)

        self.lbl_IR = tk.Label(self.frame_1_bot, text="Initial IR Size (% of N):");
        self.scl_IR = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.001, orient="horizontal", command=self.updateModel)

        self.lbl_IL = tk.Label(self.frame_1_bot, text="Initial IL Size (% of N):");
        self.scl_IL = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.001, orient="horizontal", command=self.updateModel)

        self.lbl_IP = tk.Label(self.frame_1_bot, text="Initial IP Size (% of N):");
        self.scl_IP = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.001, orient="horizontal", command=self.updateModel)

        self.lbl_WSN = tk.Label(self.frame_1_bot, text="Wireless Sensor Network Count:");
        self.WSN_Options = ["1", "5", "10", "20", "50"];
        self.cmb_WSN = ttk.Combobox(self.frame_1_bot, values=self.WSN_Options, state="readonly")

        self.lbl_DEP = tk.Label(self.frame_1_bot, text="Node Deployment Area: (m x m)");
        self.DEP_Options = ["25", "50", "100", "150"];
        self.cmb_DEP = ttk.Combobox(self.frame_1_bot, values=self.DEP_Options, state="readonly")

        self.lbl_TRNS = tk.Label(self.frame_1_bot, text="Node Transmission Range (m):");
        self.TRNS_Options = ["1", "5", "10", "15"];
        self.cmb_TRNS = ttk.Combobox(self.frame_1_bot, values=self.TRNS_Options, state="readonly")

        self.lbl_CNTCT = tk.Label(self.frame_1_bot, text="S Node Contact Rate:");
        self.CNTCT_Options = ["1", "5", "10", "20", "50", "75", "100", "250"];
        self.cmb_CNTCT = ttk.Combobox(self.frame_1_bot, values=self.CNTCT_Options, state="readonly")

        self.lbl_SCAN = tk.Label(self.frame_1_bot, text="Botnet Scanning Rate (/sec):");
        self.scl_SCAN = tk.Scale(self.frame_1_bot, from_=0, to=250, resolution=1, orient="horizontal",command=self.updateModel)

        self.lbl_Ptrns = tk.Label(self.frame_1_bot, text="PTransmission Rate:");
        self.scl_Ptrns = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)

        self.lbl_IrPsu = tk.Label(self.frame_1_bot, text="IR PSuccess Rate:");
        self.scl_IrPsu = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.00001, orient="horizontal", command=self.updateModel)

        self.lbl_IlPsu = tk.Label(self.frame_1_bot, text="IL PSuccess Rate:");
        self.scl_IlPsu = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)

        self.lbl_IpPsu = tk.Label(self.frame_1_bot, text="IP PSuccess Rate:");
        self.scl_IpPsu = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)

        self.lbl_MSG = tk.Label(self.frame_1_bot, text="Mean Message Size (Bytes):");
        self.MSG_Options = ["10", "20", "50", "100"];
        self.cmb_MSG = ttk.Combobox(self.frame_1_bot, values=self.MSG_Options, state="readonly")

        self.lbl_PWR = tk.Label(self.frame_1_bot, text="Mean Power to Send Message (mA):");
        self.PWR_Options = ["0.25", "0.5", "0.75", "1", "1.25"];
        self.cmb_PWR = ttk.Combobox(self.frame_1_bot, values=self.PWR_Options, state="readonly")

        self.lbl_BTRY = tk.Label(self.frame_1_bot, text="Total Node Battery Capacity (mAs):");
        self.BTRY_Options = ["432000", "864000", "1728000"];
        self.cmb_BTRY = ttk.Combobox(self.frame_1_bot, values=self.BTRY_Options, state="readonly")

        self.lbl_RR = tk.Label(self.frame_1_bot, text="Recovery rate:");
        self.scl_RR = tk.Scale(self.frame_1_bot, from_=0, to=1, digits=3, resolution=0.250, orient="horizontal", command=self.updateModel)

        self.lbl_T = tk.Label(self.frame_1_bot, text="Days to Observe:");
        self.scl_T = tk.Scale(self.frame_1_bot, from_=0, to=900, resolution=1, orient="horizontal", command=self.updateModel)

        self.btn_RUN = tk.Button(self.frame_1_bot, text="Run Model HERE 4 NOW", command=self.displayGraphs)
        self.btn_INSP = tk.Button(self.frame_1_bot, text="Inspect Model")
        self.btn_SAVE = tk.Button(self.frame_1_bot, text="Save Configuration")
        self.btn_NEW = tk.Button(self.frame_1_bot, text="New Simulation")
        self.btn_CMPR = tk.Button(self.frame_1_bot, text="Compare Configurations")

        # Placing all elements
        ## Frame 1 Top Half
        self.frame_1_top.place(relheight=0.75, relwidth=1)
        ## Frame 1 Bottom Half
        self.frame_1_bot.place(y=648, relheight=0.27, relwidth=1)
        # 1st Block
        self.lbl_N.grid(row=0, column=0, padx=(10, 5), pady=(7, 0), sticky="e"); self.cmb_N.grid(row=0, column=1, padx=5, pady=(7, 0)); self.cmb_N.set("10000");
        self.cmb_N.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_S.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_S.grid(row=1, column=1, padx=5, sticky="ew"); self.scl_S.set("0.99")
        self.lbl_IR.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_IR.grid(row=2, column=1, padx=5, sticky="ew"); self.scl_IR.set("0.003")
        self.lbl_IL.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_IL.grid(row=3, column=1, padx=5, sticky="ew"); self.scl_IL.set("0.003")
        self.lbl_IP.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_IP.grid(row=4, column=1, padx=5, sticky="ew"); self.scl_IP.set("0.004")
        # 2nd Block
        self.lbl_WSN.grid(row=0, column=2, padx=5, pady=(7, 0), sticky="e"); self.cmb_WSN.grid(row=0, column=3, padx=5, pady=(7, 0)); self.cmb_WSN.set("10");
        self.cmb_WSN.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_DEP.grid(row=1, column=2, padx=5, pady=5, sticky="e"); self.cmb_DEP.grid(row=1, column=3, padx=5, pady=5); self.cmb_DEP.set("50");
        self.cmb_DEP.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_TRNS.grid(row=2, column=2, padx=5, pady=5, sticky="e"); self.cmb_TRNS.grid(row=2, column=3, padx=5, pady=5); self.cmb_TRNS.set("10");
        self.cmb_TRNS.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_CNTCT.grid(row=3, column=2, padx=5, pady=5, sticky="e"); self.cmb_CNTCT.grid(row=3, column=3, padx=5, pady=5, sticky="ew"); self.cmb_CNTCT.set("1");
        self.cmb_CNTCT.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_SCAN.grid(row=4, column=2, padx=5, pady=5, sticky="e"); self.scl_SCAN.grid(row=4, column=3, padx=5, sticky="ew"); self.scl_SCAN.set("27")
        # 3rd Block
        self.lbl_Ptrns.grid(row=0, column=4, padx=5, pady=(7, 0), sticky="e"); self.scl_Ptrns.grid(row=0, column=5, padx=5, pady=(7, 0)); self.scl_Ptrns.set("0.3")
        self.lbl_IrPsu.grid(row=1, column=4, padx=5, pady=5, sticky="e"); self.scl_IrPsu.grid(row=1, column=5, padx=5, sticky="ew"); self.scl_IrPsu.set("0.00002")
        self.lbl_IlPsu.grid(row=2, column=4, padx=5, pady=5, sticky="e"); self.scl_IlPsu.grid(row=2, column=5, padx=5, sticky="ew"); self.scl_IlPsu.set("0.06")
        self.lbl_IpPsu.grid(row=3, column=4, padx=5, pady=5, sticky="e"); self.scl_IpPsu.grid(row=3, column=5, padx=5, sticky="ew"); self.scl_IpPsu.set("0.09")
        # 4th Block
        self.lbl_MSG.grid(row=0, column=6, padx=5, pady=(7, 0), sticky="e"); self.cmb_MSG.grid(row=0, column=7, padx=5, pady=(7, 0)); self.cmb_MSG.set("50");
        self.cmb_MSG.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_PWR.grid(row=1, column=6, padx=5, pady=5, sticky="e"); self.cmb_PWR.grid(row=1, column=7, padx=5, pady=5);  self.cmb_PWR.set("0.75");
        self.cmb_PWR.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_BTRY.grid(row=2, column=6, padx=5, pady=5, sticky="e"); self.cmb_BTRY.grid(row=2, column=7, padx=5, pady=5); self.cmb_BTRY.set("864000");
        self.cmb_BTRY.bind("<<ComboboxSelected>>", self.updateModel)
        self.lbl_RR.grid(row=3, column=6, padx=5, pady=5, sticky="e"); self.scl_RR.grid(row=3, column=7, padx=5, sticky="ew"); self.scl_RR.set("0.5")
        self.lbl_T.grid(row=4, column=6, padx=5, pady=5, sticky="e"); self.scl_T.grid(row=4, column=7, padx=5, sticky="ew"); self.scl_T.set("100")
        # 5th Block
        self.btn_RUN.grid(row=0, column=8, padx=(60, 5), pady=(7, 4), sticky="ew")
        self.btn_INSP.grid(row=1, column=8, padx=(60, 5), pady=4, sticky="ew")
        self.btn_SAVE.grid(row=2, column=8, padx=(60, 5), pady=4, sticky="ew")
        self.btn_NEW.grid(row=3, column=8, padx=(60, 5), pady=4, sticky="ew")
        self.btn_CMPR.grid(row=4, column=8, padx=(60, 5), pady=4, sticky="ew")

        # Getting the graphs out
        self.updateModel(1)
        #self.displayGraphs()

        # Runnit
        self.base.mainloop()

    # This method places all graph elements displaying the model
    def displayGraphs(self):
        S1, Ir1, Il1, Ip1 = self.activeModel.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = self.activeModel.Timesteps

        figure, axes = plt.subplots(nrows=2, ncols=2)

        axes[0, 0].plot(T1, S1, 'g', label="Susceptible")
        axes[0, 0].plot(T1, Ir1, 'y', label="Random-Scanning Infected")
        axes[0, 0].plot(T1, Il1, 'b', label="Local Scanning Infected")
        axes[0, 0].plot(T1, Ip1, 'c', label="Peer-to-Peer Infected")
        axes[0, 0].set_title("Title")
        axes[0, 0].ticklabel_format(style="plain")

        pop = [S1[len(S1)-1], Ir1[len(Ir1)-1], Il1[len(Il1)-1], Ip1[len(Ip1)-1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible", "Random-Scanning Infected", "Local Scanning Infected", "Peer-to-Peer Infected"]
        axes[0, 1].pie(pop, explode=explode, labels=labels)

        axes[1, 0].plot(T1, Ip1)

        axes[1, 1].plot(T1, S1, 'g', label="Susceptible")
        axes[1, 1].plot(T1, Ir1, 'y', label="Random-Scanning Infected")
        axes[1, 1].plot(T1, Il1, 'b', label="Local Scanning Infected")
        axes[1, 1].plot(T1, Ip1, 'c', label="Peer-to-Peer Infected")
        axes[1, 1].legend(loc="best")

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self.frame_1_top)  # A tk.DrawingArea.
        #canvas.get_tk_widget().delete(self.figure)

        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # toolbar = NavigationToolbar2Tk(canvas, self.frame_1_top)
        # toolbar.update()
        i = 0

    # This method is called whenever a value option is changed, to automatically update the model
    def updateModel(self, Stub):
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

        self.activeModel = model.Model(N, S, IR, IL, IP, WSN, DEP, TRNS, CNTCT, SCAN, PTrns, IrPsu, IlPsu, IpPsu, MSG, PWR, BTRY, RR, T)
        OtherStub = Stub

        print("Hey")
