import tkinter as tk
from tkinter import *


class HomeInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        ##################################### Instantiating LEFT-side elements #########################################

        # Left side of the screen frame
        frame_left = tk.Frame(self, bg="#654e78")
        column_left_border = tk.Frame(frame_left, bg="white")
        self.column_left_frame = tk.Frame(frame_left, bg="#654e78")
        # Page title gui
        titleBgBorder = tk.Frame(frame_left, bg="white")
        titleBgInner = tk.Frame(frame_left, bg="#654e78")
        lblTitle = tk.Label(titleBgInner, text="IoT-SIS Sim:", bg="#654e78",font=("Courier", 30, "underline"),
                            fg="white")
        lblTitle2 = tk.Label(titleBgInner, text="An IoT-SIS Virus model Simulation Tool", bg="#654e78",
                                  font=("Courier", 20), fg="white")


        ####################################### Placing LEFT-side elements #############################################

        frame_left.place(x=0, y=0, height="864", width="718")
        column_left_border.place(relheight=0.87, relwidth=1, x=0, y=118)
        self.column_left_frame.place(relheight=0.86, relwidth=0.99, x=0, y=123)
        lblTitle.place(x=5, y=2)
        lblTitle2.place(x=5, y=50)
        titleBgBorder.place(x=25, y=23, height="100", width="635")
        titleBgInner.place(x=30, y=28, height="90", width="625")

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
                            lambda x: self.updateActiveModel(controller, 1))
        # Button: opens control page with the current active model
        btn_Configure = tk.Button(frame_right, width=17, text="Configure Model",
                              command=lambda: [controller.display("HomeInterface", "ControlInterface")])
        # Button: opens inspect page with the current active model
        btn_Inspect = tk.Button(frame_right, width=17, text="Inspect Model")
        # Button: Deletes selected model from model list
        btn_Delete = tk.Button(frame_right, width=17, text="Delete Model",
                               command=lambda: self.deleteSelectedModel(controller, 1))
        # Button: creates new default SIS model
        btn_New_SIS = tk.Button(frame_right, width=17, text="New SIS Model")
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
        # Button: Deletes selected model from model list
        btn_Compare = tk.Button(frame_right, width=17, text="Compare Model")

        ####################################### Placing RIGHT-side elements ############################################

        frame_right.place(x=717, y=0, height="864", width="819")
        column_right_frame.place(relheight=1, relwidth=0.7, x=135)

        lbl_model_list.place(x=218, y=20)
        self.lstModels.place(x=220, y=50)
        self.lstModels.select_set(0)
        btn_Configure.place(x=220, y=310)
        btn_Inspect.place(x=358, y=310)
        btn_Delete.place(x=496, y=310)
        btn_New_SIS.place(x=220, y=344)
        btn_New_B1.place(x=358, y=344)
        btn_New_B2.place(x=496, y=344)

        lbl_compare_model_list.place(x=218, y=420)
        self.lstCompareModels.place(x=220, y=450)
        btn_Compare.place(x=220, y=710)

        # This method must be called after the listbox is placed
        self.setModelInfoBox()

    # Method: called from base whenever the frame is repacked so the list of models is always refreshed on screen
    def updateModelList(self):
        self.lstModels.delete(0, END)
        for M in self.controller.models:
            self.lstModels.insert(END, M)

    # Method: Same as previous method but for the comparison model list
    def updateCompareModelList(self):
        self.lstCompareModels.delete(0, END)
        for M in self.controller.models:
            self.lstCompareModels.insert(END, M)

    # Method: Deletes the currently selected model from the controllers list, replaces the active model with another
    def deleteSelectedModel(self, controller, stub):
        if len(controller.models) == 1:
            self.controller.popup("Invalid Delete", "There is only one model left!")
        else:
            controller.setActiveModel(0)
            controller.removeModel(int(''.join(map(str, self.lstModels.curselection()))))
            self.updateModelList()
            self.updateCompareModelList()
            self.controller.popup("Model Deleted", "The Active Model is now {}".format(controller.models[0].Name))

    # Method: checks to see what virus model is currently selected
    def checkModelType(self):
        if self.lstModels.curselection() != ():
            modelName = self.lstModels.get(self.lstModels.curselection())
            modelPrefix = modelName.partition(":")

            if modelPrefix[0] == "SIS":
                return "SIS"
            if modelPrefix[0] == "SIR":
                return "SIR"
            if modelPrefix[0] == "SIRD":
                return "SIRD"

    # Method: called everytime a different entry in the listbox is selected, updating the controllers
    # (base windows) current active model and an index variable that is used when saving the models
    # also calls other methods that update the GUI
    def updateActiveModel(self, controller, stub):
        if self.lstModels.curselection() != ():
            # Long prefixes to take the listbox index and obtain a single integer to be used to
            # index with the controller
            controller.setActiveModel(int(''.join(map(str, self.lstModels.curselection()))))
            controller.setActiveModelIndex(int(''.join(map(str, self.lstModels.curselection()))))

            self.updateListboxes()
            self.setModelInfoBox()

    # Method: Called whenever a model is selected to update the listboxes
    def updateListboxes(self):
        pass

    # Method: Called whenever a model is selected to display the correct model information box
    def setModelInfoBox(self):
        if self.checkModelType() == "SIS":
            # This outputs the SIS model Information
            lbl_Title = tk.Label(self.column_left_frame, text="SIS Model Variable Explanation", font=("Arial", 14),
                                 bg="#654e78")
            infoFrame = tk.Frame(self.column_left_frame, bg="#654e78")

            lbl_N_Title = tk.Label(infoFrame, text="N", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_N_Desc = tk.Label(infoFrame, text=" The starting Node count", font=("Arial", 10), bg="#654e78")

            lbl_S_Title = tk.Label(infoFrame, text="S", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_S_Desc = tk.Label(infoFrame, text=" A percentage of the number chosen for the N value, a decimal between 0-1 (default is 99%)", font=("Arial", 10), bg="#654e78")

            lbl_IR_Title = tk.Label(infoFrame, text="IR", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_IR_Desc = tk.Label(infoFrame, text=" A percentage of the number chosen for the N value, a decimal between 0-1 (default is 0.3%)", font=("Arial", 10), bg="#654e78")

            lbl_IL_Title = tk.Label(infoFrame, text="IL", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_IL_Desc = tk.Label(infoFrame, text=" A percentage of the number chosen for the N value, a decimal between 0-1 (default is 0.3%)", font=("Arial", 10), bg="#654e78")

            lbl_IP_Title = tk.Label(infoFrame, text="IP", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_IP_Desc = tk.Label(infoFrame, text=" A percentage of the number chosen for the N value, a decimal between 0-1 (default is 0.4%)", font=("Arial", 10), bg="#654e78")

            lbl_WSN_Title = tk.Label(infoFrame, text="WSN", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_WSN_Desc = tk.Label(infoFrame, text=" The number of Wireless Sensor Networks contained within your hypothetical ", font=("Arial", 10), bg="#654e78")
            lbl_WSN_Desc2 = tk.Label(infoFrame, text=" network. This option determines how many groups the N population is split into", font=("Arial", 10), bg="#654e78")

            lbl_DEP_Title = tk.Label(infoFrame, text="Deployment Area", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_DEP_Desc = tk.Label(infoFrame, text=" The space that your hypothetical network is deployed over, in Meters Squared", font=("Arial", 10), bg="#654e78")
            lbl_DEP_Desc2 = tk.Label(infoFrame, text=" This variable changes how far a message must travel before reaching a node", font=("Arial", 10), bg="#654e78")

            lbl_TRNS_Title = tk.Label(infoFrame, text="Transmission Range", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_TRNS_Desc = tk.Label(infoFrame, text=" The range each node is able to communicate at, in Meters. This variable", font=("Arial", 10), bg="#654e78")
            lbl_TRNS_Desc2 = tk.Label(infoFrame, text=" changes how far each node can send a message and propagate a payload ...", font=("Arial", 10), bg="#654e78")

            lbl_CNTCT_Title = tk.Label(infoFrame, text="Contact Rate", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_CNTCT_Desc = tk.Label(infoFrame, text=" The contact rate for all Susceptible nodes, the rate at which they", font=("Arial", 10), bg="#654e78")
            lbl_CNTCT_Desc2 = tk.Label(infoFrame, text=" communicate with any other nodes, per Second", font=("Arial", 10), bg="#654e78")

            lbl_SCAN_Title = tk.Label(infoFrame, text="Scanning Rate", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_SCAN_Desc = tk.Label(infoFrame, text=" The rate at which any infected node will scan for other nodes, per Second", font=("Arial", 10), bg="#654e78")
            lbl_SCAN_Desc2 = tk.Label(infoFrame, text=" This will impact how well an infected node can spread the infection", font=("Arial", 10), bg="#654e78")

            lbl_PTrns_Title = tk.Label(infoFrame, text="PTransmission", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_PTrns_Desc = tk.Label(infoFrame, text=" The rate of a successful transmission of infection, per contact of Infected to Susceptible", font=("Arial", 10), bg="#654e78")

            lbl_IrPsu_Title = tk.Label(infoFrame, text="IR PSuccess", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_IrPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection when an Infected node attacks with Random-Scanning (IR)", font=("Arial", 10), bg="#654e78")

            lbl_IlPsu_Title = tk.Label(infoFrame, text="IL PSuccess", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_IlPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection when an Infected node attacks with Local-Scanning (IL)", font=("Arial", 10), bg="#654e78")

            lbl_IpPsu_Title = tk.Label(infoFrame, text="IP PSuccess", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_IpPsu_Desc = tk.Label(infoFrame, text=" The rate of a successful connection when an Infected node attacks with Peer-to-Peer (IP)", font=("Arial", 10), bg="#654e78")

            lbl_MSG_Title = tk.Label(infoFrame, text="Message Size", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_MSG_Desc = tk.Label(infoFrame, text=" The average size of a message sent between any nodes, in Bytes. Changing this", font=("Arial", 10), bg="#654e78")
            lbl_MSG_Desc2 = tk.Label(infoFrame, text=" will impact how much effort it takes a node to send each message", font=("Arial", 10), bg="#654e78")

            lbl_PWR_Title = tk.Label(infoFrame, text="Power", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_PWR_Desc = tk.Label(infoFrame, text=" The average amount of power it takes to send a message between any nodes,", font=("Arial", 10), bg="#654e78")
            lbl_PWR_Desc2 = tk.Label(infoFrame, text=" in Milliamps (mA). This also impact the effort (lifespan)", font=("Arial", 10), bg="#654e78")

            lbl_BTRY_Title = tk.Label(infoFrame, text="Battery Size", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_BTRY_Desc = tk.Label(infoFrame, text=" The total amount of battery life all nodes have, in Milliamps per Hour (mAh)", font=("Arial", 10), bg="#654e78")
            lbl_BTRY_Desc2 = tk.Label(infoFrame, text=" This is how much energy a node has to work with before it dies", font=("Arial", 10), bg="#654e78")

            lbl_RR_Title = tk.Label(infoFrame, text="Recovery rate", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_RR_Desc = tk.Label(infoFrame, text=" The rate that Infected nodes recover and return to being Susceptible nodes,", font=("Arial", 10), bg="#654e78")
            lbl_RR_Desc2 = tk.Label(infoFrame, text=" per Day. A general measure of human intervention to a network attack", font=("Arial", 10), bg="#654e78")

            lbl_T_Title = tk.Label(infoFrame, text="Timesteps", font=("Arial", 10, "bold"), bg="#654e78", fg="white")
            lbl_T_Desc = tk.Label(infoFrame, text=" The number of days to observe the simulation", font=("Arial", 10), bg="#654e78")

            lbl_Title.pack(pady=7)
            infoFrame.place(relwidth=0.98, relheight=1, x=7, y=40)
            lbl_N_Title.grid(row=0, column=0, sticky="e", pady=2)
            lbl_N_Desc.grid(row=0, column=1, sticky="w", pady=2)
            lbl_S_Title.grid(row=1, column=0, sticky="e", pady=2)
            lbl_S_Desc.grid(row=1, column=1, sticky="w", pady=2)
            lbl_IR_Title.grid(row=2, column=0, sticky="e", pady=2)
            lbl_IR_Desc.grid(row=2, column=1, sticky="w", pady=2)
            lbl_IL_Title.grid(row=3, column=0, sticky="e", pady=2)
            lbl_IL_Desc.grid(row=3, column=1, sticky="w", pady=2)
            lbl_IP_Title.grid(row=4, column=0, sticky="e", pady=2)
            lbl_IP_Desc.grid(row=4, column=1, sticky="w", pady=2)
            lbl_WSN_Title.grid(row=5, column=0, sticky="e", pady=2)
            lbl_WSN_Desc.grid(row=5, column=1, sticky="w", pady=2)
            lbl_WSN_Desc2.grid(row=6, column=1, sticky="w", pady=2)
            lbl_DEP_Title.grid(row=7, column=0, sticky="e", pady=2)
            lbl_DEP_Desc.grid(row=7, column=1, sticky="w", pady=2)
            lbl_DEP_Desc2.grid(row=8, column=1, sticky="w", pady=2)
            lbl_TRNS_Title.grid(row=9, column=0, sticky="e", pady=2)
            lbl_TRNS_Desc.grid(row=9, column=1, sticky="w", pady=2)
            lbl_TRNS_Desc2.grid(row=10, column=1, sticky="w", pady=2)
            lbl_CNTCT_Title.grid(row=11, column=0, sticky="e", pady=2)
            lbl_CNTCT_Desc.grid(row=11, column=1, sticky="w", pady=2)
            lbl_CNTCT_Desc2.grid(row=12, column=1, sticky="w", pady=2)
            lbl_SCAN_Title.grid(row=13, column=0, sticky="e", pady=2)
            lbl_SCAN_Desc.grid(row=13, column=1, sticky="w", pady=2)
            lbl_SCAN_Desc2.grid(row=14, column=1, sticky="w", pady=2)
            lbl_PTrns_Title.grid(row=15, column=0, sticky="e", pady=2)
            lbl_PTrns_Desc.grid(row=15, column=1, sticky="w", pady=2)
            lbl_IrPsu_Title.grid(row=14, column=0, sticky="e", pady=2)
            lbl_IrPsu_Desc.grid(row=14, column=1, sticky="w", pady=2)
            lbl_IlPsu_Title.grid(row=15, column=0, sticky="e", pady=2)
            lbl_IlPsu_Desc.grid(row=15, column=1, sticky="w", pady=2)
            lbl_IpPsu_Title.grid(row=16, column=0, sticky="e", pady=2)
            lbl_IpPsu_Desc.grid(row=16, column=1, sticky="w", pady=2)
            lbl_MSG_Title.grid(row=17, column=0, sticky="e", pady=2)
            lbl_MSG_Desc.grid(row=17, column=1, sticky="w", pady=2)
            lbl_MSG_Desc2.grid(row=18, column=1, sticky="w", pady=2)
            lbl_PWR_Title.grid(row=19, column=0, sticky="e", pady=2)
            lbl_PWR_Desc.grid(row=19, column=1, sticky="w", pady=2)
            lbl_PWR_Desc2.grid(row=20, column=1, sticky="w", pady=2)
            lbl_BTRY_Title.grid(row=21, column=0, sticky="e", pady=2)
            lbl_BTRY_Desc.grid(row=21, column=1, sticky="w", pady=2)
            lbl_BTRY_Desc2.grid(row=22, column=1, sticky="w", pady=2)
            lbl_RR_Title.grid(row=23, column=0, sticky="e", pady=2)
            lbl_RR_Desc.grid(row=23, column=1, sticky="w", pady=2)
            lbl_RR_Desc2.grid(row=24, column=1, sticky="w", pady=2)
            lbl_T_Title.grid(row=25, column=0, sticky="e", pady=2)
            lbl_T_Desc.grid(row=25, column=1, sticky="w", pady=2)

        if self.checkModelType() == "SIR":
            # This outputs the _____ model information
            infoFrame = tk.Frame(self.column_left_frame, bg="red")
            lbl_Title = tk.Label(infoFrame, text="OORAH")
            infoFrame.place(relwidth=0.95, relheight=0.9, x=11, y=40)
            lbl_Title.pack()

        if self.checkModelType() == "SIRD":
            pass
