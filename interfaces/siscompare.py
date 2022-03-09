import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class SISCompareInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interfaces
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.setModels(controller)

        titleFrame = tk.Frame(self, bg="#453354")
        lblTitle = tk.Label(titleFrame, bg="#453354", text="SIS Virus Model Comparison", font=("Arial", 15, "italic"), fg="white")
        btnReturn = tk.Button(titleFrame, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: controller.display("SISCompareInterface", "HomeInterface"))
        nameFrame = tk.Frame(self, bg="#574b59")
        self.lblLeftName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblLeftScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 16))
        btnConfigureLeft = tk.Button(nameFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                     command=lambda: controller.display("SISCompareInterface", "SISControlInterface"))
        self.lblRightName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblRightScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 16))
        btnConfigureRight = tk.Button(nameFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                     command=lambda: [self.setNewActivePlusIndex(controller), controller.display("SISCompareInterface", "SISControlInterface")])
        legendFrame = tk.Frame(nameFrame, bg="#574b59")
        lblG = tk.Label(legendFrame, text="Green", fg="#2d802f", bg="#574b59", font=("Arial", 9, "bold"))
        lblGEx = tk.Label(legendFrame, text=" Indicates a Lower & Better Score", bg="#574b59", fg="white", font=("Arial", 8))
        lblO = tk.Label(legendFrame, text="Orange", fg="#e68f39", bg="#574b59", font=("Arial", 9, "bold"))
        lblOEx = tk.Label(legendFrame, text="Indicates an Identical Score", bg="#574b59", fg="white", font=("Arial", 8))
        lblR = tk.Label(legendFrame, text="Red", fg="#d12c3f", bg="#574b59", font=("Arial", 9, "bold"))
        lblREx = tk.Label(legendFrame, text="Indicates a Higher & Worse Score", bg="#574b59", fg="white", font=("Arial", 8))
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
        nameFrame.place(relwidth=1, relheight=0.08, y=60)
        btnReturn.place(x=14, y=14)
        btnConfigureLeft.pack(side="left", padx=14)
        self.lblLeftName.pack(side="left", padx=10)
        self.lblLeftScore.pack(side="left")
        btnConfigureRight.pack(side="right", padx=14)
        self.lblRightName.pack(side="right", padx=10)
        self.lblRightScore.pack(side="right")
        legendFrame.place(x=657, y=3)
        lblG.grid(row=0, column=0)
        lblGEx.grid(row=0, column=1)
        lblO.grid(row=1, column=0)
        lblOEx.grid(row=1, column=1)
        lblR.grid(row=2, column=0)
        lblREx.grid(row=2, column=1)
        leftFrame.place(relwidth=0.333, relheight=0.93, y=126, x=0)
        leftGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)
        rightFrame.place(relwidth=0.333, relheight=0.93, y=126, x=1025)
        rightGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)
        self.informationFrame.place(relwidth=0.334, relheight=0.93, y=130, x=511)

    # Method: Called upon page opening to set the correct models
    def setModels(self, controller):
        self.activeModel = controller.activeModel
        self.compareModel = controller.compareModel

    # Method: Called when opting to configure the Right, CompareModel to ensure compatibility
    def setNewActivePlusIndex(self, controller):
        index = 0
        for M in controller.models:
            if M == self.compareModel:
                controller.setActiveModel(index)
                controller.setActiveModelIndex(index)
            index = index + 1

    # Method: Called on page opening to update the Left, ActiveModel graph information
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

    # Method: Called on page opening to update the Right, CompareModel graph information
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

    # Method: Called on page opening to set the correct information
    def updateColumnInfo(self):
        activeScore = self.activeModel.calculateScores()[8]
        actPopScore = self.activeModel.calculateScores()[1]
        actSizeScore = self.activeModel.calculateScores()[4]
        compareScore = self.compareModel.calculateScores()[8]
        compPopScore = self.compareModel.calculateScores()[1]
        compSizeScore = self.compareModel.calculateScores()[4]

        self.lblLeftName.config(text="{}   |   Total Score :".format(self.activeModel.Name))
        self.lblRightName.config(text=": Total Score   |   {}".format(self.compareModel.Name))

        if activeScore < compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#2d802f")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#d12c3f")
        if activeScore > compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#d12c3f")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#2d802f")
        if activeScore == compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#e68f39")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#e68f39")

        leftScores = tk.Frame(self.informationFrame, bg="#e0e0e0")
        rightScores = tk.Frame(self.informationFrame, bg="#e0e0e0")
        lblPopLeft = tk.Label(leftScores, text="Population Score:", bg="#e0e0e0")
        lblPopScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblPopRight = tk.Label(rightScores, text="Population Score:", bg="#e0e0e0")
        lblPopScoreRight = tk.Label(rightScores, bg="#e0e0e0")

        if actPopScore < compPopScore:
            lblPopScoreLeft.config(text="{}".format(actPopScore), fg="#2d802f")
            lblPopScoreRight.config(text="{}".format(compPopScore), fg="#d12c3f")
        if actPopScore > compPopScore:
            lblPopScoreLeft.config(text="{}".format(actPopScore), fg="#d12c3f")
            lblPopScoreRight.config(text="{}".format(compPopScore), fg="#2d802f")
        if actPopScore == compPopScore:
            lblPopScoreLeft.config(text="{}".format(actPopScore), fg="#e68f39")
            lblPopScoreRight.config(text="{}".format(compPopScore), fg="#e68f39")

        centreFrame = tk.Frame(self.informationFrame, bg="#e0e0e0")




        leftScores.place(x=3, y=3, relheight=0.98, relwidth=0.28)
        lblPopLeft.grid(row=0, column=0, sticky="w")
        lblPopScoreLeft.grid(row=1, column=0, sticky="w")
        lblPopRight.grid(row=0, column=0, sticky="e")
        lblPopScoreRight.grid(row=1, column=0, sticky="e")

        centreFrame.place(x=150, y=3, relheight=0.98, relwidth=0.42)


        rightScores.place(x=367, y=3, relheight=0.98, relwidth=0.28)
