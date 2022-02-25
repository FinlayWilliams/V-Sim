import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

class SISInspectInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        #################################### Instantiating Information Frame ########################################

        frameLeft = tk.Frame(self, bg="#453354")

        btnConfigure = tk.Button(frameLeft, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                 command=lambda: controller.display("SISInspectInterface", "SISControlInterface"))
        btnReturn = tk.Button(frameLeft, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                               command=lambda: controller.display("SISInspectInterface", "HomeInterface"))

        ####################################### Placing Information Frame ###########################################

        frameLeft.place(relheight=1, relwidth=0.6)
        btnConfigure.pack()
        btnReturn.pack()

        ########################################## Instantiating Graphs #############################################

        graphFrame = tk.Frame(self, bg="#654e78")

        figure = plt.figure(facecolor="#654e78")
        self.canvas = FigureCanvasTkAgg(figure, graphFrame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.ax = [figure.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(3):
            self.ax[x].ticklabel_format(style="plain")
        figure.tight_layout(pad=2)

        ############################################# Placing Graphs ################################################

        graphFrame.place(x=922, y=0, relheight=1, relwidth=0.4)
        self.updateGraphs()

    def updateGraphs(self):
        S1, Ir1, Il1, Ip1 = self.controller.activeModel.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.controller.activeModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(3)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
        self.ax[0].plot(T1, Il1, "#1f77b4", label="Local Scanning Infected")
        self.ax[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
        self.ax[0].set_xlabel("Timesteps (Days)")
        self.ax[0].set_ylabel("Node Count")
        self.ax[0].set_title("Node Population Sizes Over Time - S, IR, IL, IP")
        # Plotting the second graph
        self.ax[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.ax[1].plot(T1, I1, '#d62728', label="All Infected")
        self.ax[1].set_xlabel("Timesteps (Days)")
        self.ax[1].set_ylabel("Node Count")
        self.ax[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        # Plotting the third graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning Infected: {:.0f}".format(pop[1]),
                  "Local Scanning Infected: {:.0f}".format(pop[2]), "Peer-to-Peer Infected: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
        self.ax[2].pie(pop, explode=explode, labels=labels, colors=colours)
        self.ax[2].set_title("Population Sizes on Final Recorded Day #{}".format(self.controller.activeModel.Timesteps))

        self.canvas.draw()
