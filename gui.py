import tkinter as tk
from tkinter import *
from tkinter import ttk
import model

class ModelInterface:
    def __init__(self, model):
        self.activeModel = model
        self.modelList = []

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

        self.frame_1 = tk.Frame(self.base, bg="#453354")
        self.frame_1_top = tk.Frame(self.frame_1, bg="red")

        # Frame 1 Bottom Settings
        self.frame_1_bot = tk.Frame(self.frame_1, bg="green")
        # Creating labels and entry boxes for all initial variables
        self.lbl_N = tk.Label(self.frame_1_bot, text="Initial Node Population Size (N):"); self.N_Options = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"]; self.cmb_N = ttk.Combobox(self.frame_1_bot, values=self.N_Options, state="readonly")
        self.lbl_S = tk.Label(self.frame_1_bot, text="Initial S Size (% of N):"); self.scl_S = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_IR = tk.Label(self.frame_1_bot, text="Initial IR Size (% of N):"); self.scl_IR = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_IL = tk.Label(self.frame_1_bot, text="Initial IL Size (% of N):"); self.scl_IL = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_IP = tk.Label(self.frame_1_bot, text="Initial IP Size (% of N):"); self.scl_IP = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_WSN = tk.Label(self.frame_1_bot, text="Wireless Sensor Network Count:"); self.WSN_Options = ["1", "5", "10", "20", "50"]; self.cmb_WSN = ttk.Combobox(self.frame_1_bot, values=self.WSN_Options, state="readonly")
        self.lbl_DEP = tk.Label(self.frame_1_bot, text="Node Deployment Area: (m x m)"); self.DEP_Options = ["25", "50", "100", "150"]; self.cmb_DEP = ttk.Combobox(self.frame_1_bot, values=self.DEP_Options, state="readonly")
        self.lbl_TRNS = tk.Label(self.frame_1_bot, text="Node Transmission Range (m):"); self.TRNS_Options = ["1", "5", "10", "15"]; self.cmb_TRNS = ttk.Combobox(self.frame_1_bot, values=self.TRNS_Options, state="readonly")
        self.lbl_CNTCT = tk.Label(self.frame_1_bot, text="S Node Contact Rate:"); self.CNTCT_Options = ["1", "5", "10", "20", "50", "75", "100", "250"]; self.cmb_CNTCT = ttk.Combobox(self.frame_1_bot, values=self.CNTCT_Options, state="readonly")
        self.lbl_SCAN = tk.Label(self.frame_1_bot, text="Botnet Scanning Rate (/sec):"); self.scl_SCAN = tk.Scale(self.frame_1_bot, from_=0, to=250, resolution=1, orient="horizontal", command=self.updateModel)
        self.lbl_Ptrns = tk.Label(self.frame_1_bot, text="PTransmission Rate:"); self.scl_Ptrns = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_IrPsu = tk.Label(self.frame_1_bot, text="IR PSuccess Rate:"); self.scl_IrPsu = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_IlPsu = tk.Label(self.frame_1_bot, text="IL PSuccess Rate:"); self.scl_IlPsu = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_IpPsu = tk.Label(self.frame_1_bot, text="IP PSuccess Rate:"); self.scl_IpPsu = tk.Scale(self.frame_1_bot, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.updateModel)
        self.lbl_MSG = tk.Label(self.frame_1_bot, text="Mean Message Size (Bytes):"); self.entry_MSG = tk.Entry(self.frame_1_bot)
        self.lbl_PWR = tk.Label(self.frame_1_bot, text="Mean Power to Send Message (mA):"); self.entry_PWR = tk.Entry(self.frame_1_bot)
        self.lbl_BTRY = tk.Label(self.frame_1_bot, text="Total Node Battery Capacity (mAs):"); self.entry_BTRY = tk.Entry(self.frame_1_bot)
        self.lbl_RR = tk.Label(self.frame_1_bot, text="Recovery rate:"); self.scl_RR = tk.Scale(self.frame_1_bot, from_=0, to=1, digits=3, resolution=0.250, orient="horizontal", command=self.updateModel)
        self.lbl_T = tk.Label(self.frame_1_bot, text="Days to Observe:"); self.scl_T = tk.Scale(self.frame_1_bot, from_=0, to=900, resolution=1, orient="horizontal", command=self.updateModel)
        self.btn_RUN = tk.Button(self.frame_1_bot, text="Run Model HERE 4 NOW")
        self.btn_INSP = tk.Button(self.frame_1_bot, text="Inspect Model")
        self.btn_SAVE = tk.Button(self.frame_1_bot, text="Save Configuration")
        self.btn_NEW = tk.Button(self.frame_1_bot, text="New Simulation")
        self.btn_CMPR = tk.Button(self.frame_1_bot, text="Compare Configurations")

    def setActiveModel(self, model):
        self.activeModel = model

    def getActiveModel(self):
        return self.activeModel()

    def setModelList(self, modelList):
        self.modelList = modelList

    def getModelList(self):
        return self.modelList

    # This method places and displays all elements
    def displayModelView(self):
        ### Frame 1 ( first screen )
        self.frame_1.place(relheight=1, relwidth=1)

        ## Frame 1 Top Half
        self.frame_1_top.place(relheight=0.75, relwidth=1)

        ## Frame 1 Bottom Half
        self.frame_1_bot.place(y=648, relheight=0.27, relwidth=1)

        # Placing them
        # 1st Block
        self.lbl_N.grid(row=0, column=0, padx=(10, 5), pady=(7, 0), sticky="e"); self.cmb_N.grid(row=0, column=1, padx=5, pady=(7, 0)); self.cmb_N.set("10000")
        self.lbl_S.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_S.grid(row=1, column=1, padx=5, sticky="ew"); self.scl_S.set("0.97")
        self.lbl_IR.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_IR.grid(row=2, column=1, padx=5, sticky="ew"); self.scl_IR.set("0.01")
        self.lbl_IL.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_IL.grid(row=3, column=1, padx=5, sticky="ew"); self.scl_IL.set("0.01")
        self.lbl_IP.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="e"); self.scl_IP.grid(row=4, column=1, padx=5, sticky="ew"); self.scl_IP.set("0.01")
        # 2nd Block
        self.lbl_WSN.grid(row=0, column=2, padx=5, pady=(7, 0), sticky="e"); self.cmb_WSN.grid(row=0, column=3, padx=5, pady=(7, 0)); self.cmb_WSN.set("10"); #self.cmb_WSN.bind("<<ComboboxSelected>>", self.updateModel())
        self.lbl_DEP.grid(row=1, column=2, padx=5, pady=5, sticky="e"); self.cmb_DEP.grid(row=1, column=3, padx=5, pady=5); self.cmb_DEP.set("50"); #self.cmb_DEP.bind("<<ComboboxSelected>>", self.updateModel())
        self.lbl_TRNS.grid(row=2, column=2, padx=5, pady=5, sticky="e"); self.cmb_TRNS.grid(row=2, column=3, padx=5, pady=5); self.cmb_TRNS.set("10"); #self.cmb_TRNS.bind("<<ComboboxSelected>>", self.updateModel())
        self.lbl_CNTCT.grid(row=3, column=2, padx=5, pady=5, sticky="e"); self.cmb_CNTCT.grid(row=3, column=3, padx=5, pady=5, sticky="ew"); self.cmb_CNTCT.set("1"); #self.cmb_CNTCT.bind("<<ComboboxSelected>>", self.updateModel())
        self.lbl_SCAN.grid(row=4, column=2, padx=5, pady=5, sticky="e"); self.scl_SCAN.grid(row=4, column=3, padx=5, sticky="ew"); self.scl_SCAN.set("27")
        # 3rd Block
        self.lbl_Ptrns.grid(row=0, column=4, padx=5, pady=(7, 0), sticky="e"); self.scl_Ptrns.grid(row=0, column=5, padx=5, pady=(7, 0)); self.scl_Ptrns.set("0.3")
        self.lbl_IrPsu.grid(row=1, column=4, padx=5, pady=5, sticky="e"); self.scl_IrPsu.grid(row=1, column=5, padx=5, sticky="ew"); self.scl_IrPsu.set("0.01")
        self.lbl_IlPsu.grid(row=2, column=4, padx=5, pady=5, sticky="e"); self.scl_IlPsu.grid(row=2, column=5, padx=5, sticky="ew"); self.scl_IlPsu.set("0.06")
        self.lbl_IpPsu.grid(row=3, column=4, padx=5, pady=5, sticky="e"); self.scl_IpPsu.grid(row=3, column=5, padx=5, sticky="ew"); self.scl_IpPsu.set("0.09")
        # 4th Block
        self.lbl_MSG.grid(row=0, column=6, padx=5, pady=(7, 0), sticky="e"); self.entry_MSG.grid(row=0, column=7, padx=5, pady=(7, 0)); self.entry_MSG.insert(0, "50")
        self.lbl_PWR.grid(row=1, column=6, padx=5, pady=5, sticky="e"); self.entry_PWR.grid(row=1, column=7, padx=5, pady=5); self.entry_PWR.insert(0, "0.7")
        self.lbl_BTRY.grid(row=2, column=6, padx=5, pady=5, sticky="e"); self.entry_BTRY.grid(row=2, column=7, padx=5, pady=5); self.entry_BTRY.insert(0, "864000")
        self.lbl_RR.grid(row=3, column=6, padx=5, pady=5, sticky="e"); self.scl_RR.grid(row=3, column=7, padx=5, sticky="ew"); self.scl_RR.set("0.5")
        self.lbl_T.grid(row=4, column=6, padx=5, pady=5, sticky="e"); self.scl_T.grid(row=4, column=7, padx=5, sticky="ew"); self.scl_T.set("100")
        # 5th Block
        self.btn_RUN.grid(row=0, column=8, padx=(60, 5), pady=(7, 4), sticky="ew")
        self.btn_INSP.grid(row=1, column=8, padx=(60, 5), pady=4, sticky="ew")
        self.btn_SAVE.grid(row=2, column=8, padx=(60, 5), pady=4, sticky="ew")
        self.btn_NEW.grid(row=3, column=8, padx=(60, 5), pady=4, sticky="ew")
        self.btn_CMPR.grid(row=4, column=8, padx=(60, 5), pady=4, sticky="ew")

        # Runnit
        self.base.mainloop()

    def updateModel(self, Stub):
        # N = int(self.cmb_N.get())
        # S = int(N * self.scl_S.get())
        # IR = int(N * self.scl_IR.get())
        # IL = int(N * self.scl_IL.get())
        # IP = int(N * self.scl_IP.get())
        # WSN = int(self.cmb_WSN.get())
        # DEP = int(self.cmb_DEP.get() * self.cmb_DEP.get())
        # TRNS = int(self.cmb_TRNS.get())
        # CNTCT = int(self.cmb_CNTCT.get())
        # SCAN = int(self.scl_SCAN.get())
        # PTrns = float(self.scl_Ptrns.get())
        # IrPsu = float(self.scl_IrPsu.get())
        # IlPsu = float(self.scl_IlPsu.get())
        # IpPsu = float(self.scl_IpPsu.get())
        # MSG = int(self.entry_MSG.get())
        # PWR = int(self.entry_PWR.get())
        # BTRY = int(self.entry_BTRY.get())
        # RR = float(self.scl_RR.get())
        # T = int(self.scl_T.get())
        #
        # self.activeModel = model.Model(N, S, IR, IL, IP, WSN, DEP, TRNS, CNTCT, SCAN, PTrns, IrPsu, IlPsu, IpPsu, MSG, PWR, BTRY, RR, T)
        OtherStub = Stub
        print("Hey")
