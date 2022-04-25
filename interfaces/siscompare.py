import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from models import sis


class SISCompareInterface(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.setConfigurations(controller)

        ###################################### Instantiating MIDDLE elements ###########################################
        titleFrame = tk.Frame(self, bg="#453354")
        lblTitle = tk.Label(titleFrame, bg="#453354", text="IoT-SIS Virus Model Configuration Comparison", font=("Arial", 15, "italic"),
                            fg="white")
        btnReturn = tk.Button(titleFrame, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: controller.display("SISCompareInterface", "HomeInterface"))
        nameFrame = tk.Frame(self, bg="#574b59")

        legendFrame = tk.Frame(nameFrame, bg="#574b59")
        lblG = tk.Label(legendFrame, text="Green", fg="#2d802f", bg="#574b59", font=("Arial", 9, "bold"))
        lblGEx = tk.Label(legendFrame, text=" Indicates a Higher & Better Score", bg="#574b59", fg="white",
                          font=("Arial", 8))
        lblO = tk.Label(legendFrame, text="Orange", fg="#e68f39", bg="#574b59", font=("Arial", 9, "bold"))
        lblOEx = tk.Label(legendFrame, text="Indicates an Identical Score", bg="#574b59", fg="white", font=("Arial", 8))
        lblR = tk.Label(legendFrame, text="Red", fg="#d12c3f", bg="#574b59", font=("Arial", 9, "bold"))
        lblREx = tk.Label(legendFrame, text="Indicates a Lower & Worse Score", bg="#574b59", fg="white",
                          font=("Arial", 8))

        self.informationFrame = tk.Frame(self, bg="#e0e0e0")

        ##################################### Instantiating LEFT-side elements #########################################
        self.lblLeftName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblLeftScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 17, "bold"))
        btnConfigureLeft = tk.Button(nameFrame, wraplength=57, width=10, text="Control Configuration", font=("Arial", 7),
                                     command=lambda: controller.display("SISCompareInterface", "SISControlInterface"))
        btnInspectLeft = tk.Button(nameFrame, wraplength=57, width=10, text="Inspect Configuration", font=("Arial", 7),
                                   command=lambda: controller.display("SISCompareInterface", "SISInspectInterface"))

        leftFrame = tk.Frame(self, bg="#453354")
        leftGraphFrame = tk.Frame(leftFrame, bg="#654e78")

        figureLeft = plt.figure(facecolor="#654e78")
        self.canvasLeft = FigureCanvasTkAgg(figureLeft, leftGraphFrame)
        self.canvasLeft.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.axLeft = [figureLeft.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(3):
            self.axLeft[x].ticklabel_format(style="plain")
        figureLeft.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.lblFinalNLeft = tk.Label(leftFrame, bg="#654e78", fg="black", font=("Arial", 12))
        self.updateLeftGraph()

        ##################################### Instantiating RIGHT-side elements ########################################
        self.lblRightName = tk.Label(nameFrame, bg="#574b59", font=("Arial", 14), fg="white")
        self.lblRightScore = tk.Label(nameFrame, bg="#574b59", font=("Arial", 17, "bold"))
        btnConfigureRight = tk.Button(nameFrame, wraplength=57, width=10, text="Control Configuration", font=("Arial", 7),
                                      command=lambda: [self.setNewActivePlusIndex(controller), controller.display("SISCompareInterface","SISControlInterface")])
        btnInspectRight = tk.Button(nameFrame, wraplength=57, width=10, text="Inspect Configuration", font=("Arial", 7),
                                    command=lambda: [self.setNewActivePlusIndex(controller), controller.display("SISCompareInterface", "SISInspectInterface")])

        rightFrame = tk.Frame(self, bg="#453354")
        rightGraphFrame = tk.Frame(rightFrame, bg="#654e78")

        figureRight = plt.figure(facecolor="#654e78")
        self.canvasRight = FigureCanvasTkAgg(figureRight, rightGraphFrame)
        self.canvasRight.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.axRight = [figureRight.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(3):
            self.axRight[x].ticklabel_format(style="plain")
        figureRight.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)
        self.lblFinalNRight = tk.Label(rightFrame, bg="#654e78", fg="black", font=("Arial", 12))
        self.updateRightGraph()

        ########################################### Placing ALL elements ###############################################
        titleFrame.place(relwidth=1, relheight=0.07)
        lblTitle.pack(pady=15)
        nameFrame.place(relwidth=1, relheight=0.065, y=60)
        btnReturn.place(x=14, y=14)
        legendFrame.place(x=846, y=3)
        lblG.grid(row=0, column=0)
        lblGEx.grid(row=0, column=1)
        lblO.grid(row=1, column=0)
        lblOEx.grid(row=1, column=1)
        lblR.grid(row=2, column=0)
        lblREx.grid(row=2, column=1)
        self.informationFrame.place(relwidth=0.334, relheight=0.93, y=130, x=639)
        # Left
        btnInspectLeft.pack(side="left", padx=14)
        btnConfigureLeft.pack(side="left", padx=7)
        self.lblLeftName.pack(side="left", padx=10)
        self.lblLeftScore.pack(side="left")
        leftFrame.place(relwidth=0.333, relheight=0.93, y=126, x=0)
        leftGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)
        self.lblFinalNLeft.place(x=160, y=880)
        # Right
        btnInspectRight.pack(side="right", padx=14)
        btnConfigureRight.pack(side="right", padx=7)
        self.lblRightScore.pack(side="right", padx=10)
        self.lblRightName.pack(side="right")
        rightFrame.place(relwidth=0.333, relheight=0.93, y=126, x=1280)
        rightGraphFrame.place(relwidth=0.98, relheight=0.95, x=5, y=5)
        self.lblFinalNRight.place(x=160, y=880)

    # Called upon page opening to set the correct models and ensure the timesteps are synchronised
    def setConfigurations(self, controller):
        self.activeConfiguration = controller.activeConfiguration
        self.compareConfiguration = controller.compareConfiguration

    # Called when opting to configure the Right, CompareModel to ensure compatibility
    def setNewActivePlusIndex(self, controller):
        index = 0
        for M in controller.configurations:
            if M == self.compareConfiguration:
                controller.setActiveConfiguration(index)
                controller.setActiveConfigurationIndex(index)
            index = index + 1

    # Called on page opening to update the Left, ActiveModel graph information
    def updateLeftGraph(self):
        # Configuration is made local to change timesteps for this graph only
        leftConfiguration = sis.SIS(self.activeConfiguration.Name, self.activeConfiguration.N, self.activeConfiguration.I, self.activeConfiguration.WSNnumber, self.activeConfiguration.deploymentArea, self.activeConfiguration.transmissionRange, self.activeConfiguration.contactRate, self.activeConfiguration.botScanningRate, self.activeConfiguration.Ptransmission, self.activeConfiguration.IrPsuccess, self.activeConfiguration.IlPsuccess, self.activeConfiguration.IpPsuccess,
                                 self.activeConfiguration.meanMessageSize, self.activeConfiguration.meanPower, self.activeConfiguration.totalBattery, self.activeConfiguration.recoveryRate, 12, self.activeConfiguration.IDS)

        S1, Ir1, Il1, Ip1 = leftConfiguration.runSimulation()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, leftConfiguration.Timesteps, 500)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axLeft[x].clear() for x in range(3)]

        # Plotting the first graph
        self.axLeft[0].plot(T1, S1, "#2ca02c", label="Susceptible: ")
        self.axLeft[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning")
        self.axLeft[0].plot(T1, Il1, "#1f77b4", label="Local-Scanning")
        self.axLeft[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer")
        self.axLeft[0].set_xlabel("Timesteps (Hours)")
        self.axLeft[0].set_ylabel("Node Count")
        self.axLeft[0].set_title("Node Population Sizes Over Time - S, IR, IL, IP")
        self.axLeft[0].axvline(linewidth=0.5, color="#a8a8a8", x=leftConfiguration.Timesteps / 2, linestyle="--")
        # Plotting the second graph
        self.axLeft[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.axLeft[1].plot(T1, I1, '#d62728', label="All Infected")
        self.axLeft[1].set_xlabel("Timesteps (Hours)")
        self.axLeft[1].set_ylabel("Node Count")
        self.axLeft[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        self.axLeft[1].axvline(linewidth=0.5, color="#a8a8a8", x=leftConfiguration.Timesteps / 2, linestyle="--")
        self.axLeft[1].axhline(linewidth=0.5, color="#d62728", y=max(I1), linestyle="--", label="Peak I: {}".format(max(I1)))
        # Plotting the third graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]

        idx = 0
        for x in range(len(pop)):
            if pop[x] <= 0:
                idx = idx + 1

        if idx == len(pop):
            pop = [1]
            label = ["100% of Nodes are Dead"]
            colour = ["#d62728"]
            self.axLeft[2].pie(pop, labels=label, colors=colour)
            self.axLeft[2].set_title(
                "Population Sizes on Final Recorded Hour #{}".format(leftConfiguration.Timesteps))
        else:
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning: {:.0f}".format(pop[1]),
                      "Local Scanning: {:.0f}".format(pop[2]), "Peer-to-Peer: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.axLeft[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True, labeldistance=1.2)
            self.axLeft[2].set_title("Population Sizes on Final Recorded Hour ({})".format(leftConfiguration.Timesteps))

        self.canvasLeft.draw()
        self.lblFinalNLeft.config(text="Population Sizes Totalled (Final N Value): {:.0f}".format(S1[-1] + I1[-1], leftConfiguration.N))

    # Called on page opening to update the Right, CompareModel graph information
    def updateRightGraph(self):
        # Configuration is made local to change timesteps for this graph only
        rightConfiguration = sis.SIS(self.compareConfiguration.Name, self.compareConfiguration.N, self.compareConfiguration.I, self.compareConfiguration.WSNnumber, self.compareConfiguration.deploymentArea, self.compareConfiguration.transmissionRange, self.compareConfiguration.contactRate, self.compareConfiguration.botScanningRate, self.compareConfiguration.Ptransmission, self.compareConfiguration.IrPsuccess, self.compareConfiguration.IlPsuccess, self.compareConfiguration.IpPsuccess,
                                 self.compareConfiguration.meanMessageSize, self.compareConfiguration.meanPower, self.compareConfiguration.totalBattery, self.compareConfiguration.recoveryRate, 12, self.compareConfiguration.IDS)
        S1, Ir1, Il1, Ip1 = rightConfiguration.runSimulation()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, rightConfiguration.Timesteps, 500)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.axRight[x].clear() for x in range(3)]

        # Plotting the first graph
        self.axRight[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.axRight[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning")
        self.axRight[0].plot(T1, Il1, "#1f77b4", label="Local-Scanning")
        self.axRight[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer")
        self.axRight[0].set_xlabel("Timesteps (Hours)")
        self.axRight[0].set_ylabel("Node Count")
        self.axRight[0].set_title("Node Population Sizes Over Time - S, IR, IL, IP")
        self.axRight[0].axvline(linewidth=0.5, color="#a8a8a8", x=rightConfiguration.Timesteps / 2, linestyle="--")
        # Plotting the second graph
        self.axRight[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.axRight[1].plot(T1, I1, '#d62728', label="All Infected")
        self.axRight[1].set_xlabel("Timesteps (Hours)")
        self.axRight[1].set_ylabel("Node Count")
        self.axRight[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        self.axRight[1].axvline(linewidth=0.5, color="#a8a8a8", x=rightConfiguration.Timesteps / 2, linestyle="--")
        self.axRight[1].axhline(linewidth=0.5, color="#d62728", y=max(I1), linestyle="--", label="Peak I: {}".format(max(I1)))
        # Plotting the third graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]

        idx = 0
        for x in range(len(pop)):
            if pop[x] <= 0:
                idx = idx + 1

        if idx == len(pop):
            pop = [1]
            label = ["100% of Nodes are Dead"]
            colour = ["#d62728"]
            self.axRight[2].pie(pop, labels=label, colors=colour)
            self.axRight[2].set_title("Population Sizes on Final Recorded Hour #{}".format(rightConfiguration.Timesteps))
        else:
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning: {:.0f}".format(pop[1]),
                      "Local Scanning: {:.0f}".format(pop[2]), "Peer-to-Peer: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.axRight[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True, labeldistance=1.2)
            self.axRight[2].set_title(
                "Population Sizes on Final Recorded Hour ({})".format(rightConfiguration.Timesteps))

        self.canvasRight.draw()
        self.lblFinalNRight.config(text="Population Sizes Totalled (Final N Value): {:.0f}".format(S1[-1] + I1[-1], rightConfiguration.N))

    # Called on page opening to set the correct information
    def updateColumnInfo(self):
        activeSingleFactorScore = self.activeConfiguration.calculateScores()[0]
        activeNeighbourScore = self.activeConfiguration.calculateScores()[4]
        activeInfectionScore = self.activeConfiguration.calculateScores()[7]
        activeEffortScore = self.activeConfiguration.calculateScores()[13]
        activeDeathRateScore = self.activeConfiguration.calculateScores()[19]
        activeScore = activeSingleFactorScore + activeNeighbourScore + activeInfectionScore + activeEffortScore + activeDeathRateScore

        compareSingleFactorScore = self.compareConfiguration.calculateScores()[0]
        compareNeighbourScore = self.compareConfiguration.calculateScores()[4]
        compareInfectionScore = self.compareConfiguration.calculateScores()[7]
        compareEffortScore = self.compareConfiguration.calculateScores()[13]
        compareDeathRateScore = self.compareConfiguration.calculateScores()[19]
        compareScore = compareSingleFactorScore + compareNeighbourScore + compareInfectionScore + compareEffortScore + compareDeathRateScore


        self.lblLeftName.config(text="{} Score : ".format(self.activeConfiguration.Name[9:]))
        self.lblRightName.config(text="{} Score : ".format(self.compareConfiguration.Name[9:]))

        if activeScore < compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#d12c3f")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#2d802f")
        if activeScore > compareScore:
            self.lblLeftScore.config(text="{}".format(activeScore), fg="#2d802f")
            self.lblRightScore.config(text="{}".format(compareScore), fg="#d12c3f")
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

        if activeNeighbourScore < compareNeighbourScore:
            lblPopScoreLeft.config(text="{}".format(activeNeighbourScore), fg="#d12c3f")
            lblPopScoreRight.config(text="{}".format(compareNeighbourScore), fg="#2d802f")
            lblPopDesc.config(text="{} has the Better Score for the Neighbour Set Category".format(self.activeConfiguration.Name[9:]))
        if activeNeighbourScore > compareNeighbourScore:
            lblPopScoreLeft.config(text="{}".format(activeNeighbourScore), fg="#2d802f")
            lblPopScoreRight.config(text="{}".format(compareNeighbourScore), fg="#d12c3f")
            lblPopDesc.config(text="{} has the Better Score for the Neighbour Set Category".format(self.compareConfiguration.Name[9:]))
        if activeNeighbourScore == compareNeighbourScore:
            lblPopScoreLeft.config(text="{}".format(activeNeighbourScore), fg="#e68f39")
            lblPopScoreRight.config(text="{}".format(compareNeighbourScore), fg="#e68f39")
            lblPopDesc.config(text="The Models have an Equal Score for the Neighbour Set Category")

        lblSizeLeft = tk.Label(leftScores, text="Size Score :", bg="#e0e0e0")
        lblSizeScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblSizeRight = tk.Label(rightScores, text="Size Score :", bg="#e0e0e0")
        lblSizeScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblSizeDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=25)
        lblBufferLeft1 = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight1 = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actSizeScore < compSizeScore:
            lblSizeScoreLeft.config(text="{}".format(actSizeScore), fg="#d12c3f")
            lblSizeScoreRight.config(text="{}".format(compSizeScore), fg="#2d802f")
            lblPopDesc.config(text="{} has the Better Score for the Population Category".format(self.activeConfiguration.Name[9:]))
        if actSizeScore > compSizeScore:
            lblSizeScoreLeft.config(text="{}".format(actSizeScore), fg="#2d802f")
            lblSizeScoreRight.config(text="{}".format(compSizeScore), fg="#d12c3f")
            lblPopDesc.config(text="{} has the Better Score for the Population Category".format(self.compareConfiguration.Name[9:]))
        if actSizeScore == compSizeScore:
            lblSizeScoreLeft.config(text="{}".format(actSizeScore), fg="#e68f39")
            lblSizeScoreRight.config(text="{}".format(compSizeScore), fg="#e68f39")
            lblSizeDesc.config(text="The Models have an Equal Score for the Size Category")

        lblNeighbourELeft = tk.Label(leftScores, text="Neighbour Set Score :", bg="#e0e0e0")
        lblNeighbourEScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblNeighbourRight = tk.Label(rightScores, text="Neighbour Set Score :", bg="#e0e0e0")
        lblNeighbourScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblNeighbourDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=8)
        lblBufferLeft2 = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight2 = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actNeighbouErScore < compNeighboEurScore:
            lblNeighbEourScoreLeft.config(text="{}".format(actNeiEghbourScore), fg="#d12c3f")
            lblNeighbEourScoreRight.config(text="{}".format(compNEeighbourScore), fg="#2d802f")
            lblNeighbEourDesc.config(text="{} has the Better Score for the Neighbour Sets Category".format(self.activeConfiguration.Name[9:]))
        if actNeighboEurScore > compNeighbourScore:
            lblNeighbEourScoreLeft.config(text="{}".format(actNeiEghbourScore), fg="#2d802f")
            lblNeighbEourScoreRight.config(text="{}".format(compNEeighbourScore), fg="#d12c3f")
            lblNeighEbourDesc.config(text="{} has the Better Score for the Neighbour Sets Category".format(self.compareConfiguration.Name[9:]))
        if actNeighbEourScore == compNeighbourScore:
            lblNeighbEourScoreLeft.config(text="{}".format(actNeiEghbourScore), fg="#e68f39")
            lblNeighbEourScoreRight.config(text="{}".format(compNEeighbourScore), fg="#e68f39")
            lblNeighboEurDesc.config(text="The Models have an Equal Score for the Neighbour Sets Category")

        lblInfectionLeft = tk.Label(leftScores, text="Infection Rates Score :", bg="#e0e0e0")
        lblInfectionScoreLeft = tk.Label(leftScores, bg="#e0e0e0")
        lblInfectionRight = tk.Label(rightScores, text="Infection Rates Score :", bg="#e0e0e0")
        lblInfectionScoreRight = tk.Label(rightScores, bg="#e0e0e0")
        lblInfectionDesc = tk.Label(centreFrame, bg="#e0e0e0", wraplength=190, pady=17)
        lblBufferLeft3 = tk.Label(leftScores, text="", bg="#e0e0e0")
        lblBufferRight3 = tk.Label(rightScores, text="", bg="#e0e0e0")

        if actInfectionScore < compInfectionScore:
            lblInfectionScoreLeft.config(text="{}".format(actInfectionScore), fg="#d12c3f")
            lblInfectionScoreRight.config(text="{}".format(compInfectionScore), fg="#2d802f")
            lblInfectionDesc.config(
                text="{} has the Better Score for the Infection Rates Category".format(self.activeConfiguration.Name[9:]))
        if actInfectionScore > compInfectionScore:
            lblInfectionScoreLeft.config(text="{}".format(actInfectionScore), fg="#2d802f")
            lblInfectionScoreRight.config(text="{}".format(compInfectionScore), fg="#d12c3f")
            lblInfectionDesc.config(
                text="{} has the Better Score for the Infection Rates Category".format(self.compareConfiguration.Name[9:]))
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
            lblDeathScoreLeft.config(text="{}".format(actDeathScore), fg="#d12c3f")
            lblDeathScoreRight.config(text="{}".format(compDeathScore), fg="#2d802f")
            lblDeathDesc.config(
                text="{} has the Better Score for the Death Rates Category".format(self.activeConfiguration.Name[9:]))
        if actDeathScore > compDeathScore:
            lblDeathScoreLeft.config(text="{}".format(actDeathScore), fg="#2d802f")
            lblDeathScoreRight.config(text="{}".format(compDeathScore), fg="#d12c3f")
            lblDeathDesc.config(
                text="{} has the Better Score for the Death Rates Category".format(self.compareConfiguration.Name[9:]))
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
            lblMiscScoreLeft.config(text="{}".format(actMiscScore), fg="#d12c3f")
            lblMiscScoreRight.config(text="{}".format(compMiscScore), fg="#2d802f")
            lblMiscDesc.config(
                text="{} has the Better Score for the Miscellaneous Category".format(self.activeConfiguration.Name[9:]))
        if actMiscScore > compMiscScore:
            lblMiscScoreLeft.config(text="{}".format(actMiscScore), fg="#2d802f")
            lblMiscScoreRight.config(text="{}".format(compMiscScore), fg="#d12c3f")
            lblMiscDesc.config(
                text="{} has the Better Score for the Miscellaneous Category".format(self.compareConfiguration.Name[9:]))
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
