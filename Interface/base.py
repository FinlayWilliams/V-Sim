from Interface import master
from Interface import controls
from Interface import home
from Model import model
import tkinter as tk


class BaseInterface(master.MasterInterface):

    # Constructor
    def __init__(self):
        self.newModel = model.Model(10000, 0.99, 0.003, 0.003, 0.004, 10, 50, 10, 1, 27, 0.3, 0.00002, 0.06,
                                       0.09, 50, 0.75, 864000, 0.75, 10)
        self.newModel2 = model.Model(5000, 0.99, 0.003, 0.003, 0.004, 10, 50, 10, 1, 10, 0.3, 0.00002, 0.06,
                                    0.09, 50, 0.75, 864000, 0.75, 10)
        self.modelList = []
        self.modelList.append(self.newModel)
        self.modelList.append(self.newModel2)
        self.interfaces = []
        self.display(1)

    # This method initialises the base window itself as well as the other interfaces
    def display(self, baseWin):
        # Base Interface Settings
        self.base = tk.Tk()
        self.base.title("IoT-SIS Model Simulation")
        screen_width = self.base.winfo_screenwidth()
        screen_height = self.base.winfo_screenheight()
        center_x = int(screen_width / 2 - 1536 / 2)
        center_y = int(screen_height / 2 - 864 / 2)
        self.base.geometry(f"1536x864+{center_x}+{center_y}")
        self.base.resizable(0, 0)
        self.base.configure(background="#453354")
        self.base.attributes("-transparentcolor", "grey")
        self.base.iconbitmap('./assets/virus_icon.ico')

        self.interfaces.append(home.HomeInterface(self.modelList, self.interfaces))
        self.interfaces.append(controls.ControlInterface(self.modelList, self.interfaces, self.modelList[0]))

        for interface in self.interfaces:
            interface.display(self.base)

        self.interfaces[0].frame_1.pack(expand="true", fill="both")

        self.base.mainloop()

