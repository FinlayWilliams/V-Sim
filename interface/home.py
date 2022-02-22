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
        # Page title gui
        titleBgBorder = tk.Frame(frame_left, bg="white")
        titleBgInner = tk.Frame(frame_left, bg="#654e78")
        lblTitle = tk.Label(titleBgInner, text="IoT-SIS Sim:", bg="#654e78",font=("Courier", 30, "underline"),
                            fg="white")
        lblTitle2 = tk.Label(titleBgInner, text="An IoT-SIS Virus model Simulation Tool", bg="#654e78",
                                  font=("Courier", 20), fg="white")

        ####################################### Placing LEFT-side elements #############################################

        frame_left.place(x=0, y=0, height="864", width="718")
        lblTitle.place(x=5, y=2)
        lblTitle2.place(x=5, y=50)
        titleBgBorder.place(x=25, y=23, height="100", width="635")
        titleBgInner.place(x=30, y=28, height="90", width="625")

        ##################################### Instantiating RIGHT-side elements ########################################

        frame_right = tk.Frame(self, bg="#453354")
        column_frame = tk.Frame(frame_right, bg="#a8a8a8")

        lbl_model_list = tk.Label(frame_right, text="Select a Model to Begin ... ", bg="#a8a8a8", font=("Arial", 12))
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
        btn_Delete = tk.Button(frame_right, width=17, text="Delete Model")
        # Button: creates new default SIS model
        btn_New_SIS = tk.Button(frame_right, width=17, text="New SIS Model")
        # Button:
        btn_New_B1 = tk.Button(frame_right, width=17, text="PLACEHOLDER")
        # Button:
        btn_New_B2 = tk.Button(frame_right, width=17, text="PLACEHOLDER")

        # Creating a second listbox of all models to for comparison

        ####################################### Placing RIGHT-side elements ############################################

        frame_right.place(x=717, y=0, height="864", width="819")
        column_frame.place(relheight=1, relwidth=0.7, x=135)

        lbl_model_list.place(x=218, y=20)
        self.lstModels.place(x=220, y=50)
        btn_Configure.place(x=220, y=310)
        btn_Inspect.place(x=358, y=310)
        btn_Delete.place(x=496, y=310)
        btn_New_SIS.place(x=220, y=344)
        btn_New_B1.place(x=358, y=344)
        btn_New_B2.place(x=496, y=344)

    # Method that is called from base whenever the frame is repacked so the list of models is always refreshed on screen
    def updateModelList(self):
        self.lstModels.delete(0, END)
        for M in self.controller.models:
            self.lstModels.insert(END, M)

    # Method that is called everytime a different entry in the listbox is selected, updating the controllers
    # (base windows) current active model and an index variable that is used when saving the models
    def updateActiveModel(self, controller, stub):
        if self.lstModels.curselection() != ():
            controller.setActiveModel(int(''.join(map(str, self.lstModels.curselection()))))
            controller.setActiveModelIndex(int(''.join(map(str, self.lstModels.curselection()))))
