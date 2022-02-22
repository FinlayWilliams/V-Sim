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
        frame_left = tk.Frame(self, bg="#453354")
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
        column_left_border.place(relheight=0.86, relwidth=0.72, x=83, y=123)
        self.column_left_frame.place(relheight=0.86, relwidth=0.7, x=90, y=123)
        lblTitle.place(x=5, y=2)
        lblTitle2.place(x=5, y=50)
        titleBgBorder.place(x=25, y=23, height="100", width="635")
        titleBgInner.place(x=30, y=28, height="90", width="625")
        self.setModelInfo()

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
        btn_Configure.place(x=220, y=310)
        btn_Inspect.place(x=358, y=310)
        btn_Delete.place(x=496, y=310)
        btn_New_SIS.place(x=220, y=344)
        btn_New_B1.place(x=358, y=344)
        btn_New_B2.place(x=496, y=344)

        lbl_compare_model_list.place(x=218, y=420)
        self.lstCompareModels.place(x=220, y=450)
        btn_Compare.place(x=220, y=710)

    # Method: Called whenever a model is selected to display the correct model information
    def setModelInfo(self):
        validate = 0

        if validate == 0:
            # This outputs the SIS model Information
            infoFrame = tk.Frame(self.column_left_frame, bg="blue")
            lblTitle = tk.Label(infoFrame, text="Heya")
            infoFrame.place(relwidth=0.95, relheight=0.9, x=5, y=10)
            lblTitle.pack()

        if validate ==1:
            # This outputs the _____ model information
            infoFrame = tk.Frame(self.column_left_frame, bg="red")
            lblTitle = tk.Label(infoFrame, text="OORAH")
            infoFrame.place(relwidth=0.95, relheight=0.9, x=5, y=10)
            lblTitle.pack()

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

    # Method: called everytime a different entry in the listbox is selected, updating the controllers
    # (base windows) current active model and an index variable that is used when saving the models
    def updateActiveModel(self, controller, stub):
        if self.lstModels.curselection() != ():
            # Long prefixes to take the listbox index and obtain a single integer to be used to
            # index with the controller
            controller.setActiveModel(int(''.join(map(str, self.lstModels.curselection()))))
            controller.setActiveModelIndex(int(''.join(map(str, self.lstModels.curselection()))))

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
