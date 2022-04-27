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

        ###################################### Instantiating CENTER elements ###########################################
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

    # Called upon page opening to set the correct configurations
    def setConfigurations(self, controller):
        self.activeConfiguration = controller.activeConfiguration
        self.compareConfiguration = controller.compareConfiguration

    # Called when opting to configure the Right configuration to update the active configuration
    def setNewActivePlusIndex(self, controller):
        index = 0
        for M in controller.configurations:
            if M == self.compareConfiguration:
                controller.setActiveConfiguration(index)
                controller.setActiveConfigurationIndex(index)
            index = index + 1

    # Called on page opening to update the Left, activeConfiguration graph information
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
        # Following code deals with any negative values to ensure the pie charts do not throw up errors
        idx = 0
        for x in range(len(pop)):
            if pop[x] <= 0.999999999999999999999:
                idx = idx + 1
        if idx == len(pop):
            pop = [1]
            label = ["100% of Nodes are Dead"]
            colour = ["#d62728"]
            self.axLeft[2].pie(pop, labels=label, colors=colour)
            self.axLeft[2].set_title(
                "Population Sizes on Final Recorded Hour #{}".format(leftConfiguration.Timesteps))
        elif 1 <= idx < 4:
            for x in range(len(pop)):
                if pop[x] <= 0:
                    pop[x] = 0
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning Infected: {:.0f}".format(pop[1]),
                      "Local Scanning Infected: {:.0f}".format(pop[2]), "Peer-to-Peer Infected: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.axLeft[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True)
            self.axLeft[2].set_title(
                "Population Sizes on Final Recorded Hour ({})".format(leftConfiguration.Timesteps))
        else:
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning: {:.0f}".format(pop[1]),
                      "Local Scanning: {:.0f}".format(pop[2]), "Peer-to-Peer: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.axLeft[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True, labeldistance=1.2)
            self.axLeft[2].set_title("Population Sizes on Final Recorded Hour ({})".format(leftConfiguration.Timesteps))

        self.canvasLeft.draw()
        self.lblFinalNLeft.config(text="Population Sizes Totalled (Final N Value): {:.0f}".format(S1[-1] + I1[-1]))

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
        # Following code deals with any negative values to ensure the pie charts do not throw up errors
        idx = 0
        for x in range(len(pop)):
            if pop[x] <= 0.999999999999999999999:
                idx = idx + 1
        if idx == len(pop):
            pop = [1]
            label = ["100% of Nodes are Dead"]
            colour = ["#d62728"]
            self.axRight[2].pie(pop, labels=label, colors=colour)
            self.axRight[2].set_title("Population Sizes on Final Recorded Hour #{}".format(rightConfiguration.Timesteps))
        elif 1 <= idx < 4:
            for x in range(len(pop)):
                if pop[x] <= 0:
                    pop[x] = 0
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning Infected: {:.0f}".format(pop[1]),
                      "Local Scanning Infected: {:.0f}".format(pop[2]), "Peer-to-Peer Infected: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.axRight[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True)
            self.axRight[2].set_title(
                "Population Sizes on Final Recorded Hour ({})".format(rightConfiguration.Timesteps))
        else:
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning: {:.0f}".format(pop[1]),
                      "Local Scanning: {:.0f}".format(pop[2]), "Peer-to-Peer: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.axRight[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True, labeldistance=1.2)
            self.axRight[2].set_title(
                "Population Sizes on Final Recorded Hour ({})".format(rightConfiguration.Timesteps))

        self.canvasRight.draw()
        self.lblFinalNRight.config(text="Population Sizes Totalled (Final N Value): {:.0f}".format(S1[-1] + I1[-1]))

    # Called on page opening to set the correct information on the center information section
    # The section displays page elements based on elements with higher / lower scores, done through many IF statements
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

        explainFrame = tk.Frame(self.informationFrame, bg="#e0e0e0")
        comparisonFrame = tk.Frame(self.informationFrame, bg="#e0e0e0")
        lblExplain = tk.Label(explainFrame, bg="#e0e0e0", font=("Arial", 12), justify="center", wraplength=630,
                              text="This section takes two chosen configurations and compares them, side-by-side.\n\n"
                                   "The goal is to allow quick visualisation and understanding of where two configurations differ, or where they are similar.")
        lblLeft = tk.Label(comparisonFrame, text="{} Scores".format(self.activeConfiguration.Name[9:]), bg="#e0e0e0", font=("Arial", 10, "bold"), wraplength=170)
        lblRight = tk.Label(comparisonFrame, text="{} Scores".format(self.compareConfiguration.Name[9:]), bg="#e0e0e0", font=("Arial", 10, "bold"), wraplength=170)

        lblNeighbourLeft = tk.Label(comparisonFrame, text="Neighbour Sets ( /7):", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblNeighbourScoreLeft = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblNeighbourRight = tk.Label(comparisonFrame, text="Neighbour Sets: ( /7)", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblNeighbourScoreRight = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblNeighbourDesc = tk.Label(comparisonFrame, bg="#e0e0e0", wraplength=280, pady=2, font=("Arial", 10))
        if activeNeighbourScore < compareNeighbourScore:
            lblNeighbourScoreLeft.config(text="{}".format(activeNeighbourScore), fg="#d12c3f")
            lblNeighbourScoreRight.config(text="{}".format(compareNeighbourScore), fg="#2d802f")
            lblNeighbourDesc.config(text="The   {}   configuration's Neighbour Sets are smaller than average, minimising the IL and IP attack surfaces.".format(self.compareConfiguration.Name[9:]))
        if activeNeighbourScore > compareNeighbourScore:
            lblNeighbourScoreLeft.config(text="{}".format(activeNeighbourScore), fg="#2d802f")
            lblNeighbourScoreRight.config(text="{}".format(compareNeighbourScore), fg="#d12c3f")
            lblNeighbourDesc.config(text="The   {}   configuration's Neighbour Sets are smaller than average, minimising the IL and IP attack surfaces.".format(self.activeConfiguration.Name[9:]))
        if activeNeighbourScore == compareNeighbourScore:
            lblNeighbourScoreLeft.config(text="{}".format(activeNeighbourScore), fg="#e68f39")
            lblNeighbourScoreRight.config(text="{}".format(compareNeighbourScore), fg="#e68f39")
            lblNeighbourDesc.config(text="Both configuration's Neighbour Sets are equally sized.")

        lblInfLeft = tk.Label(comparisonFrame, text="Infection Rates ( /16):", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblInfScoreLeft = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblInfRight = tk.Label(comparisonFrame, text="Infection Rates ( /16):", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblInfScoreRight = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblInfDesc = tk.Label(comparisonFrame, bg="#e0e0e0", wraplength=280, pady=2, font=("Arial", 10))
        if activeInfectionScore < compareInfectionScore:
            lblInfScoreLeft.config(text="{}".format(activeInfectionScore), fg="#d12c3f")
            lblInfScoreRight.config(text="{}".format(compareInfectionScore), fg="#2d802f")
            lblInfDesc.config(
                text="The   {}   configuration's Infection Rates are lower than average, minimising overall infection and I population size.".format(
                    self.compareConfiguration.Name[9:]))
        if activeInfectionScore > compareInfectionScore:
            lblInfScoreLeft.config(text="{}".format(activeInfectionScore), fg="#2d802f")
            lblInfScoreRight.config(text="{}".format(compareInfectionScore), fg="#d12c3f")
            lblInfDesc.config(
                text="The   {}   configuration's Infection Rates are lower than average, minimising overall infection and I population size.".format(
                    self.activeConfiguration.Name[9:]))
        if activeInfectionScore == compareInfectionScore:
            lblInfScoreLeft.config(text="{}".format(activeInfectionScore), fg="#e68f39")
            lblInfScoreRight.config(text="{}".format(compareInfectionScore), fg="#e68f39")
            lblInfDesc.config(text="Both configuration's Infection Rates are equal, infection spreads through the network at the same pace.")

        lblEffortLeft = tk.Label(comparisonFrame, text="Payload Effort ( /13):", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblEffortScoreLeft = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblEffortRight = tk.Label(comparisonFrame, text="Payload Effort ( /13):", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblEffortScoreRight = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblEffortDesc = tk.Label(comparisonFrame, bg="#e0e0e0", wraplength=280, pady=2, font=("Arial", 10))
        if activeEffortScore < compareEffortScore:
            lblEffortScoreLeft.config(text="{}".format(activeEffortScore), fg="#d12c3f")
            lblEffortScoreRight.config(text="{}".format(compareEffortScore), fg="#2d802f")
            lblEffortDesc.config(
                text="The   {}   configuration's factors contributing towards delivery of payloads across the network result in less effort exerted and power consumed.".format(
                    self.compareConfiguration.Name[9:]))
        if activeEffortScore > compareEffortScore:
            lblEffortScoreLeft.config(text="{}".format(activeEffortScore), fg="#2d802f")
            lblEffortScoreRight.config(text="{}".format(compareEffortScore), fg="#d12c3f")
            lblEffortDesc.config(
                text="The   {}   configuration's factors contributing towards delivery of payloads across the network result in less effort exerted and power consumed.".format(
                    self.activeConfiguration.Name[9:]))
        if activeEffortScore == compareEffortScore:
            lblEffortScoreLeft.config(text="{}".format(activeEffortScore), fg="#e68f39")
            lblEffortScoreRight.config(text="{}".format(compareEffortScore), fg="#e68f39")
            lblEffortDesc.config(
                text="Both configuration's factors contributing towards delivery of payloads across the network result in equal effort exerted and power consumed..")

        lblDthLeft = tk.Label(comparisonFrame, text="Lifespan and Death Rates ( /22):", bg="#e0e0e0", font=("Arial", 10, "underline"), wraplength=160)
        lblDthScoreLeft = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblDthRight = tk.Label(comparisonFrame, text="Lifespan and Death Rates ( /22):", bg="#e0e0e0", font=("Arial", 10, "underline"), wraplength=160)
        lblDthScoreRight = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblDthDesc = tk.Label(comparisonFrame, bg="#e0e0e0", wraplength=280, pady=2, font=("Arial", 10))
        if activeDeathRateScore < compareDeathRateScore:
            lblDthScoreLeft.config(text="{}".format(activeDeathRateScore), fg="#d12c3f")
            lblDthScoreRight.config(text="{}".format(compareDeathRateScore), fg="#2d802f")
            lblDthDesc.config(
                text="The   {}   configuration's Node Lifespans are longer, and the corresponding Death Rates shorter. Nodes live longer durations and mean malicious activity & effort used is low.".format(
                    self.compareConfiguration.Name[9:]))
        if activeDeathRateScore > compareDeathRateScore:
            lblDthScoreLeft.config(text="{}".format(activeDeathRateScore), fg="#2d802f")
            lblDthScoreRight.config(text="{}".format(compareDeathRateScore), fg="#d12c3f")
            lblDthDesc.config(
                text="The   {}   configuration's Node Lifespans are longer, and the corresponding Death Rates shorter. Nodes live longer durations and mean malicious activity & effort used is low.".format(
                    self.activeConfiguration.Name[9:]))
        if activeDeathRateScore == compareDeathRateScore:
            lblDthScoreLeft.config(text="{}".format(activeDeathRateScore), fg="#e68f39")
            lblDthScoreRight.config(text="{}".format(compareDeathRateScore), fg="#e68f39")
            lblDthDesc.config(
                text="Both configuration's Nodes have equal Lifespans and Death Rates. Nodes live the same duration and perform the same amount of malicious activity.")

        lblSFLeft = tk.Label(comparisonFrame, text="Single Factors ( /8):", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblSFScoreLeft = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblSFRight = tk.Label(comparisonFrame, text="Single Factors ( /8):", bg="#e0e0e0", font=("Arial", 10, "underline"))
        lblSFScoreRight = tk.Label(comparisonFrame, bg="#e0e0e0", font=("Arial", 11, "bold"))
        lblSFDesc = tk.Label(comparisonFrame, bg="#e0e0e0", wraplength=280, pady=2, font=("Arial", 10))
        if activeSingleFactorScore < compareSingleFactorScore:
            lblSFScoreLeft.config(text="{}".format(activeSingleFactorScore), fg="#d12c3f")
            lblSFScoreRight.config(text="{}".format(compareSingleFactorScore), fg="#2d802f")
            lblSFDesc.config(
                text="The   {}   configuration's Starting Population, Security Level, and IDS Usage scores indicate improved S population size and minimzed chance of node Infection and Death".format(
                    self.compareConfiguration.Name[9:]))
        if activeSingleFactorScore > compareSingleFactorScore:
            lblSFScoreLeft.config(text="{}".format(activeSingleFactorScore), fg="#2d802f")
            lblSFScoreRight.config(text="{}".format(compareSingleFactorScore), fg="#d12c3f")
            lblSFDesc.config(
                text="The   {}   configuration's Starting Population, Security Level, and IDS Usage scores indicate improved S population size and minimzed chance of node Infection and Death".format(
                    self.activeConfiguration.Name[9:]))
        if activeSingleFactorScore == compareSingleFactorScore:
            lblSFScoreLeft.config(text="{}".format(activeSingleFactorScore), fg="#e68f39")
            lblSFScoreRight.config(text="{}".format(compareSingleFactorScore), fg="#e68f39")
            lblSFDesc.config(
                text="Both configuration's Starting Population, Security Level, and IDS Usage scores are equal; affecting both configurations S population size, and node Infection and Death rates equally.")

        explainFrame.place(x=20, y=15)
        lblExplain.pack(expand=True, fill="both")
        comparisonFrame.place(x=20, y=140)
        lblLeft.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        lblRight.grid(row=0, column=2, sticky="ew", pady=(0, 15))
        lblNeighbourLeft.grid(row=1, column=0, sticky="ew")
        lblNeighbourScoreLeft.grid(row=2, column=0, sticky="ew")
        lblNeighbourRight.grid(row=1, column=2, sticky="ew")
        lblNeighbourScoreRight.grid(row=2, column=2, sticky="ew")
        lblNeighbourDesc.grid(row=2, column=1, sticky="ew")
        lblInfLeft.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        lblInfScoreLeft.grid(row=4, column=0, sticky="ew")
        lblInfRight.grid(row=3, column=2, sticky="ew", pady=(20, 0))
        lblInfScoreRight.grid(row=4, column=2, sticky="ew")
        lblInfDesc.grid(row=4, column=1, sticky="ew")
        lblEffortLeft.grid(row=5, column=0, sticky="ew", pady=(20, 0))
        lblEffortScoreLeft.grid(row=6, column=0, sticky="ew")
        lblEffortRight.grid(row=5, column=2, sticky="ew", pady=(20, 0))
        lblEffortScoreRight.grid(row=6, column=2, sticky="ew")
        lblEffortDesc.grid(row=6, column=1, sticky="ew")
        lblDthLeft.grid(row=7, column=0, sticky="ew", pady=(20, 0))
        lblDthScoreLeft.grid(row=8, column=0, sticky="ew")
        lblDthRight.grid(row=7, column=2, sticky="ew", pady=(20, 0))
        lblDthScoreRight.grid(row=8, column=2, sticky="ew")
        lblDthDesc.grid(row=8, column=1, sticky="ew")
        lblSFLeft.grid(row=9, column=0, sticky="ew", pady=(20, 0))
        lblSFScoreLeft.grid(row=10, column=0, sticky="ew")
        lblSFRight.grid(row=9, column=2, sticky="ew", pady=(20, 0))
        lblSFScoreRight.grid(row=10, column=2, sticky="ew")
        lblSFDesc.grid(row=10, column=1, sticky="ew")
