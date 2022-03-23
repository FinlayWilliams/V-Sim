import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
from models import sir


class SIRControlInterface(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.activeModel = controller.activeModel

        ####################################### Instantiating ALL elements ############################################

        # Upper area for displaying and models option buttons
        frameTop = tk.Frame(self, bg="#453354")
        # Button: Resets models config and refreshes graphs
        btnReset = tk.Button(frameTop, wraplength=40, width=5, text="Reset Model", font=("Arial", 7),
                             relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: [self.updateVariables(controller), self.updateGraphs()])
        # Button: overwrites the current models "saving" it
        btnSave = tk.Button(frameTop, wraplength=40, width=5, text="Save Model", font=("Arial", 7),
                            relief="ridge", fg="white", bg="#6e6e6e",
                             command=lambda: [self.updateModel(1),
                                              controller.overwriteModel(self.activeModelIndex, self.activeModel),
                                              controller.setActiveModel(self.activeModelIndex)])
        # Button: add this models configuration to the list
        btnSaveNew = tk.Button(frameTop, wraplength=40, width=5, text="Save New", font=("Arial", 7), bg="#6e6e6e",
                               relief="ridge", fg="white",
                               command=lambda: [self.updateModel(1), controller.addModel(self.activeModel),
                                                controller.setActiveModel(len(controller.models)-1)])
        # Button: opens the inspect models page with the currently selected models
        btnInspect = tk.Button(frameTop, wraplength=40, width=5, text="Inspect Model", font=("Arial", 7),
                               relief="ridge", fg="white", bg="#6e6e6e",
                               command=lambda: self.checkModelSaved(controller, 1))
        # Button: takes the user to the home page
        btnReturn = tk.Button(frameTop, wraplength=40, width=5, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                             command=lambda: controller.display("SIRControlInterface", "HomeInterface"))

        # This frame holds the graphs
        canvasFrame = tk.Frame(frameTop, bg="#654e78")
        # Frame for the legend to sit in + legend labels
        lblLegendTitle = tk.Label(frameTop, bg="#453354", width=25, pady=4, text="Legend :",
                                    font=("Calibri", 14, "bold"), fg="white")
        lblLegend1 = tk.Label(frameTop, bg="#2ca02c", width=25, pady=4, text="(S) Susceptible",
                               font=("Arial", 12), fg="white")
        lblLegend2 = tk.Label(frameTop, bg="#d62728", width=25, pady=4, text="(I) Infected",
                               font=("Arial", 12), fg="white")
        lblLegend3 = tk.Label(frameTop, bg="#1f77b4", width=25, pady=4, text="(R) Recovered",
                               font=("Arial", 12), fg="white")

        # Separates graphs from the controls
        frameMid = tk.Frame(self, bg="#6e6e6e")
        lblOptions = tk.Label(frameMid, text="Model Variables", bg="#6e6e6e", font=("Arial", 10), fg="white")

        # Lower area for the controls
        frameBot = tk.Frame(self, bg="#a8a8a8")
        # All labels and widgets for inputting variables
        lblModelName = tk.Label(frameBot, text="Model Name:", bg="#a8a8a8", font=("Arial", 10))
        self.entryName = tk.Entry(frameBot)
        lblN = tk.Label(frameBot, text="Initial Node Population Size (N):")
        NOptions = ["1000", "2000", "5000", "10000", "20000", "50000", "100000"]
        self.cmbN = ttk.Combobox(frameBot, values=NOptions, state="readonly")
        lblS = tk.Label(frameBot, text="Initial S Size (% of N):")
        self.sclS = tk.Scale(frameBot, from_=0, to=100, resolution=1, orient="horizontal")
        lblI = tk.Label(frameBot, text="Initial I Size (% of N):")
        self.lblIMatch = tk.Label(frameBot, bg="white", bd=3)
        lblBeta = tk.Label(frameBot, text="Beta:")
        self.sclBeta = tk.Scale(frameBot, from_=0.01, to=1, resolution=0.01, orient="horizontal")
        lblGamma = tk.Label(frameBot, text="Gamma:")
        self.sclGamma = tk.Scale(frameBot, from_=0.001, to=1, resolution=0.001, orient="horizontal")
        lblT = tk.Label(frameBot, text="Days to Observe:")
        self.sclT = tk.Scale(frameBot, from_=1, to=365, resolution=1, orient="horizontal")

        ####################################### Placing ALL elements ############################################

        ## Frame Top Half
        frameTop.place(relheight=0.70, relwidth=1)
        btnReturn.place(x=10, y=13)
        btnInspect.place(x=10, y=64)
        btnReset.place(x=10, y=458)
        btnSave.place(x=10, y=509)
        btnSaveNew.place(x=10, y=560)
        canvasFrame.place(relheight=1, relwidth=0.73, x=58)
        lblLegendTitle.place(x=1229, y=194)
        lblLegend1.place(x=1243, y=227)
        lblLegend2.place(x=1243, y=260)
        lblLegend3.place(x=1243, y=293)
        ## Frame Mid
        frameMid.place(y=605, relheight=0.05, relwidth=1)
        lblOptions.pack()
        ## Frame Bottom Half
        frameBot.place(y=628, relheight=0.30, relwidth=1)
        # 1st Block
        lblModelName.grid(row=0, column=0, padx=30, sticky="w")
        self.entryName.grid(row=1, column=0, padx=30, sticky="nw")
        # 2nd Block
        lblN.grid(row=0, column=1, padx=(10, 5), pady=(7, 0), sticky="e")
        self.cmbN.grid(row=0, column=2, padx=5, pady=(7, 0))
        self.cmbN.bind("<<ComboboxSelected>>", self.updateModel)
        lblS.grid(row=1, column=1, padx=(10, 5), pady=5, sticky="e")
        self.sclS.grid(row=1, column=2, padx=5, sticky="ew")
        self.sclS.bind("<ButtonRelease-1>", self.updateModel)
        lblI.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="e")
        self.lblIMatch.grid(row=2, column=2, padx=5, sticky="ew")
        # 3rd Block
        lblBeta.grid(row=0, column=5, padx=5, pady=(7, 0), sticky="e")
        self.sclBeta.grid(row=0, column=6, padx=5, pady=(7, 0))
        self.sclBeta.bind("<ButtonRelease-1>", self.updateModel)
        lblGamma.grid(row=1, column=5, padx=5, pady=5, sticky="e")
        self.sclGamma.grid(row=1, column=6, padx=5, sticky="ew")
        self.sclGamma.bind("<ButtonRelease-1>", self.updateModel)
        lblT.grid(row=4, column=7, padx=5, pady=5, sticky="e")
        self.sclT.grid(row=4, column=8, padx=5, sticky="ew")
        self.sclT.bind("<ButtonRelease-1>", self.updateModel)

        # Calling the method to allign the variables and populate all fields
        self.updateVariables(controller)

        # Setting up the canvas area for the graphs in frameTop
        figure = plt.figure(facecolor="#654e78")
        self.canvas = FigureCanvasTkAgg(figure, canvasFrame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = [figure.add_subplot(2, 1, x + 1, facecolor="#453354") for x in range(2)]
        for x in range(1):
            self.ax[x].ticklabel_format(style="plain")
        figure.tight_layout(rect=[0.01, 0.03, 1, 0.95], h_pad=3)

    # Method to update the onscreen graphs to whatever the current models configuration is
    def updateGraphs(self):
        S1, I1, R1 = self.activeModel.runModel()
        T1 = np.linspace(0, self.activeModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(1)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, I1, "#d62728", label="Infected")
        self.ax[0].plot(T1, R1, "#1f77b4", label="Recovered")
        self.ax[0].set_xlabel("Timesteps (Days)")
        self.ax[0].set_ylabel("Population Count")
        self.ax[0].set_title("Population Sizes Over Time - S, I, R")

        self.canvas.draw()

    # Called when a value option is changed, to automatically update the active models parameters
    def updateModel(self, Stub):
        if len(self.entryName.get()) == 0:
            self.controller.popup("Invalid Save", "Please enter a name for the models!")
        if len(self.entryName.get()) > 24:
            self.controller.popup("Invalid Save", "Please enter a shorter name for the models!")
        else:
            Name = str("SIR: " + self.entryName.get())
            N = int(self.cmbN.get())
            S = float(self.sclS.get() / 100)
            I = float((100 - self.sclS.get()) / 100)
            Beta = float(self.sclBeta.get())
            Gamma = float(self.sclGamma.get())
            T = int(self.sclT.get())

            newActiveModel = sir.SIR(Name, N, S, I, Beta, Gamma, T)

            self.lblIMatch.config(text="{:.0f}".format(I*100))

            self.activeModel = newActiveModel
            self.updateGraphs()

    # Called once when this interfaces is created + everytime this interfaces is opened to ensure all variables
    # are updated and correct
    def updateVariables(self, controller):
        self.activeModel = controller.activeModel
        self.activeModelIndex = controller.activeModelIndex

        self.cmbN.set(self.activeModel.N)
        self.sclS.set(self.activeModel.percentS * 100)
        self.lblIMatch.config(text="{:.0f}".format(self.activeModel.percentI * 100))
        self.sclBeta.set(self.activeModel.Beta)
        self.sclGamma.set(self.activeModel.Gamma)
        self.entryName.delete(0, 'end')
        self.entryName.insert(END, self.activeModel.Name[5:])
        self.sclT.set(self.activeModel.Timesteps)

    # Checks whether the models is saved or not before the user proceeds to the inspect screen and looses
    # the current configuration
    def checkModelSaved(self, controller, stub):
        if self.activeModel != controller.activeModel:
            self.controller.popup("Warning", "Current models configuration not saved")
        else:
            controller.display("SIRControlInterface", "SIRInspectInterface")

    # Checks if the current configuration is valid by checking no population size dips below zero
    def checkValid(self, newActiveModel):
        S1, I1, R1 = newActiveModel.runModel()
        populations = [S1, I1, R1]
        for P in populations:
            for value in P:
                if value < 0:
                    return False
        return True
