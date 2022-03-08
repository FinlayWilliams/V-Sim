import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class SISCompareInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.setModels(controller)

        titleFrame = tk.Frame(self, bg="#453354")
        lblTitle = tk.Label(titleFrame, bg="#453354", text="SIS Virus Model Comparison", font=("Arial", 15, "italic"), fg="white")
        btnReturn = tk.Button(titleFrame, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: controller.display("SISCompareInterface", "HomeInterface"))
        nameFrameLeft = tk.Frame(self, bg="#6e6e6e")
        self.lblLeftName = tk.Label(nameFrameLeft, bg="#6e6e6e", font=("Arial", 14), fg="white")
        self.lblLeftScore = tk.Label(nameFrameLeft, bg="#6e6e6e", font=("Arial", 14))
        btnConfigureLeft = tk.Button(nameFrameLeft, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                     command=lambda: controller.display("SISCompareInterface", "SISControlInterface"))
        nameFrameRight = tk.Frame(self, bg="#6e6e6e")
        self.lblRightName = tk.Label(nameFrameRight, bg="#6e6e6e", font=("Arial", 14), fg="white")
        self.lblRightScore = tk.Label(nameFrameRight, bg="#6e6e6e", font=("Arial", 14))
        btnConfigureRight = tk.Button(nameFrameRight, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                     command=lambda: [self.setNewActivePlusIndex(controller), controller.display("SISCompareInterface", "SISControlInterface")])
        leftFrame = tk.Frame(self, bg="#453354")
        leftGraphFrame = tk.Frame(leftFrame, bg="#654e78")
        rightFrame = tk.Frame(self, bg="#453354")
        rightGraphFrame = tk.Frame(rightFrame, bg="#654e78")
        self.informationFrame = tk.Frame(self, bg="#e0e0e0")

        figureLeft = plt.figure(facecolor="#654e78")
        self.canvasLeft = FigureCanvasTkAgg(figureLeft, leftGraphFrame)
        self.canvasLeft.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.axLeft = [figureLeft.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(3):
            self.axLeft[x].ticklabel_format(style="plain")
        figureLeft.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.updateLeftGraph()

        figureRight = plt.figure(facecolor="#654e78")
        self.canvasRight = FigureCanvasTkAgg(figureRight, rightGraphFrame)
        self.canvasRight.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.axRight = [figureRight.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(3):
            self.axRight[x].ticklabel_format(style="plain")
        figureRight.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.updateRightGraph()

        titleFrame.place(relwidth=1, relheight=0.07)
        lblTitle.pack(pady=15)
        btnReturn.place(x=14, y=14)
        nameFrameLeft.place(relwidth=0.5, relheight=0.07, y=60)
        btnConfigureLeft.pack(side="left", padx=14)
        self.lblLeftName.pack(side="left", padx=10)
        self.lblLeftScore.pack(side="left", padx=10)
        nameFrameRight.place(relwidth=0.5, relheight=0.07, y=60, x=768)
        btnConfigureRight.pack(side="right", padx=14)
        self.lblRightName.pack(side="right", padx=10)
        self.lblRightScore.pack(side="right", padx=10)
        leftFrame.place(relwidth=0.333, relheight=0.93, y=120, x=0)
        leftGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)
        rightFrame.place(relwidth=0.333, relheight=0.93, y=120, x=1025)
        rightGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)
        self.informationFrame.place(relwidth=0.334, relheight=0.93, y=120, x=511)

    def setModels(self, controller):
        self.activeModel = controller.activeModel
        self.compareModel = controller.compareModel

    def setNewActivePlusIndex(self, controller):
        index = 0
        for M in controller.models:
            if M == self.compareModel:
                controller.setActiveModel(index)
                controller.setActiveModelIndex(index)
            index = index + 1

    def updateColumnInfo(self):
        self.lblLeftName.config(text="{}   -".format(self.activeModel.Name))
        self.lblRightName.config(text="-   {}".format(self.compareModel.Name))

        activeScore = self.activeModel.calculateScores()[8]
        compareScore = self.compareModel.calculateScores()[8]

        if activeScore < compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#2d802f")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#b81d28")
        if activeScore > compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#b81d28")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#2d802f")
        if activeScore == compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#e68f39")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#e68f39")

    def updateLeftGraph(self):
        S1, Ir1, Il1, Ip1 = self.activeModel.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.activeModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axLeft[x].clear() for x in range(3)]

        # Plotting the first graph
        self.axLeft[0].plot(T1, S1, "#2ca02c", label="Susceptible: ")
        self.axLeft[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning")
        self.axLeft[0].plot(T1, Il1, "#1f77b4", label="Local-Scanning")
        self.axLeft[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer")
        self.axLeft[0].set_xlabel("Timesteps (Days)")
        self.axLeft[0].set_ylabel("Node Count")
        self.axLeft[0].set_title("Node Population Sizes Over Time - S, IR, IL, IP")
        # Plotting the second graph
        self.axLeft[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.axLeft[1].plot(T1, I1, '#d62728', label="All Infected")
        self.axLeft[1].set_xlabel("Timesteps (Days)")
        self.axLeft[1].set_ylabel("Node Count")
        self.axLeft[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        # Plotting the third graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning: {:.0f}".format(pop[1]),
                  "Local-Scanning: {:.0f}".format(pop[2]), "Peer-to-Peer: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
        self.axLeft[2].pie(pop, explode=explode, labels=labels, colors=colours)
        self.axLeft[2].set_title("Population Sizes on Final Recorded Day #{}".format(self.activeModel.Timesteps))

        self.canvasLeft.draw()

    def updateRightGraph(self):
        S1, Ir1, Il1, Ip1 = self.compareModel.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.compareModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axRight[x].clear() for x in range(3)]

        # Plotting the first graph
        self.axRight[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.axRight[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning")
        self.axRight[0].plot(T1, Il1, "#1f77b4", label="Local-Scanning")
        self.axRight[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer")
        self.axRight[0].set_xlabel("Timesteps (Days)")
        self.axRight[0].set_ylabel("Node Count")
        self.axRight[0].set_title("Node Population Sizes Over Time - S, IR, IL, IP")
        # Plotting the second graph
        self.axRight[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.axRight[1].plot(T1, I1, '#d62728', label="All Infected")
        self.axRight[1].set_xlabel("Timesteps (Days)")
        self.axRight[1].set_ylabel("Node Count")
        self.axRight[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        # Plotting the third graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning: {:.0f}".format(pop[1]),
                  "Local-Scanning: {:.0f}".format(pop[2]), "Peer-to-Peer: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
        self.axRight[2].pie(pop, explode=explode, labels=labels, colors=colours)
        self.axRight[2].set_title("Population Sizes on Final Recorded Day #{}".format(self.compareModel.Timesteps))

        self.canvasRight.draw()
