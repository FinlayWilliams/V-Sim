from Interface import master
import tkinter as tk


class HomeInterface(master.MasterInterface):

    def display(self, baseWin, interfaces):
        self.frame_1 = tk.Frame(baseWin, bg="#453354")

        lblex = tk.Label(self.frame_1, text="Welcome to the IoT-SIS Simulation tool", bg="#453354")
        lblex.pack()

        lblex2 = tk.Label(self.frame_1, text="Here, some basic information about the models variables will be explained:", bg="#453354")
        lblex2.pack()

        lbl1 = tk.Label(self.frame_1, text="Press this button to get started configuring a the model", bg="#453354")
        lbl1.pack()

        btnGo = tk.Button(self.frame_1, text="Press me!", command=lambda: self.changeFrame(interfaces[1]))
        btnGo.pack()
