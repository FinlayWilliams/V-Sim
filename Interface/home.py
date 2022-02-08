import tkinter as tk

class HomeInterface:

    def display(self, base):
        self.frame_1 = tk.Frame(base, bg="black")
        #self.frame_1.place(relheight=1, relwidth=1)
        lbl1 = tk.Label(self.frame_1, text="ligma")
        lbl1.pack()
