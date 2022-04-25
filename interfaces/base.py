import tkinter as tk
from .home import HomeInterface
from .siscompare import SISCompareInterface
from .siscontrol import SISControlInterface
from .sisinspect import SISInspectInterface
from models.sis import SIS


class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialising base class and overarching container (setting default sizes, default models, all interfaces)
        self.title("V-Sim")
        self.resizable(0, 0)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        center_x = int(self.screen_width / 2 - 1920 / 2) #1536
        center_y = int(self.screen_height / 2 - 1080 / 2) #864
        self.geometry(f"1920x1080+{center_x - 7}+{center_y}")
        self.iconbitmap("assets/virus_icon.ico")

        # Creating a base frame interfaces for all other interfaces to use as the master class
        base = tk.Frame(self, background="#453354")
        base.pack(side="top", fill="both", expand=True)

        # Initialising a models list and all default configurations
        self.configurations = []
        self.configurations.append(SIS("IoT-SIS: Default Configuration",    1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8, 50, 0.75, 864000, 0.5, 12, False))
        self.configurations.append(SIS("IoT-SIS: IDS On",                   1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8, 50, 0.75, 864000, 0.5, 12, True))
        self.configurations.append(SIS("IoT-SIS: Large Population",        10000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8, 50, 0.75, 864000, 0.5, 12, False))
        self.configurations.append(SIS("IoT-SIS: Local Biased Propagation", 1000, 1, 1,  50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8, 50, 0.75, 864000, 0.5, 12, False))
        self.configurations.append(SIS("IoT-SIS: P2P Biased Propagation",   1000, 1, 10, 25, 15, 10, 27, 0.01, 0.02, 0.1, 0.95, 50, 0.75, 864000, 0.5, 12, False))
        self.configurations.append(SIS("IoT-SIS: High Node Death Rate",     1000, 1, 50, 150, 1, 250, 27, 0.01, 0.02, 0.1, 0.8, 150, 1.25, 216000, 0.5, 12, False))
        self.configurations.append(SIS("IoT-SIS: High Infected Node Death Rate", 1000, 1, 50, 150, 1, 10, 250, 0.01, 0.005, 0.05, 0.45, 150, 1.25, 216000, 0.5, 12, False))
        self.activeConfigurationIndex = 0
        self.activeConfiguration = self.configurations[self.activeConfigurationIndex]
        self.compareConfiguration = SIS("IoT-SIS: Comparison Configuration", 1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8, 50, 0.75, 864000, 0.5, 12, False)

        # Manually initialising all interfaces and displaying the Home interfaces
        self.interfaces = {}
        homeInterface = HomeInterface(master=base, controller=self)
        self.interfaces[HomeInterface.__name__] = homeInterface
        sisInspectInterface = SISInspectInterface(master=base, controller=self)
        self.interfaces[SISInspectInterface.__name__] = sisInspectInterface
        sisControlInterface = SISControlInterface(master=base, controller=self)
        self.interfaces[SISControlInterface.__name__] = sisControlInterface
        sisCompareInterface = SISCompareInterface(master=base, controller=self)
        self.interfaces[SISCompareInterface.__name__] = sisCompareInterface
        self.interfaces[HomeInterface.__name__].pack(side="top", fill="both", expand=True)

    # Callable from any interface to display a custom popup message box for any cause
    def popup(self, title, message):
        popup = tk.Tk()
        popup.wm_title(title)
        popup.configure(bg="#453354")
        center_x = int(self.screen_width / 2 - 400 / 2)
        center_y = int(self.screen_height / 2 - 120 / 2)
        popup.geometry(f"400x120+{center_x}+{center_y}")
        popup.resizable(0, 0)
        lbl_Msg = tk.Label(popup, text=message, bg="#453354", font=("Arial", 10), fg="white", wraplength=400)
        lbl_Msg.pack(side="top", fill="x", pady=15, anchor="center")
        btn_Close = tk.Button(popup, text="Okay", command=popup.destroy)
        btn_Close.pack(pady=10)
        popup.iconbitmap("assets/virus_icon.ico")
        popup.mainloop()

    # Callable from any interface to switch to another, also calls other methods to set up the page
    def display(self, hide, show):
        self.interfaces[hide].pack_forget()
        if show == "HomeInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            self.interfaces[show].updateConfigurationList()
            self.interfaces[show].updateCompareConfigurationList(self)
        if show == "SISInspectInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            self.interfaces[show].updateGraphs()
            self.interfaces[show].populateFrames()
            self.interfaces[show].switchInfoFrame(0, 1)
        if show == "SISControlInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            self.interfaces[show].updateVariables(self)
            self.interfaces[show].updateGraphs(self.activeConfiguration)
        if show == "SISCompareInterface":
            self.interfaces[show].pack(side="top", fill="both", expand=True)
            self.interfaces[show].setConfigurations(self)
            self.interfaces[show].updateLeftGraph()
            self.interfaces[show].updateRightGraph()
            self.interfaces[show].updateColumnInfo()

    def setActiveConfiguration(self, index):
        self.activeConfiguration = self.configurations[index]

    def setActiveConfigurationIndex(self, index):
        self.activeConfigurationIndex = index

    def addConfiguration(self, newConfig):
        self.configurations.append(newConfig)

    def removeConfiguration(self, index):
        self.configurations.remove(self.configurations[index])

    def overwriteConfiguration(self, index, model):
        self.configurations[index] = model

    def setCompareConfiguration(self, model):
        self.compareConfiguration = model

    def addDefaultSISConfiguration(self):
        self.configurations.append(SIS("IoT-SIS: Default Configuration", 1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8, 50, 0.75, 864000, 0.5, 12, False))
