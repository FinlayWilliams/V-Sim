import tkinter as tk
from tkinter import *

class SISInspectInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        btn_Return = tk.Button(self, wraplength=40, width=5, text="Return Home", font=("Arial", 7),
                               command=lambda: controller.display("SISInspectInterface", "HomeInterface"))

        btn_Return.pack()
