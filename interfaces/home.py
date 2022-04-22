import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image


class HomeInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interfaces. This is the same for each interface class
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.newCompareConfigurationList = []

        ##################################### Instantiating LEFT-side elements #########################################
        # Left side frame
        frame_left = tk.Frame(self, bg="#453354")
        column_left_border = tk.Frame(frame_left, bg="white")
        column_left_frame = tk.Frame(frame_left, bg="#654e78")
        self.lblVariableTitle = tk.Label(column_left_frame, text="IoT-SIS Model Starting Condition Variables :", font=("Arial", 14, "italic"), bg="#654e78")
        infoFrame = tk.Frame(column_left_frame, bg="#654e78")
        lbl_N_Title = tk.Label(infoFrame, text="N", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_N_Desc = tk.Label(infoFrame, text=" The starting Node population count", font=("Arial", 10), bg="#654e78")
        lbl_S_Title = tk.Label(infoFrame, text="S", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_S_Desc = tk.Label(infoFrame, text=" The starting Susceptible (S) population.", font=("Arial", 10), bg="#654e78")
        lbl_I_Title = tk.Label(infoFrame, text="I", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_I_Desc = tk.Label(infoFrame, text=" The starting Infected population count. The reccomended and default value is 1.", font=("Arial", 10), bg="#654e78")
        #lbl_I_Desc2 = tk.Label(infoFrame, text="larger values  demonstrates the power of a larger starting attack force. ", font=("Arial", 10), bg="#654e78")
        lbl_WSN_Title = tk.Label(infoFrame, text="WSN", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_WSN_Desc = tk.Label(infoFrame, text=" The number of Wireless Sensor Networks contained within the hypothetical network.", font=("Arial", 10), bg="#654e78")
        lbl_WSN_Desc2 = tk.Label(infoFrame, text=" This option determines how many Local groups the N population is split into.", font=("Arial", 10), bg="#654e78")
        lbl_DEP_Title = tk.Label(infoFrame, text="Deployment Area", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_DEP_Desc = tk.Label(infoFrame, text=" The space that the hypothetical network is deployed over, in Meters Squared. ", font=("Arial", 10), bg="#654e78")
        lbl_DEP_Desc2 = tk.Label(infoFrame, text=" This variable changes how far messages must travel before reaching a node.", font=("Arial", 10), bg="#654e78")
        lbl_TRNS_Title = tk.Label(infoFrame, text="Transmission Range", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_TRNS_Desc = tk.Label(infoFrame, text=" The range each node is able to communicate, in Meters. This variable", font=("Arial", 10), bg="#654e78")
        lbl_TRNS_Desc2 = tk.Label(infoFrame, text=" changes how far each node can send a message and propagate a payload.", font=("Arial", 10), bg="#654e78")
        lbl_CNTCT_Title = tk.Label(infoFrame, text="Contact Rate", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_CNTCT_Desc = tk.Label(infoFrame, text=" The contact rate for all Susceptible nodes, the rate at which they communicate with.", font=("Arial", 10), bg="#654e78")
        lbl_CNTCT_Desc2 = tk.Label(infoFrame, text=" any other nodes, per Second.", font=("Arial", 10), bg="#654e78")
        lbl_SCAN_Title = tk.Label(infoFrame, text="Scanning Rate", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_SCAN_Desc = tk.Label(infoFrame, text=" The rate at which infected nodes scan to make contact with other nodes, per Second.", font=("Arial", 10), bg="#654e78")
        #lbl_SCAN_Desc2 = tk.Label(infoFrame, text=" ", font=("Arial", 10), bg="#654e78")
        lbl_PTrns_Title = tk.Label(infoFrame, text="PTransmission", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_PTrns_Desc = tk.Label(infoFrame, text=" The rate of a successful transmission of infection, per contact of Infected to Susceptible.", font=("Arial", 10), bg="#654e78")
        lbl_PTrns_Desc2 = tk.Label(infoFrame, text=" The recommended and default value is left on 'Expected'.", font=("Arial", 10), bg="#654e78")
        lbl_IrPsu_Title = tk.Label(infoFrame, text="IR PSuccess", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_IrPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection per contact, per second, for Random-Scanning (IR).", font=("Arial", 10), bg="#654e78")
        lbl_IrPsu_Desc2 = tk.Label(infoFrame, text=" The recommended and default value is left on 'Expected'.", font=("Arial", 10), bg="#654e78")
        lbl_IlPsu_Title = tk.Label(infoFrame, text="IL PSuccess", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_IlPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection per contact, per second, for Local-Scanning (IL).", font=("Arial", 10), bg="#654e78")
        lbl_IlPsu_Desc2 = tk.Label(infoFrame, text=" The recommended and default value is left on 'Expected'.", font=("Arial", 10), bg="#654e78")
        lbl_IpPsu_Title = tk.Label(infoFrame, text="IP PSuccess", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_IpPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection per contact, per second, for Peer-to-Peer (IP).", font=("Arial", 10), bg="#654e78")
        lbl_IpPsu_Desc2 = tk.Label(infoFrame, text=" The recommended and default value is left on 'Expected'.", font=("Arial", 10), bg="#654e78")
        lbl_MSG_Title = tk.Label(infoFrame, text="Message Size", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_MSG_Desc = tk.Label(infoFrame, text=" The mean size of a message sent between any nodes, in Bytes.", font=("Arial", 10), bg="#654e78")
        #lbl_MSG_Desc2 = tk.Label(infoFrame, text=" will impact how much effort it takes a node to send each message.", font=("Arial", 10), bg="#654e78")
        lbl_PWR_Title = tk.Label(infoFrame, text="Power per Message", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_PWR_Desc = tk.Label(infoFrame, text=" The mean amount of power it takes to send a message between any nodes in Milliamps (mA).", font=("Arial", 10), bg="#654e78")
        #lbl_PWR_Desc2 = tk.Label(infoFrame, text="  This also impact the effort (lifespan).", font=("Arial", 10), bg="#654e78")
        lbl_BTRY_Title = tk.Label(infoFrame, text="Battery Size", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_BTRY_Desc = tk.Label(infoFrame, text=" The total amount of battery life all nodes have, in Milliamps per Hour (mAh).", font=("Arial", 10), bg="#654e78")
        #lbl_BTRY_Desc2 = tk.Label(infoFrame, text=" This is how much energy a node has to work with before it dies.", font=("Arial", 10), bg="#654e78")
        lbl_RR_Title = tk.Label(infoFrame, text="Security Level", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_RR_Desc = tk.Label(infoFrame, text=" The rate that Infected nodes recover and return to being Susceptible nodes, per hour. ", font=("Arial", 10), bg="#654e78")
        lbl_RR_Desc2 = tk.Label(infoFrame, text=" A general measure of Admin Intervention to a network attack.", font=("Arial", 10), bg="#654e78")
        lbl_T_Title = tk.Label(infoFrame, text="Timesteps", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
        lbl_T_Desc = tk.Label(infoFrame, text=" The number of hours to observe the simulation.", font=("Arial", 10), bg="#654e78")

        # Page Icon GUI
        self.virusIcon = ImageTk.PhotoImage(Image.open("assets/virus_icon.png"))
        placeableLogo = tk.Label(frame_left, image=self.virusIcon, compound="center", padx=0, pady=0, borderwidth=0, highlightthickness=0, bg="#453354")
        # Page title GUI
        titleBgBorder = tk.Frame(frame_left, bg="white")
        titleBgInner = tk.Frame(frame_left, bg="#654e78")
        lblTitle = tk.Label(titleBgInner, text="V-Sim:", bg="#654e78", font=("Courier", 30, "underline"), fg="white")
        lblSubTitle = tk.Label(titleBgInner, text="A Virus Spread Simulation Tool for Botnet Propagation in IoT Devices", bg="#654e78", font=("Courier", 11), fg="white")

        ##################################### Instantiating RIGHT-side elements ########################################
        frame_right = tk.Frame(self, bg="#453354")
        column_right_frame = tk.Frame(frame_right, bg="#a8a8a8")

        # Creating the listbox where the list of all saved models will appear
        lbl_model_list = tk.Label(frame_right, text="Select an Active Configuration to Begin",bg="#a8a8a8", font=("Arial", 12))
        self.lstConfig = tk.Listbox(frame_right, height=12, width=40, bg="#654e78", fg="white", selectbackground="#453354", font=("Calibri", 15))
        self.updateConfigurationList()
        self.lstConfig.bind("<<ListboxSelect>>", lambda x: [self.updateActiveConfiguration(controller, 1)])

        # Button: opens control page with the current active models
        btn_Configure = tk.Button(frame_right, width=17, text="Control Configuration", command=lambda: [controller.display("HomeInterface", "SISControlInterface")])
        # Button: opens inspect page with the current active models
        btn_Inspect = tk.Button(frame_right, width=17, text="Inspect Configuration", command=lambda: [controller.display("HomeInterface", "SISInspectInterface")])
        # Button: Deletes selected models from models list
        btn_Delete = tk.Button(frame_right, width=17, text="Delete Configuration", command=lambda: self.deleteSelectedConfiguration(controller, 1))
        # Button: creates new default SIS models
        btn_New_SIS = tk.Button(frame_right, width=17, text="Default SIS Model", command=lambda:[controller.addDefaultSISConfiguration(), self.updateConfigurationList(), self.updateCompareConfigurationList(controller)])

        # Creating a second listbox of all models to for comparison
        lbl_compare_model_list = tk.Label(frame_right, text="Select a Configuration to Compare Against the Active Configuration", bg="#a8a8a8", font=("Arial", 12))
        self.lstCompareConfig = tk.Listbox(frame_right, height=10, width=40, bg="#654e78", fg="white", selectbackground="#453354", font=("Calibri", 15))
        self.updateCompareConfigurationList(controller)
        self.lstCompareConfig.bind("<<ListboxSelect>>", lambda x: [self.updateCompareConfiguration(controller, 1)])
        self.lstCompareConfig.config()

        # Button: Deletes selected models from models list
        self.btn_Compare = tk.Button(frame_right, width=17, text="Compare Configuration", state="disabled", command=lambda: [controller.display("HomeInterface", "SISCompareInterface")])

        ########################################## Placing All elements ###############################################
        # Left
        frame_left.place(x=0, y=0, height="864", width="718")
        column_left_border.place(relheight=0.87, relwidth=1, x=0, y=118)
        column_left_frame.place(relheight=0.86, relwidth=0.99, x=0, y=123)
        self.lblVariableTitle.place(x=7, y=7)
        placeableLogo.place(x=6, y=33)
        lblTitle.place(x=5, y=3)
        lblSubTitle.place(x=5, y=56)
        titleBgBorder.place(x=82, y=23, height="100", width="635")
        titleBgInner.place(x=87, y=28, height="90", width="625")
        infoFrame.place(relwidth=0.98, relheight=1, x=7, y=40)
        lbl_N_Title.grid(row=0, column=0, sticky="e", pady=3)
        lbl_N_Desc.grid(row=0, column=1, sticky="w", pady=3)
        lbl_S_Title.grid(row=1, column=0, sticky="e", pady=3)
        lbl_S_Desc.grid(row=1, column=1, sticky="w", pady=3)
        lbl_I_Title.grid(row=2, column=0, sticky="e", pady=(3, 0))
        lbl_I_Desc.grid(row=2, column=1, sticky="w", pady=(3, 0))
        #lbl_I_Desc2.grid(row=3, column=1, sticky="w")
        lbl_WSN_Title.grid(row=3, column=0, sticky="e", pady=(3, 0))
        lbl_WSN_Desc.grid(row=3, column=1, sticky="w", pady=(3, 0))
        lbl_WSN_Desc2.grid(row=4, column=1, sticky="w")
        lbl_DEP_Title.grid(row=5, column=0, sticky="e", pady=(3, 0))
        lbl_DEP_Desc.grid(row=5, column=1, sticky="w", pady=(3, 0))
        lbl_DEP_Desc2.grid(row=6, column=1, sticky="w")
        lbl_TRNS_Title.grid(row=7, column=0, sticky="e", pady=(3, 0))
        lbl_TRNS_Desc.grid(row=7, column=1, sticky="w", pady=(3, 0))
        lbl_TRNS_Desc2.grid(row=8, column=1, sticky="w")
        lbl_CNTCT_Title.grid(row=9, column=0, sticky="e", pady=(3, 0))
        lbl_CNTCT_Desc.grid(row=9, column=1, sticky="w", pady=(3, 0))
        lbl_CNTCT_Desc2.grid(row=10, column=1, sticky="w")
        lbl_SCAN_Title.grid(row=11, column=0, sticky="e", pady=(3, 0))
        lbl_SCAN_Desc.grid(row=11, column=1, sticky="w", pady=(3, 0))
        #lbl_SCAN_Desc2.grid(row=14, column=1, sticky="w")
        lbl_IrPsu_Title.grid(row=12, column=0, sticky="e", pady=(3, 0))
        lbl_IrPsu_Desc.grid(row=12, column=1, sticky="w", pady=(3, 0))
        lbl_IrPsu_Desc2.grid(row=13, column=1, sticky="w")
        lbl_IlPsu_Title.grid(row=14, column=0, sticky="e", pady=(3, 0))
        lbl_IlPsu_Desc.grid(row=14, column=1, sticky="w", pady=(3, 0))
        lbl_IlPsu_Desc2.grid(row=15, column=1, sticky="w")
        lbl_IpPsu_Title.grid(row=16, column=0, sticky="e", pady=(3, 0))
        lbl_IpPsu_Desc.grid(row=16, column=1, sticky="w", pady=(3, 0))
        lbl_IpPsu_Desc2.grid(row=17, column=1, sticky="w")
        lbl_PTrns_Title.grid(row=18, column=0, sticky="e", pady=(3, 0))
        lbl_PTrns_Desc.grid(row=18, column=1, sticky="w", pady=(3, 0))
        lbl_PTrns_Desc2.grid(row=19, column=1, sticky="w")
        lbl_MSG_Title.grid(row=20, column=0, sticky="e", pady=(3, 0))
        lbl_MSG_Desc.grid(row=20, column=1, sticky="w", pady=(3, 0))
        #lbl_MSG_Desc2.grid(row=19, column=1, sticky="w")
        lbl_PWR_Title.grid(row=21, column=0, sticky="e", pady=(3, 0))
        lbl_PWR_Desc.grid(row=21, column=1, sticky="w", pady=(3, 0))
        #lbl_PWR_Desc2.grid(row=21, column=1, sticky="w")
        lbl_BTRY_Title.grid(row=22, column=0, sticky="e", pady=3)
        lbl_BTRY_Desc.grid(row=22, column=1, sticky="w", pady=3)
        #lbl_BTRY_Desc2.grid(row=23, column=1, sticky="w")
        lbl_RR_Title.grid(row=23, column=0, sticky="e", pady=(3, 0))
        lbl_RR_Desc.grid(row=23, column=1, sticky="w", pady=(3, 0))
        lbl_RR_Desc2.grid(row=24, column=1, sticky="w")
        lbl_T_Title.grid(row=25, column=0, sticky="e", pady=3)
        lbl_T_Desc.grid(row=25, column=1, sticky="w", pady=(3, 0))
        # Right
        frame_right.place(x=717, y=0, height="864", width="819")
        column_right_frame.place(relheight=1, relwidth=0.7, x=135)
        lbl_model_list.place(x=270, y=40)
        self.lstConfig.place(x=220, y=70)
        self.lstConfig.select_set(0)
        btn_Inspect.place(x=220, y=382)
        btn_Configure.place(x=358, y=382)
        btn_Delete.place(x=496, y=382)
        btn_New_SIS.place(x=358, y=416)
        lbl_compare_model_list.place(x=186, y=470)
        self.lstCompareConfig.place(x=220, y=500)
        self.btn_Compare.place(x=358, y=760)

    # Method: called from base whenever the frame is repacked so the list of models is always refreshed on screen
    def updateConfigurationList(self):
        self.lstConfig.delete(0, END)
        for C in self.controller.configurations:
            self.lstConfig.insert(END, C)

    # Method: This method populates the compare box with models of the same virus models type
    def updateCompareConfigurationList(self, controller):
        self.lstCompareConfig.delete(0, END)
        self.newCompareConfigurationList = []

        for C in controller.configurations:
            if controller.activeConfiguration != C:
                self.newCompareConfigurationList.append(C)
        for C in self.newCompareConfigurationList:
            self.lstCompareConfig.insert(END, C)

    # Method: Deletes the currently selected models from the controllers list, replaces the active models with another
    def deleteSelectedConfiguration(self, controller, stub):
        if len(controller.configurations) == 1:
            self.controller.popup("Invalid Delete", "There is Only One Configuration Left!")
        else:
            if self.lstConfig.curselection() != ():
                controller.setActiveConfiguration(0)
                controller.removeConfiguration(int(''.join(map(str, self.lstConfig.curselection()))))
                self.updateConfigurationList()
                self.updateCompareConfigurationList(controller)
                self.controller.popup("Model Deleted", "The Active Configuration is now {}, (The First Entry)".format(controller.configurations[0].Name))

    # Called everytime listbox is updated & other GUI updates, updates a range of variables and indexes
    def updateActiveConfiguration(self, controller, stub):
        if self.lstConfig.curselection() != ():
            # Long prefixes = obtaining listbox idx and reformatting
            oldActive = controller.activeConfiguration
            controller.setActiveConfiguration(int(''.join(map(str, self.lstConfig.curselection()))))
            controller.setActiveConfigurationIndex(int(''.join(map(str, self.lstConfig.curselection()))))
            self.controller.setActiveConfiguration(int(''.join(map(str, self.lstConfig.curselection()))))

            self.updateCompareConfigurationList(controller)
            self.updateCompareConfiguration(controller, 1)

    # Called to update the compare configuration selection
    def updateCompareConfiguration(self, controller, stub):
        if self.lstCompareConfig.curselection() == ():
            self.btn_Compare.config(state="disabled")
        if self.lstCompareConfig.curselection() != ():
            self.btn_Compare.config(state="active")
            controller.setCompareConfiguration(self.newCompareConfigurationList[int(''.join(map(str, self.lstCompareConfig.curselection())))])
