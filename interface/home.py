import tkinter as tk
from tkinter import *


class HomeInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        ## Left frame initialisation
        frame_left = tk.Frame(self, bg="red")
        # The page title gui
        titleBgBorder = tk.Frame(frame_left, bg="white")
        titleBgInner = tk.Frame(frame_left, bg="#453354")
        lblTitle = tk.Label(titleBgInner, text="IoT-SIS Sim:", bg="#453354",font=("Courier", 30, "underline"), fg="white")
        lblTitle2 = tk.Label(titleBgInner, text="An IoT-SIS Virus model Simulation Tool", bg="#453354",
                                  font=("Courier", 20), fg="white")

        # Left frame placement
        frame_left.place(x=0, y=0, height="864", width="718")
        # The page title gui
        lblTitle.place(x=5, y=2)
        lblTitle2.place(x=5, y=50)
        titleBgBorder.place(x=25, y=23, height="100", width="635")
        titleBgInner.place(x=30, y=28, height="90", width="625")

        ## Right frame initialisation
        frame_right = tk.Frame(self, bg="blue")
        # Creating the listbox where the list of all saved models will appear
        self.lstModels = tk.Listbox(frame_right, height=5, width=40, bg="yellow", font=("Calibri", 15))
        self.updateModelList()
        self.lstModels.bind("<<ListboxSelect>>",
                            lambda x: self.updateActiveModel(controller, 1))

        btnConfig = tk.Button(frame_right, text="Configure Selected model",
                              command=lambda: [controller.display("HomeInterface", "ControlInterface")])

        # Right frame placement
        frame_right.place(x=717, y=0, height="864", width="818")

        self.lstModels.pack()

        btnConfig.place(x=650, y=800)

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
