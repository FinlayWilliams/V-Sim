import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class SIRCompareInterface(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.setModels(controller)

        ###################################### Instantiating MIDDLE elements ###########################################
        titleFrame = tk.Frame(self, bg="#453354")
        lblTitle = tk.Label(titleFrame, bg="#453354", text="SIR Virus Model Comparison", font=("Arial", 15, "italic"),
                            fg="white")
        btnReturn = tk.Button(titleFrame, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: controller.display("SIRCompareInterface", "HomeInterface"))
        nameFrame = tk.Frame(self, bg="#574b59")

        legendFrame = tk.Frame(nameFrame, bg="#574b59")
        lblG = tk.Label(legendFrame, text="Green", fg="#2d802f", bg="#574b59", font=("Arial", 9, "bold"))
        lblGEx = tk.Label(legendFrame, text=" Indicates a Lower & Better Score", bg="#574b59", fg="white",
                          font=("Arial", 8))
        lblO = tk.Label(legendFrame, text="Orange", fg="#e68f39", bg="#574b59", font=("Arial", 9, "bold"))
        lblOEx = tk.Label(legendFrame, text="Indicates an Identical Score", bg="#574b59", fg="white", font=("Arial", 8))
        lblR = tk.Label(legendFrame, text="Red", fg="#d12c3f", bg="#574b59", font=("Arial", 9, "bold"))
        lblREx = tk.Label(legendFrame, text="Indicates a Higher & Worse Score", bg="#574b59", fg="white",
                          font=("Arial", 8))

        self.informationFrame = tk.Frame(self, bg="#e0e0e0")

        ##################################### Instantiating LEFT-side elements #########################################
        self.lblLeftName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblLeftScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 16))
        btnConfigureLeft = tk.Button(nameFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                     command=lambda: controller.display("SIRCompareInterface", "SIRControlInterface"))
        btnInspectLeft = tk.Button(nameFrame, wraplength=41, width=7, text="Inspect Model", font=("Arial", 7),
                                   command=lambda: controller.display("SIRCompareInterface", "SIRInspectInterface"))

        leftFrame = tk.Frame(self, bg="#453354")
        leftGraphFrame = tk.Frame(leftFrame, bg="#654e78")

        figureLeft = plt.figure(facecolor="#654e78")
        self.canvasLeft = FigureCanvasTkAgg(figureLeft, leftGraphFrame)
        self.canvasLeft.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.axLeft = [figureLeft.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(2):
            self.axLeft[x].ticklabel_format(style="plain")
        figureLeft.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.updateLeftGraph()

        ##################################### Instantiating RIGHT-side elements ########################################
        self.lblRightName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblRightScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 16))
        btnConfigureRight = tk.Button(nameFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                      command=lambda: [self.setNewActivePlusIndex(controller),
                                                    controller.display("SIRCompareInterface", "SIRControlInterface")])
        btnInspectRight = tk.Button(nameFrame, wraplength=41, width=7, text="Inspect Model", font=("Arial", 7),
                                      command=lambda: [self.setNewActivePlusIndex(controller),
                                                    controller.display("SIRCompareInterface", "SIRInspectInterface")])

        rightFrame = tk.Frame(self, bg="#453354")
        rightGraphFrame = tk.Frame(rightFrame, bg="#654e78")

        figureRight = plt.figure(facecolor="#654e78")
        self.canvasRight = FigureCanvasTkAgg(figureRight, rightGraphFrame)
        self.canvasRight.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.axRight = [figureRight.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(2):
            self.axRight[x].ticklabel_format(style="plain")
        figureRight.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.updateRightGraph()

        ######################################### Placing MIDDLE elements ##############################################
        titleFrame.place(relwidth=1, relheight=0.07)
        lblTitle.pack(pady=15)
        nameFrame.place(relwidth=1, relheight=0.08, y=60)
        btnReturn.place(x=14, y=14)
        legendFrame.place(x=657, y=3)
        lblG.grid(row=0, column=0)
        lblGEx.grid(row=0, column=1)
        lblO.grid(row=1, column=0)
        lblOEx.grid(row=1, column=1)
        lblR.grid(row=2, column=0)
        lblREx.grid(row=2, column=1)
        self.informationFrame.place(relwidth=0.334, relheight=0.93, y=130, x=511)

        ####################################### Placing LEFT-side elements #############################################
        btnInspectLeft.pack(side="left", padx=14)
        btnConfigureLeft.pack(side="left", padx=7)
        self.lblLeftName.pack(side="left", padx=10)
        self.lblLeftScore.pack(side="left")
        leftFrame.place(relwidth=0.333, relheight=0.93, y=126, x=0)
        leftGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)

        ####################################### Placing RIGHT-side elements ############################################
        btnInspectRight.pack(side="right", padx=14)
        btnConfigureRight.pack(side="right", padx=7)
        self.lblRightName.pack(side="right", padx=10)
        self.lblRightScore.pack(side="right")
        rightFrame.place(relwidth=0.333, relheight=0.93, y=126, x=1025)
        rightGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)

    # Called upon page opening to set the correct models
    def setModels(self, controller):
        self.activeModel = controller.activeModel
        self.compareModel = controller.compareModel

    # Called when opting to configure the Right, CompareModel to ensure compatibility
    def setNewActivePlusIndex(self, controller):
        index = 0
        for M in controller.models:
            if M == self.compareModel:
                controller.setActiveModel(index)
                controller.setActiveModelIndex(index)
            index = index + 1

    # Called on page opening to update the Left, ActiveModel graph information
    def updateLeftGraph(self):
        S1, I1, R1 = self.activeModel.runModel()
        T1 = np.linspace(0, self.activeModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axLeft[x].clear() for x in range(2)]

        # Plotting the first graph
        self.axLeft[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.axLeft[0].plot(T1, I1, "#d62728", label="Infected")
        self.axLeft[0].plot(T1, R1, "#1f77b4", label="Recovered")
        self.axLeft[0].set_xlabel("Timesteps (Days)")
        self.axLeft[0].set_ylabel("Population Count")
        self.axLeft[0].set_title("Population Sizes Over Time - S, I, R")
        # Plotting the second graph
        pop = [S1[len(S1) - 1], I1[len(I1) - 1], R1[len(R1) - 1]]
        explode = (0.1, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Infected: {:.0f}".format(pop[1]),
                  "Recovered: {:.0f}".format(pop[2])]
        colours = ["#2ca02c", "#d62728", "#1f77b4"]
        self.axLeft[1].pie(pop, explode=explode, labels=labels, colors=colours)
        self.axLeft[1].set_title("Population Sizes on Final Recorded Day #{}".format(self.controller.activeModel.Timesteps))

        self.canvasLeft.draw()

    # Called on page opening to update the Right, CompareModel graph information
    def updateRightGraph(self):
        S1, I1, R1 = self.compareModel.runModel()
        T1 = np.linspace(0, self.compareModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axRight[x].clear() for x in range(2)]

        # Plotting the first graph
        self.axRight[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.axRight[0].plot(T1, I1, "#d62728", label="Infected")
        self.axRight[0].plot(T1, R1, "#1f77b4", label="Recovered")
        self.axRight[0].set_xlabel("Timesteps (Days)")
        self.axRight[0].set_ylabel("Population Count")
        self.axRight[0].set_title("Population Sizes Over Time - S, I, R")
        # Plotting the second graph
        pop = [S1[len(S1) - 1], I1[len(I1) - 1], R1[len(R1) - 1]]
        explode = (0.1, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Infected: {:.0f}".format(pop[1]),
                  "Recovered: {:.0f}".format(pop[2])]
        colours = ["#2ca02c", "#d62728", "#1f77b4"]
        self.axRight[1].pie(pop, explode=explode, labels=labels, colors=colours)
        self.axRight[1].set_title(
            "Population Sizes on Final Recorded Day #{}".format(self.controller.compareModel.Timesteps))

        self.canvasLeft.draw()

    # Called on page opening to set the correct information
    def updateColumnInfo(self):
        pass
