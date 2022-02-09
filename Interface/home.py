from Interface import master
import tkinter as tk


class HomeInterface(master.MasterInterface):

    def display(self, baseWin, interfaces):
        self.frame_1 = tk.Frame(baseWin, bg="black")
        lbl1 = tk.Label(self.frame_1, text="Press this button to get started")
        lbl1.pack()

        btnGo = tk.Button(self.frame_1, text="Press me!", command=lambda: self.changeFrame(interfaces[1]))
        btnGo.pack()
