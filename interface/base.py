import tkinter as tk
from tkinter import ttk
from .home import HomeInterface
from .siscontrol import SISControlInterface
from .sisinspect import SISInspectInterface
from model.sis import SIS


class BaseApp(tk.Tk):
    # Initialising the base tk.Tk class and overarching container
    # (setting default sizes, default models, all interfaces)
    def __init__(self):
        super().__init__()
        self.title("V - Sim")
        self.resizable(0, 0)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        center_x = int(self.screen_width / 2 - 1536 / 2)
        center_y = int(self.screen_height / 2 - 864 / 2)
        self.geometry(f"1536x864+{center_x}+{center_y}")
        self.iconbitmap("assets/virus_icon.ico")

        # Creating a base frame interface for all other interfaces to use as the master class
        base = tk.Frame(self, background="#453354")
        base.pack(side="top", fill="both", expand=True)

        # Initialising a model list and a default model
        self.models = []
        self.addDefaultSISModel()
        self.activeModelIndex = 0
        self.activeModel = self.models[self.activeModelIndex]

        # Manually initialising all interfaces and displaying the Home interface
        self.interfaces = {}
        homeInterface = HomeInterface(master=base, controller=self)
        self.interfaces[HomeInterface.__name__] = homeInterface
        sisInspectInterface = SISInspectInterface(master=base, controller=self)
        self.interfaces[SISInspectInterface.__name__] = sisInspectInterface
        sisControlInterface = SISControlInterface(master=base, controller=self)
        self.interfaces[SISControlInterface.__name__] = sisControlInterface

        self.interfaces[HomeInterface.__name__].pack(side="top", fill="both", expand=True)

    # A method to call from any interface to display a custom popup message box for any cause
    def popup(self, title, message):
        popup = tk.Tk()
        popup.wm_title(title)
        popup.configure(bg="#453354")
        center_x = int(self.screen_width / 2 - 400 / 2)
        center_y = int(self.screen_height / 2 - 100 / 2)
        popup.geometry(f"400x100+{center_x}+{center_y}")
        popup.resizable(0, 0)
        lbl_Msg = tk.Label(popup, text=message, bg="#453354", font=("Arial", 10), fg="white")
        lbl_Msg.pack(side="top", fill="x", pady=15, anchor="center")
        btn_Close = tk.Button(popup, text="Okay", command=popup.destroy)
        btn_Close.pack(pady=10)
        popup.iconbitmap("assets/virus_icon.ico")
        popup.mainloop()

    # A method created to display all interfaces from any interface
    def display(self, hide, show):
        self.interfaces[hide].pack_forget()

        if show == "HomeInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            self.interfaces[show].updateModelList()
            self.interfaces[show].updateCompareModelList()
        if show == "SISInspectInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
        if show == "SISControlInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            self.interfaces[show].updateVariables(self)
            self.interfaces[show].updateGraphs()
        if show == "SIRControlInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            # self.interfaces[show].updateVariables(self)
            # self.interfaces[show].updateGraphs()
        if show == "SIRDControlInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            # self.interfaces[show].updateVariables(self)
            # self.interfaces[show].updateGraphs()

    # A range of methods controlling the model list and active model
    def getActiveModelIndex(self): return self.activeModelIndex

    def setActiveModelIndex(self, index): self.activeModelIndex = index

    def getActiveModel(self): return self.activeModel

    def setActiveModel(self, index): self.activeModel = self.models[index]

    def addModel(self, newModel): self.models.append(newModel)

    def addDefaultSISModel(self): self.models.append(SIS("SIS: DefaultModel", 10000, 0.99, 0.01, 10, 50, 10, 1, 27, 0.3, 0.00002, 0.06,
                           0.09, 50, 0.75, 864000, 0.75, 10))

    def removeModel(self, index): self.models.remove(self.models[index])

    def overwriteModel(self, index, model): self.models[index] = model
