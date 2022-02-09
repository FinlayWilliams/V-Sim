from Interface import master
from Interface import controls
from Interface import home
from Model import model
import tkinter as tk


class BaseInterface(master.MasterInterface):

    # Constructor
    def __init__(self):
        self.activeModel = model.Model(10000, 0.99, 0.003, 0.003, 0.004, 10, 50 * 50, 10, 1, 27, 0.3, 0.00002, 0.06, 0.09, 50, 0.75, 864000, 0.75, 100)
        self.modelList = []
        self.interfaces = []
        self.display(1, self.interfaces)

    # This method initialises the base window itself
    def display(self, baseWin, interfaces):
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

        # self.otherInterface = home.HomeInterface()
        # self.otherInterface.display(self.base)
        # self.btn2 = tk.Button(self.otherInterface.frame_1, text="BAZINGA", command=self.displayControls)
        #
        # self.currentInterface = controls.ControlInterface()
        # self.currentInterface.display(self.base)
        # self.btn1 = tk.Button(self.currentInterface.frame_1, text="hi", command=self.displayHome)
        # self.btn1.pack()
        #
        # self.displayControls()

        interfaces.append(home.HomeInterface())
        interfaces.append(controls.ControlInterface())

        for interface in interfaces:
            interface.display(self.base, interfaces)

        self.interfaces[0].frame_1.pack(expand="true", fill="both")

        self.base.mainloop()


    # def displayControls(self):
    #     self.otherInterface.frame_1.pack_forget()
    #     self.btn2.pack_forget()
    #
    #     self.btn1.pack()
    #     self.currentInterface.frame_1.pack(expand="true", fill="both")
    #
    # def displayHome(self):
    #     self.currentInterface.frame_1.pack_forget()
    #     self.btn1.pack_forget()
    #
    #     self.btn2.pack()
    #     self.otherInterface.frame_1.pack(expand="true", fill="both")
