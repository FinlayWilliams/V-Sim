import tkinter as tk


class MasterInterface:

    def __init__(self):
        self.frame_1 = tk.Frame()

    def display(self, baseWin, interfaces):
        pass

    def changeFrame(self, newFrame):
        self.frame_1.pack_forget()
        newFrame.frame_1.pack(expand="true", fill="both")