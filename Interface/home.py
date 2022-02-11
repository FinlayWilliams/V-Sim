from Interface import master
from Model import model
import tkinter as tk
import tkinter.font as tkFont


class HomeInterface(master.MasterInterface):

    def __init__(self, modelList, interfaces):
        self.modelList = modelList
        self.interfaces = interfaces

    def troubleshoot(self):
        print(self.listy.curselection())

    def display(self, baseWin):
        self.frame_1 = tk.Frame(baseWin, bg="#453354")

        # Left frame initialisation
        self.frame_left = tk.Frame(self.frame_1, bg="red")

        self.titleBgBorder = tk.Frame(self.frame_left, bg="white")
        self.titleBgInner = tk.Frame(self.frame_left, bg="#453354")
        self.lblTitle = tk.Label(self.titleBgInner, text="IoT-SIS Sim:", bg="#453354", font=("Courier", 30, "underline"),
                                 fg="white")
        self.lblTitle2 = tk.Label(self.titleBgInner, text="An IoT-SIS Virus Model Simulation Tool", bg="#453354",
                                  font=("Courier", 20), fg="white")

        # Left frame placement
        self.frame_left.place(x=0, y=0, height="864", width="718")

        self.lblTitle.place(x=5, y=2)
        self.lblTitle2.place(x=5, y=50)
        self.titleBgBorder.place(x=25, y=23, height="100", width="635")
        self.titleBgInner.place(x=30, y=28, height="90", width="625")

        # Right frame initialisation
        self.frame_right = tk.Frame(self.frame_1, bg="blue")

        self.listy = tk.Listbox(self.frame_right)
        self.listy.insert(1, self.modelList[0])
        self.listy.insert(2, self.modelList[1])
        self.listy.bind("<<ListboxSelect>>", self.troubleshoot)

        self.btnConfig = tk.Button(self.frame_right, text="Configure Selected Model",
                                   command=lambda: self.changeFrame(self.interfaces[1]))

        # Right frame placement
        self.frame_right.place(x=717, y=0, height="864", width="818")

        self.listy.pack()






        self.btnConfig.place(x=650, y=800)

