import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class SEIRCompareInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interfaces
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.setModels(controller)

        titleFrame = tk.Frame(self, bg="#453354")
        lblTitle = tk.Label(titleFrame, bg="#453354", text="SEIR Virus Model Comparison", font=("Arial", 15, "italic"), fg="white")
        btnReturn = tk.Button(titleFrame, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: controller.display("SEIRCompareInterface", "HomeInterface"))
        nameFrame = tk.Frame(self, bg="#574b59")
        self.lblLeftName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblLeftScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 16))
        btnConfigureLeft = tk.Button(nameFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                     command=lambda: controller.display("SEIRCompareInterface", "SEIRControlInterface"))
        btnInspectLeft = tk.Button(nameFrame, wraplength=41, width=7, text="Inspect Model", font=("Arial", 7),
                                     command=lambda: controller.display("SEIRCompareInterface", "SEIRInspectInterface"))
        self.lblRightName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblRightScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 16))
        btnConfigureRight = tk.Button(nameFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                     command=lambda: [self.setNewActivePlusIndex(controller), controller.display("SEIRCompareInterface", "SEIRControlInterface")])
        btnInspectRight = tk.Button(nameFrame, wraplength=41, width=7, text="Inspect Model", font=("Arial", 7),
                                      command=lambda: [self.setNewActivePlusIndex(controller),
                                                       controller.display("SEIRCompareInterface",
                                                                          "SEIRInspectInterface")])
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
        for x in range(2):
            self.axLeft[x].ticklabel_format(style="plain")
        figureLeft.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.updateLeftGraph()

        figureRight = plt.figure(facecolor="#654e78")
        self.canvasRight = FigureCanvasTkAgg(figureRight, rightGraphFrame)
        self.canvasRight.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.axRight = [figureRight.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(2):
            self.axRight[x].ticklabel_format(style="plain")
        figureRight.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.updateRightGraph()

        titleFrame.place(relwidth=1, relheight=0.07)
        lblTitle.pack(pady=15)
        nameFrame.place(relwidth=1, relheight=0.08, y=60)
        btnReturn.place(x=14, y=14)
        btnInspectLeft.pack(side="left", padx=14)
        btnConfigureLeft.pack(side="left", padx=7)
        self.lblLeftName.pack(side="left", padx=10)
        self.lblLeftScore.pack(side="left")
        btnInspectRight.pack(side="right", padx=14)
        btnConfigureRight.pack(side="right", padx=7)
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
        S1, E1, I1, R1 = self.activeModel.runModel()
        T1 = np.linspace(0, self.activeModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axLeft[x].clear() for x in range(2)]

        # Plotting the first graph
        self.axLeft[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.axLeft[0].plot(T1, S1, "#2ca02c", label="Exposed")
        self.axLeft[0].plot(T1, I1, "#d62728", label="Infected")
        self.axLeft[0].plot(T1, R1, "#1f77b4", label="Recovered")
        self.axLeft[0].set_xlabel("Timesteps (Days)")
        self.axLeft[0].set_ylabel("Population Count")
        self.axLeft[0].set_title("Population Sizes Over Time - S, I, R")
        # Plotting the second graph
        pop = [S1[len(S1) - 1], E1[len(I1) - 1], I1[len(I1) - 1], R1[len(R1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Exposed: {:.0f}".format(pop[1]),
                  "Infected: {:.0f}".format(pop[2]), "Recovered: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#d62728", "#1f77b4"]
        self.axLeft[1].pie(pop, explode=explode, labels=labels, colors=colours)
        self.axLeft[1].set_title("Population Sizes on Final Recorded Day #{}".format(self.controller.activeModel.Timesteps))

        self.canvasLeft.draw()

    # Method: Called on page opening to update the Right, CompareModel graph information
    def updateRightGraph(self):
        S1, E1, I1, R1 = self.compareModel.runModel()
        T1 = np.linspace(0, self.compareModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axRight[x].clear() for x in range(2)]

        # Plotting the first graph
        self.axRight[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.axRight[0].plot(T1, S1, "#2ca02c", label="Exposed")
        self.axRight[0].plot(T1, I1, "#d62728", label="Infected")
        self.axRight[0].plot(T1, R1, "#1f77b4", label="Recovered")
        self.axRight[0].set_xlabel("Timesteps (Days)")
        self.axRight[0].set_ylabel("Population Count")
        self.axRight[0].set_title("Population Sizes Over Time - S, I, R")
        # Plotting the second graph
        pop = [S1[len(S1) - 1], E1[len(I1) - 1], I1[len(I1) - 1], R1[len(R1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Exposed: {:.0f}".format(pop[1]),
                  "Infected: {:.0f}".format(pop[2]), "Recovered: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#d62728", "#1f77b4"]
        self.axRight[1].pie(pop, explode=explode, labels=labels, colors=colours)
        self.axRight[1].set_title(
            "Population Sizes on Final Recorded Day #{}".format(self.controller.activeModel.Timesteps))

        self.canvasRight.draw()

    # Method: Called on page opening to set the correct information
    def updateColumnInfo(self):
        activeScore = self.activeModel.calculateScores()[8]
        actPopScore = self.activeModel.calculateScores()[0]
        actSizeScore = self.activeModel.calculateScores()[3]
        actNeighbourScore = self.activeModel.calculateScores()[4]
        actInfectionScore = self.activeModel.calculateScores()[5]
        actDeathScore = self.activeModel.calculateScores()[6]
        actMiscScore = self.activeModel.calculateScores()[7]
        compareScore = self.compareModel.calculateScores()[8]
        compPopScore = self.compareModel.calculateScores()[0]
        compSizeScore = self.compareModel.calculateScores()[3]
        compNeighbourScore = self.compareModel.calculateScores()[4]
        compInfectionScore = self.compareModel.calculateScores()[5]
        compDeathScore = self.compareModel.calculateScores()[6]
        compMiscScore = self.compareModel.calculateScores()[7]

        self.lblLeftName.config(text="{}   |   Total Score :".format(self.activeModel.Name[5:]))
        self.lblRightName.config(text=": Total Score   |   {}".format(self.compareModel.Name[5:]))

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
        centreFrame = tk.Frame(self.informationFrame, bg="#e0e0e0")

        lblPopLeft = tk.Label(leftScores, text="Population Score :", bg="#e0e0e0")
        lblPopScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblPopRight = tk.Label(rightScores, text="Population Score :", bg="#e0e0e0")
        lblPopScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblPopDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=2)
        lblBufferLeft = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actPopScore < compPopScore:
            lblPopScoreLeft.config(text="{}".format(actPopScore), fg="#2d802f")
            lblPopScoreRight.config(text="{}".format(compPopScore), fg="#d12c3f")
            lblPopDesc.config(text="{} has the Better Score for the Population Category".format(self.activeModel.Name[5:]))
        if actPopScore > compPopScore:
            lblPopScoreLeft.config(text="{}".format(actPopScore), fg="#d12c3f")
            lblPopScoreRight.config(text="{}".format(compPopScore), fg="#2d802f")
            lblPopDesc.config(text="{} has the Better Score for the Population Category".format(self.compareModel.Name[5:]))
        if actPopScore == compPopScore:
            lblPopScoreLeft.config(text="{}".format(actPopScore), fg="#e68f39")
            lblPopScoreRight.config(text="{}".format(compPopScore), fg="#e68f39")
            lblPopDesc.config(text="The Models have an Equal Score for the Population Category")

        lblSizeLeft = tk.Label(leftScores, text="Size Score :", bg="#e0e0e0")
        lblSizeScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblSizeRight = tk.Label(rightScores, text="Size Score :", bg="#e0e0e0")
        lblSizeScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblSizeDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=25)
        lblBufferLeft1 = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight1 = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actSizeScore < compSizeScore:
            lblSizeScoreLeft.config(text="{}".format(actSizeScore), fg="#2d802f")
            lblSizeScoreRight.config(text="{}".format(compSizeScore), fg="#d12c3f")
            lblPopDesc.config(text="{} has the Better Score for the Population Category".format(self.activeModel.Name[5:]))
        if actSizeScore > compSizeScore:
            lblSizeScoreLeft.config(text="{}".format(actSizeScore), fg="#d12c3f")
            lblSizeScoreRight.config(text="{}".format(compSizeScore), fg="#2d802f")
            lblPopDesc.config(text="{} has the Better Score for the Population Category".format(self.compareModel.Name[5:]))
        if actSizeScore == compSizeScore:
            lblSizeScoreLeft.config(text="{}".format(actSizeScore), fg="#e68f39")
            lblSizeScoreRight.config(text="{}".format(compSizeScore), fg="#e68f39")
            lblSizeDesc.config(text="The Models have an Equal Score for the Size Category")

        lblNeighbourLeft = tk.Label(leftScores, text="Neighbour Set Score :", bg="#e0e0e0")
        lblNeighbourScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblNeighbourRight = tk.Label(rightScores, text="Neighbour Set Score :", bg="#e0e0e0")
        lblNeighbourScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblNeighbourDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=8)
        lblBufferLeft2 = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight2 = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actNeighbourScore < compNeighbourScore:
            lblNeighbourScoreLeft.config(text="{}".format(actNeighbourScore), fg="#2d802f")
            lblNeighbourScoreRight.config(text="{}".format(compNeighbourScore), fg="#d12c3f")
            lblNeighbourDesc.config(text="{} has the Better Score for the Neighbour Sets Category".format(self.activeModel.Name[5:]))
        if actNeighbourScore > compNeighbourScore:
            lblNeighbourScoreLeft.config(text="{}".format(actNeighbourScore), fg="#d12c3f")
            lblNeighbourScoreRight.config(text="{}".format(compNeighbourScore), fg="#2d802f")
            lblNeighbourDesc.config(text="{} has the Better Score for the Neighbour Sets Category".format(self.compareModel.Name[5:]))
        if actNeighbourScore == compNeighbourScore:
            lblNeighbourScoreLeft.config(text="{}".format(actNeighbourScore), fg="#e68f39")
            lblNeighbourScoreRight.config(text="{}".format(compNeighbourScore), fg="#e68f39")
            lblNeighbourDesc.config(text="The Models have an Equal Score for the Neighbour Sets Category")

        lblInfectionLeft = tk.Label(leftScores, text="Infection Rates Score :", bg="#e0e0e0")
        lblInfectionScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblInfectionRight = tk.Label(rightScores, text="Infection Rates Score :", bg="#e0e0e0")
        lblInfectionScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblInfectionDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=17)
        lblBufferLeft3 = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight3 = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actInfectionScore < compInfectionScore:
            lblInfectionScoreLeft.config(text="{}".format(actInfectionScore), fg="#2d802f")
            lblInfectionScoreRight.config(text="{}".format(compInfectionScore), fg="#d12c3f")
            lblInfectionDesc.config(
                text="{} has the Better Score for the Infection Rates Category".format(self.activeModel.Name[5:]))
        if actInfectionScore > compInfectionScore:
            lblInfectionScoreLeft.config(text="{}".format(actInfectionScore), fg="#d12c3f")
            lblInfectionScoreRight.config(text="{}".format(compInfectionScore), fg="#2d802f")
            lblInfectionDesc.config(
                text="{} has the Better Score for the Infection Rates Category".format(self.compareModel.Name[5:]))
        if actInfectionScore == compInfectionScore:
            lblInfectionScoreLeft.config(text="{}".format(actInfectionScore), fg="#e68f39")
            lblInfectionScoreRight.config(text="{}".format(compInfectionScore), fg="#e68f39")
            lblInfectionDesc.config(text="The Models have an Equal Score for the Infection Rates Category")

        lblDeathLeft = tk.Label(leftScores, text="Death Rates Score :", bg="#e0e0e0")
        lblDeathScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblDeathRight = tk.Label(rightScores, text="Death Rates Score :", bg="#e0e0e0")
        lblDeathScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblDeathDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=15)
        lblBufferLeft4 = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight4 = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actDeathScore < compDeathScore:
            lblDeathScoreLeft.config(text="{}".format(actDeathScore), fg="#2d802f")
            lblDeathScoreRight.config(text="{}".format(compDeathScore), fg="#d12c3f")
            lblDeathDesc.config(
                text="{} has the Better Score for the Death Rates Category".format(self.activeModel.Name[5:]))
        if actDeathScore > compDeathScore:
            lblDeathScoreLeft.config(text="{}".format(actDeathScore), fg="#d12c3f")
            lblDeathScoreRight.config(text="{}".format(compDeathScore), fg="#2d802f")
            lblDeathDesc.config(
                text="{} has the Better Score for the Death Rates Category".format(self.compareModel.Name[5:]))
        if actDeathScore == compDeathScore:
            lblDeathScoreLeft.config(text="{}".format(actDeathScore), fg="#e68f39")
            lblDeathScoreRight.config(text="{}".format(compDeathScore), fg="#e68f39")
            lblDeathDesc.config(text="The Models have an Equal Score for the Death Rates Category")

        lblMiscLeft = tk.Label(leftScores, text="Miscellaneous Score :", bg="#e0e0e0")
        lblMiscScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblMiscRight = tk.Label(rightScores, text="Miscellaneous Score :", bg="#e0e0e0")
        lblMiscScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblMiscDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=14)

        if actMiscScore < compMiscScore:
            lblMiscScoreLeft.config(text="{}".format(actMiscScore), fg="#2d802f")
            lblMiscScoreRight.config(text="{}".format(compMiscScore), fg="#d12c3f")
            lblMiscDesc.config(
                text="{} has the Better Score for the Miscellaneous Category".format(self.activeModel.Name[5:]))
        if actMiscScore > compMiscScore:
            lblMiscScoreLeft.config(text="{}".format(actMiscScore), fg="#d12c3f")
            lblMiscScoreRight.config(text="{}".format(compMiscScore), fg="#2d802f")
            lblMiscDesc.config(
                text="{} has the Better Score for the Miscellaneous Category".format(self.compareModel.Name[5:]))
        if actMiscScore == compMiscScore:
            lblMiscScoreLeft.config(text="{}".format(actMiscScore), fg="#e68f39")
            lblMiscScoreRight.config(text="{}".format(compMiscScore), fg="#e68f39")
            lblMiscDesc.config(text="The Models have an Equal Score for the Miscellaneous Category")

        leftScores.place(x=3, y=12, relheight=0.98, relwidth=0.28)
        rightScores.place(x=367, y=12, relheight=0.98, relwidth=0.28)
        centreFrame.place(x=150, y=12, relheight=0.98, relwidth=0.42)

        lblPopLeft.pack()
        lblPopScoreLeft.pack()
        lblPopRight.pack()
        lblPopScoreRight.pack()
        lblPopDesc.pack()
        lblBufferLeft.pack()
        lblBufferRight.pack()
        lblSizeLeft.pack()
        lblSizeScoreLeft.pack()
        lblSizeRight.pack()
        lblSizeScoreRight.pack()
        lblSizeDesc.pack()
        lblBufferLeft1.pack()
        lblBufferRight1.pack()
        lblNeighbourLeft.pack()
        lblNeighbourScoreLeft.pack()
        lblNeighbourRight.pack()
        lblNeighbourScoreRight.pack()
        lblNeighbourDesc.pack()
        lblBufferLeft2.pack()
        lblBufferRight2.pack()
        lblInfectionLeft.pack()
        lblInfectionScoreLeft.pack()
        lblInfectionRight.pack()
        lblInfectionScoreRight.pack()
        lblInfectionDesc.pack()
        lblBufferLeft3.pack()
        lblBufferRight3.pack()
        lblDeathLeft.pack()
        lblDeathScoreLeft.pack()
        lblDeathRight.pack()
        lblDeathScoreRight.pack()
        lblDeathDesc.pack()
        lblBufferLeft4.pack()
        lblBufferRight4.pack()
        lblMiscLeft.pack()
        lblMiscScoreLeft.pack()
        lblMiscRight.pack()
        lblMiscScoreRight.pack()
        lblMiscDesc.pack()
