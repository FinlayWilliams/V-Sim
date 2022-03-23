import tkinter as tk
from tkinter import *


class HomeInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interfaces
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.newCompareModelList = []

        # Variables used to switch interfaces set to a default option
        self.controlInterfaceShow = "SISControlInterface"
        self.inspectInterfaceShow = "SISInspectInterface"

        ##################################### Instantiating LEFT-side elements #########################################

        # Left side of the screen frame
        frame_left = tk.Frame(self, bg="#453354")
        column_left_border = tk.Frame(frame_left, bg="white")
        self.column_left_frame = tk.Frame(frame_left, bg="#654e78")
        # Page title gui
        titleBgBorder = tk.Frame(frame_left, bg="white")
        titleBgInner = tk.Frame(frame_left, bg="#654e78")
        lblTitle = tk.Label(titleBgInner, text="V-Sim:", bg="#654e78",font=("Courier", 30, "underline"),
                            fg="white")
        lblTitle2 = tk.Label(titleBgInner, text="A Virus Model Simulation Tool", bg="#654e78",
                             font=("Courier", 20), fg="white")

        ####################################### Placing LEFT-side elements #############################################

        frame_left.place(x=0, y=0, height="864", width="718")
        column_left_border.place(relheight=0.87, relwidth=1, x=0, y=118)
        self.column_left_frame.place(relheight=0.86, relwidth=0.99, x=0, y=123)
        lblTitle.place(x=5, y=2)
        lblTitle2.place(x=5, y=50)
        titleBgBorder.place(x=82, y=23, height="100", width="635")
        titleBgInner.place(x=87, y=28, height="90", width="625")

        ##################################### Instantiating RIGHT-side elements ########################################

        frame_right = tk.Frame(self, bg="#453354")
        column_right_frame = tk.Frame(frame_right, bg="#a8a8a8")

        lbl_model_list = tk.Label(frame_right, text="Select an Active Model to Begin ... ",
                                  bg="#a8a8a8", font=("Arial", 12))
        # Creating the listbox where the list of all saved models will appear
        self.lstModels = tk.Listbox(frame_right, height=10, width=40, bg="#654e78", fg="white",
                                    selectbackground="#453354", font=("Calibri", 15))
        self.updateModelList()
        self.lstModels.bind("<<ListboxSelect>>",
                            lambda x: [self.updateActiveModel(controller, 1)])
        # Button: opens control page with the current active models
        btn_Configure = tk.Button(frame_right, width=17, text="Configure Model",
                                  command=lambda: [controller.display("HomeInterface", self.controlInterfaceShow)])
        # Button: opens inspect page with the current active models
        btn_Inspect = tk.Button(frame_right, width=17, text="Inspect Model",
                                  command=lambda: [controller.display("HomeInterface", self.inspectInterfaceShow)])
        # Button: Deletes selected models from models list
        btn_Delete = tk.Button(frame_right, width=17, text="Delete Model",
                               command=lambda: self.deleteSelectedModel(controller, 1))
        # Button: creates new default SIS models
        btn_New_SIS = tk.Button(frame_right, width=17, text="Default SIS Model",
                                command=lambda:[controller.addDefaultSISModel(), self.updateModelList(),
                                                self.updateCompareModelList()])
        # Button:
        btn_New_B1 = tk.Button(frame_right, width=17, text="PLACEHOLDER")
        # Button:
        btn_New_B2 = tk.Button(frame_right, width=17, text="PLACEHOLDER")

        lbl_compare_model_list = tk.Label(frame_right,
                                          text="Select a Model to Compare Against the Active Model ... ",
                                          bg="#a8a8a8", font=("Arial", 12))
        # Creating a second listbox of all models to for comparison
        self.lstCompareModels = tk.Listbox(frame_right, height=10, width=40, bg="#654e78", fg="white",
                                    selectbackground="#453354", font=("Calibri", 15))
        self.updateCompareModelList()
        self.lstCompareModels.bind("<<ListboxSelect>>",
                            lambda x: [self.updateCompareModel(controller, 1)])
        # Button: Deletes selected models from models list
        self.btn_Compare = tk.Button(frame_right, width=17, text="Compare Model", state="disabled",
                                command=lambda: [controller.display("HomeInterface", "SISCompareInterface")])

        ####################################### Placing RIGHT-side elements ############################################

        frame_right.place(x=717, y=0, height="864", width="819")
        column_right_frame.place(relheight=1, relwidth=0.7, x=135)

        lbl_model_list.place(x=218, y=60)
        self.lstModels.place(x=220, y=90)
        self.lstModels.select_set(0)
        btn_Inspect.place(x=220, y=350)
        btn_Configure.place(x=358, y=350)
        btn_Delete.place(x=496, y=350)
        btn_New_SIS.place(x=220, y=384)
        btn_New_B1.place(x=358, y=384)
        btn_New_B2.place(x=496, y=384)

        lbl_compare_model_list.place(x=218, y=460)
        self.lstCompareModels.place(x=220, y=490)
        self.btn_Compare.place(x=220, y=750)

        # This method must be called after the listbox is placed
        self.setModelInfoBox()

    # Method: called from base whenever the frame is repacked so the list of models is always refreshed on screen
    def updateModelList(self):
        self.lstModels.delete(0, END)
        for M in self.controller.models:
            self.lstModels.insert(END, M)

    # Method: This method populates the compare box with models of the same virus models type
    def updateCompareModelList(self):
        self.lstCompareModels.delete(0, END)

        self.newCompareModelList = []

        for M in self.controller.models:
            if self.checkModelType(self.controller.activeModel) == self.checkModelType(M):
                if self.controller.activeModel != M:
                    self.newCompareModelList.append(M)

        for M in self.newCompareModelList:
            self.lstCompareModels.insert(END, M)

    # Method: Deletes the currently selected models from the controllers list, replaces the active models with another
    def deleteSelectedModel(self, controller, stub):
        if len(controller.models) == 1:
            self.controller.popup("Invalid Delete", "There is Only One Model Left!")
        else:
            if self.lstModels.curselection() != ():

                controller.setActiveModel(0)
                controller.removeModel(int(''.join(map(str, self.lstModels.curselection()))))
                self.updateModelList()
                self.updateCompareModelList()
                self.controller.popup("Model Deleted", "The Active Model is now {}, (The First Entry)".format(controller.models[0].Name))

    # Method: checks to see what type of virus models is currently selected, used in a range of other GUI updates
    def checkModelType(self, model):
        if self.lstModels.curselection() != ():
            modelPrefix = model.Name.partition(":")

            if modelPrefix[0] == "SIS":
                return "SIS"
            if modelPrefix[0] == "SIR":
                return "SIR"
            if modelPrefix[0] == "SEIR":
                return "SEIR"

    # Method: called everytime a different entry in the listbox is selected, updating the controllers
    # (base windows) current active models and an index variable that is used when saving the models
    # also calls other methods that update the GUI and validate the models type
    def updateActiveModel(self, controller, stub):
        if self.lstModels.curselection() != ():
            # Long prefixes to take the listbox index and obtain a single integer to be used to
            # index with the controller
            oldActive = controller.activeModel
            controller.setActiveModel(int(''.join(map(str, self.lstModels.curselection()))))
            controller.setActiveModelIndex(int(''.join(map(str, self.lstModels.curselection()))))
            self.controller.setActiveModel(int(''.join(map(str, self.lstModels.curselection()))))

            self.updateCompareModelList()
            self.updateCompareModel(controller, 1)

            if self.checkModelType(controller.activeModel) != self.checkModelType(oldActive):
                self.setModelInfoBox()

                if self.checkModelType(self.controller.activeModel) == "SIS":
                    self.controlInterfaceShow = "SISControlInterface"
                    self.inspectInterfaceShow = "SISInspectInterface"
                    self.compareInterfaceShow = "SISCompareInterface"
                if self.checkModelType(self.controller.activeModel) == "SIR":
                    self.controlInterfaceShow = "SIRControlInterface"
                    self.inspectInterfaceShow = "SIRInspectInterface"
                    self.compareInterfaceShow = "SIRCompareInterface"
                if self.checkModelType(self.controller.activeModel) == "SEIR":
                    self.controlInterfaceShow = "SEIRControlInterface"
                    self.inspectInterfaceShow = "SEIRInspectInterface"
                    self.compareInterfaceShow = "SEIRCompareInterface"

    # Method: Called to update the compare models selection
    def updateCompareModel(self, controller, stub):
        if self.lstCompareModels.curselection() == ():
            self.btn_Compare.config(state="disabled")
        if self.lstCompareModels.curselection() != ():
            self.btn_Compare.config(state="active")
            controller.setCompareModel(self.newCompareModelList[int(''.join(map(str, self.lstCompareModels.curselection())))])

    # Method: Called whenever a models is selected to display the correct models information box
    def setModelInfoBox(self):
        if self.checkModelType(self.controller.activeModel) == "SIS":
            # This outputs the SIS models Information
            # Instantiating the information labels
            lbl_Title = tk.Label(self.column_left_frame, text="SIS Model Starting Condition Variables :", font=("Arial", 14, "italic"),
                                 bg="#654e78")
            infoFrame = tk.Frame(self.column_left_frame, bg="#654e78")
            lbl_N_Title = tk.Label(infoFrame, text="N", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_N_Desc = tk.Label(infoFrame, text=" The starting Node population count", font=("Arial", 10), bg="#654e78")
            lbl_S_Title = tk.Label(infoFrame, text="S", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_S_Desc = tk.Label(infoFrame, text=" The starting Susceptible population, "
                                                  "a percentage of N (default is 99%).",
                                  font=("Arial", 10), bg="#654e78")
            lbl_I_Title = tk.Label(infoFrame, text="I", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_I_Desc = tk.Label(infoFrame, text=" The starting Infected population count. This variable is "
                                                  "configured by changing the", font=("Arial", 10), bg="#654e78")
            lbl_I_Desc2 = tk.Label(infoFrame, text=" S variable and is always set so that S + I = N.", font=("Arial", 10),
                                   bg="#654e78")
            lbl_WSN_Title = tk.Label(infoFrame, text="WSN", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_WSN_Desc = tk.Label(infoFrame, text=" The number of Wireless Sensor Networks contained within the "
                                                    "hypothetical ", font=("Arial", 10), bg="#654e78")
            lbl_WSN_Desc2 = tk.Label(infoFrame, text=" network. This option determines how many Local groups the "
                                                     "N population is split into.", font=("Arial", 10), bg="#654e78")
            lbl_DEP_Title = tk.Label(infoFrame, text="Deployment Area", font=("Arial", 10, "bold"), bg="#654e78",
                                     fg="white")
            lbl_DEP_Desc = tk.Label(infoFrame, text=" The space that the hypothetical network is deployed over, "
                                                    "in Meters Squared", font=("Arial", 10), bg="#654e78")
            lbl_DEP_Desc2 = tk.Label(infoFrame, text=" This variable changes how far messages must travel before "
                                                     "reaching a node.", font=("Arial", 10), bg="#654e78")
            lbl_TRNS_Title = tk.Label(infoFrame, text="Transmission Range", font=("Arial", 10, "bold"), bg="#654e78",
                                      fg="white")
            lbl_TRNS_Desc = tk.Label(infoFrame, text=" The range each node is able to communicate, in Meters. "
                                                     "This variable", font=("Arial", 10), bg="#654e78")
            lbl_TRNS_Desc2 = tk.Label(infoFrame, text=" changes how far each node can send a message and propagate "
                                                      "a payload ...", font=("Arial", 10), bg="#654e78")
            lbl_CNTCT_Title = tk.Label(infoFrame, text="Contact Rate", font=("Arial", 10, "bold"), bg="#654e78",
                                       fg="white")
            lbl_CNTCT_Desc = tk.Label(infoFrame, text=" The contact rate for all Susceptible nodes, "
                                                      "the rate at which they", font=("Arial", 10), bg="#654e78")
            lbl_CNTCT_Desc2 = tk.Label(infoFrame, text=" communicate with any other nodes, "
                                                       "per Second.", font=("Arial", 10), bg="#654e78")
            lbl_SCAN_Title = tk.Label(infoFrame, text="Scanning Rate", font=("Arial", 10, "bold"), bg="#654e78",
                                      fg="white")
            lbl_SCAN_Desc = tk.Label(infoFrame, text=" The rate at which any infected node will scan for other nodes, "
                                                     "per Second", font=("Arial", 10), bg="#654e78")
            lbl_SCAN_Desc2 = tk.Label(infoFrame, text=" This will impact how well an infected node can spread the "
                                                      "infection.", font=("Arial", 10), bg="#654e78")
            lbl_PTrns_Title = tk.Label(infoFrame, text="PTransmission", font=("Arial", 10, "bold"), bg="#654e78",
                                       fg="white")
            lbl_PTrns_Desc = tk.Label(infoFrame, text=" The rate of a successful transmission of infection, "
                                                      "per contact of Infected to Susceptible.",
                                      font=("Arial", 10), bg="#654e78")
            lbl_IrPsu_Title = tk.Label(infoFrame, text="IR PSuccess", font=("Arial", 10, "bold"), bg="#654e78",
                                       fg="white")
            lbl_IrPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection when an Infected "
                                                      "node attacks with Random-Scanning (IR).",
                                      font=("Arial", 10), bg="#654e78")
            lbl_IlPsu_Title = tk.Label(infoFrame, text="IL PSuccess", font=("Arial", 10, "bold"), bg="#654e78",
                                       fg="white")
            lbl_IlPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection when an Infected node "
                                                      "attacks with Local-Scanning (IL).",
                                      font=("Arial", 10), bg="#654e78")
            lbl_IpPsu_Title = tk.Label(infoFrame, text="IP PSuccess", font=("Arial", 10, "bold"), bg="#654e78",
                                       fg="white")
            lbl_IpPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection when an Infected node "
                                                      "attacks with Peer-to-Peer (IP).",
                                      font=("Arial", 10), bg="#654e78")
            lbl_MSG_Title = tk.Label(infoFrame, text="Message Size", font=("Arial", 10, "bold"), bg="#654e78",
                                     fg="white")
            lbl_MSG_Desc = tk.Label(infoFrame, text=" The average size of a message sent between any nodes, in Bytes. "
                                                    "Changing this", font=("Arial", 10), bg="#654e78")
            lbl_MSG_Desc2 = tk.Label(infoFrame, text=" will impact how much effort it takes a node to send each "
                                                     "message.", font=("Arial", 10), bg="#654e78")
            lbl_PWR_Title = tk.Label(infoFrame, text="Power", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_PWR_Desc = tk.Label(infoFrame, text=" The average amount of power it takes to send a message between "
                                                    "any nodes,", font=("Arial", 10), bg="#654e78")
            lbl_PWR_Desc2 = tk.Label(infoFrame, text=" in Milliamps (mA). This also impact the effort (lifespan).",
                                     font=("Arial", 10), bg="#654e78")
            lbl_BTRY_Title = tk.Label(infoFrame, text="Battery Size", font=("Arial", 10, "bold"), bg="#654e78",
                                      fg="white")
            lbl_BTRY_Desc = tk.Label(infoFrame, text=" The total amount of battery life all nodes have, in Milliamps "
                                                     "per Hour (mAh)", font=("Arial", 10), bg="#654e78")
            lbl_BTRY_Desc2 = tk.Label(infoFrame, text=" This is how much energy a node has to work with before it "
                                                      "dies.", font=("Arial", 10), bg="#654e78")
            lbl_RR_Title = tk.Label(infoFrame, text="Recovery rate", font=("Arial", 10, "bold"), bg="#654e78",
                                    fg="white")
            lbl_RR_Desc = tk.Label(infoFrame, text=" The rate that Infected nodes recover and return to being "
                                                   "Susceptible nodes,", font=("Arial", 10), bg="#654e78")
            lbl_RR_Desc2 = tk.Label(infoFrame, text=" per Day. A general measure of human intervention to a network "
                                                    "attack.", font=("Arial", 10), bg="#654e78")
            lbl_T_Title = tk.Label(infoFrame, text="Timesteps", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_T_Desc = tk.Label(infoFrame, text=" The number of days to observe the simulation.", font=("Arial", 10),
                                  bg="#654e78")

            # Placing all information labels
            lbl_Title.pack(padx=15, pady=7, anchor="w")
            infoFrame.place(relwidth=0.98, relheight=1, x=7, y=40)
            lbl_N_Title.grid(row=0, column=0, sticky="e", pady=3)
            lbl_N_Desc.grid(row=0, column=1, sticky="w", pady=3)

            lbl_S_Title.grid(row=1, column=0, sticky="e", pady=3)
            lbl_S_Desc.grid(row=1, column=1, sticky="w", pady=3)

            lbl_I_Title.grid(row=2, column=0, sticky="e", pady=(3,0))
            lbl_I_Desc.grid(row=2, column=1, sticky="w", pady=(3,0))
            lbl_I_Desc2.grid(row=3, column=1, sticky="w")

            lbl_WSN_Title.grid(row=5, column=0, sticky="e", pady=(3,0))
            lbl_WSN_Desc.grid(row=5, column=1, sticky="w", pady=(3,0))
            lbl_WSN_Desc2.grid(row=6, column=1, sticky="w")

            lbl_DEP_Title.grid(row=7, column=0, sticky="e", pady=(3,0))
            lbl_DEP_Desc.grid(row=7, column=1, sticky="w", pady=(3,0))
            lbl_DEP_Desc2.grid(row=8, column=1, sticky="w")

            lbl_TRNS_Title.grid(row=9, column=0, sticky="e", pady=(3,0))
            lbl_TRNS_Desc.grid(row=9, column=1, sticky="w", pady=(3,0))
            lbl_TRNS_Desc2.grid(row=10, column=1, sticky="w")

            lbl_CNTCT_Title.grid(row=11, column=0, sticky="e", pady=(3,0))
            lbl_CNTCT_Desc.grid(row=11, column=1, sticky="w", pady=(3,0))
            lbl_CNTCT_Desc2.grid(row=12, column=1, sticky="w")

            lbl_SCAN_Title.grid(row=13, column=0, sticky="e", pady=(3,0))
            lbl_SCAN_Desc.grid(row=13, column=1, sticky="w", pady=(3,0))
            lbl_SCAN_Desc2.grid(row=14, column=1, sticky="w")

            lbl_PTrns_Title.grid(row=14, column=0, sticky="e", pady=3)
            lbl_PTrns_Desc.grid(row=14, column=1, sticky="w", pady=3)

            lbl_IrPsu_Title.grid(row=15, column=0, sticky="e", pady=3)
            lbl_IrPsu_Desc.grid(row=15, column=1, sticky="w", pady=3)

            lbl_IlPsu_Title.grid(row=16, column=0, sticky="e", pady=3)
            lbl_IlPsu_Desc.grid(row=16, column=1, sticky="w", pady=3)

            lbl_IpPsu_Title.grid(row=17, column=0, sticky="e", pady=3)
            lbl_IpPsu_Desc.grid(row=17, column=1, sticky="w", pady=3)

            lbl_MSG_Title.grid(row=18, column=0, sticky="e", pady=(3,0))
            lbl_MSG_Desc.grid(row=18, column=1, sticky="w", pady=(3,0))
            lbl_MSG_Desc2.grid(row=19, column=1, sticky="w")

            lbl_PWR_Title.grid(row=20, column=0, sticky="e", pady=(3,0))
            lbl_PWR_Desc.grid(row=20, column=1, sticky="w", pady=(3,0))
            lbl_PWR_Desc2.grid(row=21, column=1, sticky="w")

            lbl_BTRY_Title.grid(row=22, column=0, sticky="e", pady=(3,0))
            lbl_BTRY_Desc.grid(row=22, column=1, sticky="w", pady=(3,0))
            lbl_BTRY_Desc2.grid(row=23, column=1, sticky="w")

            lbl_RR_Title.grid(row=24, column=0, sticky="e", pady=(3,0))
            lbl_RR_Desc.grid(row=24, column=1, sticky="w", pady=(3,0))
            lbl_RR_Desc2.grid(row=25, column=1, sticky="w")

            lbl_T_Title.grid(row=26, column=0, sticky="e", pady=3)
            lbl_T_Desc.grid(row=26, column=1, sticky="w", pady=3)

        if self.checkModelType(self.controller.activeModel) == "SIR":
            # This outputs the SIR models information
            # Instantiating the information labels
            lbl_Title = tk.Label(self.column_left_frame, text="SIR Model Starting Condition Variables :", font=("Arial", 14),
                                 bg="#654e78")
            infoFrame = tk.Frame(self.column_left_frame, bg="#654e78")
            lbl_N_Title = tk.Label(infoFrame, text="N", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_N_Desc = tk.Label(infoFrame, text=" The starting population count", font=("Arial", 10),
                                  bg="#654e78")
            lbl_S_Title = tk.Label(infoFrame, text="S", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_S_Desc = tk.Label(infoFrame, text=" The starting Susceptible population, "
                                                  "a percentage of N (default is 99%).",
                                  font=("Arial", 10), bg="#654e78")
            lbl_I_Title = tk.Label(infoFrame, text="I", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_I_Desc = tk.Label(infoFrame, text=" The starting Infected population count. This variable is "
                                                  "configured by changing the", font=("Arial", 10), bg="#654e78")
            lbl_I_Desc2 = tk.Label(infoFrame, text=" S variable and is always set so that S + I = N.",
                                   font=("Arial", 10),
                                   bg="#654e78")
            lbl_Beta_Title = tk.Label(infoFrame, text="Beta", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_Beta_Desc = tk.Label(infoFrame, text=" I do not know ", font=("Arial", 10), bg="#654e78")
            lbl_Beta_Desc2 = tk.Label(infoFrame, text=" not know what this is.", font=("Arial", 10), bg="#654e78")
            lbl_Gamma_Title = tk.Label(infoFrame, text="Gamma", font=("Arial", 10, "bold"), bg="#654e78",
                                     fg="white")
            lbl_Gamma_Desc = tk.Label(infoFrame, text=" I do not know", font=("Arial", 10), bg="#654e78")
            lbl_Gamma_Desc2 = tk.Label(infoFrame, text=" not know what this is.", font=("Arial", 10), bg="#654e78")
            lbl_Timesteps_Title = tk.Label(infoFrame, text="Timesteps", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_Timesteps_Desc = tk.Label(infoFrame, text=" The number of days the simulation is to be observed. ", font=("Arial", 10), bg="#654e78")

            # Placing all information labels
            infoFrame.place(relwidth=0.98, relheight=1, x=7, y=40)
            lbl_Title.pack(pady=7)
            lbl_N_Title.grid(row=0, column=0, sticky="e", pady=3)
            lbl_N_Desc.grid(row=0, column=1, sticky="w", pady=3)

            lbl_S_Title.grid(row=1, column=0, sticky="e", pady=3)
            lbl_S_Desc.grid(row=1, column=1, sticky="w", pady=3)

            lbl_I_Title.grid(row=2, column=0, sticky="e", pady=(3, 0))
            lbl_I_Desc.grid(row=2, column=1, sticky="w", pady=(3, 0))
            lbl_I_Desc2.grid(row=3, column=1, sticky="w")

            lbl_Beta_Title.grid(row=5, column=0, sticky="e", pady=(3, 0))
            lbl_Beta_Desc.grid(row=5, column=1, sticky="w", pady=(3, 0))
            lbl_Beta_Desc2.grid(row=6, column=1, sticky="w")

            lbl_Gamma_Title.grid(row=7, column=0, sticky="e", pady=(3, 0))
            lbl_Gamma_Desc.grid(row=7, column=1, sticky="w", pady=(3, 0))
            lbl_Gamma_Desc2.grid(row=8, column=1, sticky="w")

            lbl_Timesteps_Title.grid(row=9, column=0, sticky="e", pady=(3, 0))
            lbl_Timesteps_Desc.grid(row=9, column=1, sticky="w", pady=(3, 0))

        if self.checkModelType(self.controller.activeModel) == "SEIR":
            # This outputs the SEIR models information
            # Instantiating the information labels
            lbl_Title = tk.Label(self.column_left_frame, text="SEIR Model Starting Condition Variables :", font=("Arial", 14), bg="#654e78")
            infoFrame = tk.Frame(self.column_left_frame, bg="#654e78")

            # Placing all information labels
            infoFrame.place(relwidth=0.98, relheight=1, x=7, y=40)
            lbl_Title.pack(pady=7)
