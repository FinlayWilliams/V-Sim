import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class SISInspectInterface(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.index = 0

        #################################### Instantiating Information Frame ########################################
        # These are the basic controls of this page alling the user to navigate
        mainFrame = tk.Frame(self, bg="#574b59")
        controlBar = tk.Frame(mainFrame, bg="#453354")
        btnReturn = tk.Button(controlBar, wraplength=41, width=7, text="Return Home", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                              command=lambda: controller.display("SISInspectInterface", "HomeInterface"))
        self.lblControl = tk.Label(controlBar, bg="#453354", text="", font=("Arial", 14, "italic"), fg="white" )
        btnOverview = tk.Button(mainFrame, text="Overview", font=("Arial", 9), width=17, command=lambda : self.switchInfoFrame(0, 1))
        btnSingleFactors = tk.Button(mainFrame, text="Single Factors", font=("Arial", 9), width=17, command=lambda : self.switchInfoFrame(1, 1))
        btnNeighbourSet = tk.Button(mainFrame, text="Neighbour Sets", font=("Arial", 9), width=17, command=lambda : self.switchInfoFrame(2, 1))
        btnInfectionRate = tk.Button(mainFrame, text="Infection Rates", font=("Arial", 9), width=17, command=lambda : self.switchInfoFrame(3, 1))
        btnEffort = tk.Button(mainFrame, text="Payload Effort", font=("Arial", 9), width=17, command=lambda : self.switchInfoFrame(4, 1))
        btnDeath = tk.Button(mainFrame, text="Death Rates", font=("Arial", 9), width=17, command=lambda : self.switchInfoFrame(5, 1))

        # This area will contain the assessment and a starter list is created
        self.informationFrame = tk.Frame(mainFrame, bg="#e0e0e0")
        self.frames = [tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                       tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                       tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0")]

        # This is the legend footer of the page
        lblLegend1 = tk.Label(mainFrame, bg="#2ca02c", width=25, pady=4, text="(S) Susceptible", font=("Arial", 9), fg="white")
        lblLegend2 = tk.Label(mainFrame, bg="#9467bd", width=25, pady=4, text="(IR) Random-Scanning", font=("Arial", 9), fg="white")
        lblLegend3 = tk.Label(mainFrame, bg="#1f77b4", width=27, pady=4, text="(IL) Local-Scanning", font=("Arial", 9), fg="white")
        lblLegend4 = tk.Label(mainFrame, bg="#17becf", width=27, pady=4, text="(IP) Peer-to-Peer", font=("Arial", 9), fg="white")
        lblLegend5 = tk.Label(mainFrame, bg="#d62728", width=27, pady=4, text="(I) Infection Types Grouped", font=("Arial", 9), fg="white")

        # This contains all graph-side widgets
        graphFrame = tk.Frame(self, bg="#453354")
        self.lblGraphTitle = tk.Label(graphFrame, bg="#453354", text="Assessment Overview", font=("Arial", 14, "italic"), fg="white")
        btnConfigure = tk.Button(graphFrame, wraplength=60, width=10, text="Control Configuration", font=("Arial", 7), relief="ridge", fg="white", bg="#6e6e6e",
                                 command=lambda: controller.display("SISInspectInterface", "SISControlInterface"))
        graphContainer = tk.Frame(graphFrame, bg="#654e78")
        figure = plt.figure(facecolor="#654e78")
        self.canvas = FigureCanvasTkAgg(figure, graphContainer)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.ax = [figure.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(3):
            self.ax[x].ticklabel_format(style="plain")
        figure.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)

        self.lblFinalN = tk.Label(graphFrame, bg="#654e78", fg="black", font=("Arial", 12))

        ########################################### Placing Everything ###############################################
        mainFrame.place(relheight=1, relwidth=0.6)
        controlBar.place(relheight=0.087, relwidth=1)
        btnReturn.place(x=21, y=21)
        self.lblControl.pack(ipady=21)
        btnOverview.place(x=15, y=87)
        btnSingleFactors.place(x=166, y=87)
        btnNeighbourSet.place(x=317, y=87)
        btnInfectionRate.place(x=469, y=87)
        btnEffort.place(x=622, y=87)
        btnDeath.place(x=778, y=87)
        self.informationFrame.place(x=14, y=124, relheight=0.83, relwidth=0.97)
        lblLegend1.place(x=0, y=837)
        lblLegend2.place(x=172, y=837)
        lblLegend3.place(x=353, y=837)
        lblLegend4.place(x=548, y=837)
        lblLegend5.place(x=731, y=837)
        # Graphs
        graphFrame.place(x=922, y=0, relheight=1, relwidth=0.4)
        self.lblGraphTitle.pack(ipady=21, padx=(0, 30))
        btnConfigure.place(x=530, y=21)
        graphContainer.place(x=5, y=75, relheight=0.96, relwidth=1)
        self.lblFinalN.place(x=150, y=835)
        self.updateGraphs()

    # Updates the on-screen graphs
    def updateGraphs(self):
        S1, Ir1, Il1, Ip1 = self.controller.activeConfiguration.runSimulation()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.controller.activeConfiguration.Timesteps, 500)

        # Setting the title
        self.lblGraphTitle.config(text="{} - Virus Propagation".format(self.controller.activeConfiguration.Name))

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(3)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
        self.ax[0].plot(T1, Il1, "#1f77b4", label="Local-Scanning Infected")
        self.ax[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
        self.ax[0].set_xlabel("Timesteps (Hours)")
        self.ax[0].set_ylabel("Node Count")
        self.ax[0].set_title("Node Population Sizes Over Time - S, IR, IL, IP")
        self.ax[0].axvline(linewidth=0.5, color="#a8a8a8", x=self.controller.activeConfiguration.Timesteps / 2, linestyle="--")
        # Plotting the second graph
        self.ax[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.ax[1].plot(T1, I1, '#d62728', label="All Infected")
        self.ax[1].set_xlabel("Timesteps (Hours)")
        self.ax[1].set_ylabel("Node Count")
        self.ax[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        self.ax[1].axvline(linewidth=0.5, color="#a8a8a8", x=self.controller.activeConfiguration.Timesteps / 2, linestyle="--")
        self.ax[1].axhline(linewidth=0.5, color="#d62728", y=max(I1), linestyle="--")
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
            self.ax[2].pie(pop, labels=label, colors=colour)
            self.ax[2].set_title("Population Sizes on Final Recorded Hour #{}".format(self.controller.activeConfiguration.Timesteps))
        else:
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning Infected: {:.0f}".format(pop[1]),
                      "Local Scanning Infected: {:.0f}".format(pop[2]), "Peer-to-Peer Infected: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.ax[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True, labeldistance=1.2)
            self.ax[2].set_title(
                "Population Sizes on Final Recorded Hour ({})".format(self.controller.activeConfiguration.Timesteps))

        self.lblFinalN.config(text="Population Sizes Totalled (Final N Value): {:.0f}".format(S1[-1] + I1[-1], self.controller.activeConfiguration.N))

        self.canvas.draw()

    # Called each time the page is set to display the assessment of the current models
    # also provides the functionality to switch between the frames
    def switchInfoFrame(self, index, stub):
        if index == 0:
            self.frames[self.index].pack_forget()
            self.index = 0
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Assessment Overview")
        if index == 1:
            self.frames[self.index].pack_forget()
            self.index = 1
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Single Factors")
        if index == 2:
            self.frames[self.index].pack_forget()
            self.index = 2
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Neighbour Sets")
        if index == 3:
            self.frames[self.index].pack_forget()
            self.index = 3
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Infection Rates")
        if index == 4:
            self.frames[self.index].pack_forget()
            self.index = 4
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Payload Effort")
        if index == 5:
            self.frames[self.index].pack_forget()
            self.index = 5
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Death Rates")

    # Populates all of the information frames, ready to be deployed, the bulk of content on this page
    def populateFrames(self):
        # This loop ensures the frames are destroyed and reconstructed with correct information when the frame is opened
        if self.frames:
            for frame in self.frames:
                frame.destroy()

            self.frames = [tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                           tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                           tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0")]

        # Configuration prefix made small due to need to reuse
        config = self.controller.activeConfiguration

        ovrSingleFactorScore, finalNScore, startingPopScore, rrScore, idsScore, ovrNeighbourScore, slocScore, \
        snhbScore, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore, ovrEffortScore, \
        tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, depAreaScore, ovrDeathRateScore, \
        benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore = config.calculateScores()

        # This section populates each of the frames with updated information conforming to the active models simulation
        # by calling the methods that add the page widgets
        # There are many if statements indicating thresholds that change the displayed information
        self.populateOverview(config, ovrSingleFactorScore, ovrNeighbourScore, ovrInfectionScore, ovrEffortScore, ovrDeathRateScore)
        self.populateUncategorisedFrame(config, ovrSingleFactorScore, finalNScore, startingPopScore, rrScore, idsScore)
        self.populateNeighbourFrame(config, ovrNeighbourScore, slocScore, snhbScore)
        self.populateInfectionFrame(config, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore)
        self.populateEffortFrame(config, ovrEffortScore, tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, depAreaScore)
        self.populateDeathFrame(config, ovrDeathRateScore, benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore)

    # The following 8 methods are the assessment frame contents
    def populateOverview(self, C, ovrSingleFactorScore, ovrNeighbourScore, ovrInfectionScore, ovrEffortScore, ovrDeathRateScore):
        Jeff = 0

        lbl1 = tk.Label(self.frames[0], text="{} - Assessment Overview and Simulation Scores".format(C.Name), font=("Arial", 12), bg="#e0e0e0")

        lblScoreAc = tk.Label(self.frames[0], text="{}  | ".format(ovrSingleFactorScore + ovrNeighbourScore + ovrInfectionScore + ovrEffortScore + ovrDeathRateScore), font=("Arial", 11, "bold"),
                              bg="#e0e0e0")
        lblScoreAc2 = tk.Label(self.frames[0], font=("Arial", 11, "bold"), bg="#e0e0e0")
        lblScore = tk.Label(self.frames[0], text="> Overall Simulation Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblScoreAc2.config(text="Low", fg="#2d802f")
            lblScoreDes.config(
                text="This model has a configuration that results in a generally slower and less potent propagation.")
        if 1 <= Jeff < 3:
            lblScoreAc2.config(text="Medium", fg="#b35827")
            lblScoreDes.config(text="This model has a configuration that results in an average propagation of a virus.")
        if Jeff >= 3:
            lblScoreAc2.config(text="High", fg="#b81d28")
            lblScoreDes.config(
                text="This model has a configuration that results in a fast and potent virus propagation.")

        lblExplain = tk.Label(self.frames[0],
                              text="The assessment is broken down into different categories and combine to produce an overall score and explanatory breakdown",
                              font=("Arial", 10, "italic"), bg="#e0e0e0")
        lblExplain2 = tk.Label(self.frames[0], text="for how potent the virus propagation is or is not. The scores for those categories are as follow:",
                               font=("Arial", 10, "italic"), bg="#e0e0e0")

        lblPopScoreAc = tk.Label(self.frames[0], text="{}  | ".format(ovrSingleFactorScore), font=("Arial", 11, "bold"),
                                 bg="#e0e0e0")
        lblPopScoreAc2 = tk.Label(self.frames[0], font=("Arial", 11, "bold"), bg="#e0e0e0")
        lblPopScore = tk.Label(self.frames[0], text="> Population Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblPopScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblPopScoreAc2.config(text="Low", fg="#2d802f")
            lblPopScoreDes.config(text="The pre and post population sizes are weighted towards the Susceptible")
        if 1 <= Jeff < 3:
            lblPopScoreAc2.config(text="Medium", fg="#e68f39")
            lblPopScoreDes.config(text="The pre and post population sizes are equally weighted.")
        if Jeff >= 3:
            lblPopScoreAc2.config(text="High", fg="#b81d28")
            lblPopScoreDes.config(text="The pre and post population sizes are weighted heavily towards the Infected.")

        lblSizeScoreAc = tk.Label(self.frames[0], text="{}  | ".format(ovrNeighbourScore), font=("Arial", 11, "bold"),
                                  bg="#e0e0e0")
        lblSizeScoreAc2 = tk.Label(self.frames[0], font=("Arial", 11, "bold"), bg="#e0e0e0")
        lblSizeScore = tk.Label(self.frames[0], text="> Physical Size Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblSizeScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblSizeScoreAc2.config(text="Low", fg="#2d802f")
            lblSizeScoreDes.config(text="The Physical Size of the network makes life difficult for the Infected.")
        if 1 <= Jeff < 3:
            lblSizeScoreAc2.config(text="Medium", fg="#e68f39")
            lblSizeScoreDes.config(
                text="The Physical Size of the network makes life evenly uneasy for both the Infected and Susceptible")
        if Jeff >= 3:
            lblSizeScoreAc2.config(text="High", fg="#b81d28")
            lblSizeScoreDes.config(text="The Physical Size of the network makes life difficult for the Susceptible.")

        lblNeighbourScoreAc = tk.Label(self.frames[0], text="{}  | ".format(ovrInfectionScore), font=("Arial", 11, "bold"),
                                       bg="#e0e0e0")
        lblNeighbourScoreAc2 = tk.Label(self.frames[0], font=("Arial", 11, "bold"), bg="#e0e0e0")
        lblNeighbourScore = tk.Label(self.frames[0], text="> Neighbour Set Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblNeighbourScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblNeighbourScoreAc2.config(text="Low", fg="#2d802f")
            lblNeighbourScoreDes.config(text="The Neighbour Sets make virus propagation difficult.")
        if 1 <= Jeff < 3:
            lblNeighbourScoreAc2.config(text="Medium", fg="#e68f39")
            lblNeighbourScoreDes.config(text="The Neighbour Sets make virus propagation slightly easier.")
        if Jeff >= 3:
            lblNeighbourScoreAc2.config(text="High", fg="#b81d28")
            lblNeighbourScoreDes.config(text="The Neighbour Sets make virus propagation easy.")

        lblInfRateScoreAc = tk.Label(self.frames[0], text="{}  | ".format(ovrEffortScore),
                                     font=("Arial", 11, "bold"), bg="#e0e0e0")
        lblInfRateScoreAc2 = tk.Label(self.frames[0], font=("Arial", 11, "bold"), bg="#e0e0e0")
        lblInfRateScore = tk.Label(self.frames[0], text="> Infection Rates Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblInfRateScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblInfRateScoreAc2.config(text="Low", fg="#2d802f")
            lblInfRateScoreDes.config(text="The infection rates are very low.")
        if 1 <= Jeff < 3:
            lblInfRateScoreAc2.config(text="Medium", fg="#e68f39")
            lblInfRateScoreDes.config(text="The infection rates are creeping up.")
        if Jeff >= 3:
            lblInfRateScoreAc2.config(text="High", fg="#b81d28")
            lblInfRateScoreDes.config(text="The infection rates are very high.")

        lblDeathRateScoreAc = tk.Label(self.frames[0], text="{}  | ".format(ovrDeathRateScore), font=("Arial", 11, "bold"),
                                       bg="#e0e0e0")
        lblDeathRateScoreAc2 = tk.Label(self.frames[0], font=("Arial", 11, "bold"), bg="#e0e0e0")
        lblDeathRateScore = tk.Label(self.frames[0], text="> Death Rates Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblDeathRateScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblDeathRateScoreAc2.config(text="Low", fg="#2d802f")
            lblDeathRateScoreDes.config(
                text="The death rates are very high for the Infected Nodes; Mass virus propagation is difficult.")
        if 1 <= Jeff < 3:
            lblDeathRateScoreAc2.config(text="Medium", fg="#e68f39")
            lblDeathRateScoreDes.config(
                text="The death rates are mild for the Infected Nodes; Viruses are propagating.")
        if Jeff >= 3:
            lblDeathRateScoreAc2.config(text="High", fg="#b81d28")
            lblDeathRateScoreDes.config(
                text="The death rates are very low for the Infected Nodes; The Infected have plenty of time to propagate viruses!")


        lblExplain3 = tk.Label(self.frames[0], text="The overall score ranges from a minimum of ___ to ___ and to a maximum of ___",
                               font=("Arial", 10, "italic"), bg="#e0e0e0")
        lblExplain4 = tk.Label(self.frames[0], text="Below ___ is a Low Score - an Ideal Model Score for Minimal Virus Propagation, ", font=("Arial", 10, "italic"), bg="#e0e0e0",
                               fg="#2d802f")
        lblExplain5 = tk.Label(self.frames[0], text="Between ___ and ___ is Medium Score - a Sub-Optimal Score but Relatively Safe,", font=("Arial", 10, "italic"),
                               bg="#e0e0e0", fg="#e68f39")
        lblExplain6 = tk.Label(self.frames[0], text="Above ___ is Higher Score - a Dangerous Score Indicating Optimal Conditions for Virus Propagation", font=("Arial", 10, "italic"), bg="#e0e0e0",
                               fg="#b81d28")
        lblExplain7 = tk.Label(self.frames[0],
                               text="Press the labelled buttons above to inspect the correspoinding categories' score breakdown.",
                               font=("Arial", 10, "italic"), bg="#e0e0e0")

        lbl1.grid(row=0, column=2, sticky="w", pady=(7, 15), padx=(7, 0))

        lblScoreAc.grid(row=1, column=0, sticky="w", padx=(7, 0))
        lblScoreAc2.grid(row=1, column=1, sticky="w")
        lblScore.grid(row=1, column=2, sticky="w")
        lblScoreDes.grid(row=2, column=2, sticky="w", padx=(7, 0))

        lblExplain.grid(row=3, column=2, sticky="w", pady=(10, 0), padx=(7, 0))
        lblExplain2.grid(row=4, column=2, sticky="w", pady=(0, 10), padx=(7, 0))

        lblPopScoreAc.grid(row=5, column=0, sticky="w", padx=(7, 0))
        lblPopScoreAc2.grid(row=5, column=1, sticky="w")
        lblPopScore.grid(row=5, column=2, sticky="w")
        lblPopScoreDes.grid(row=6, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblSizeScoreAc.grid(row=7, column=0, sticky="w", padx=(7, 0))
        lblSizeScoreAc2.grid(row=7, column=1, sticky="w")
        lblSizeScore.grid(row=7, column=2, sticky="w")
        lblSizeScoreDes.grid(row=8, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblNeighbourScoreAc.grid(row=9, column=0, sticky="w", padx=(7, 0))
        lblNeighbourScoreAc2.grid(row=9, column=1, sticky="w")
        lblNeighbourScore.grid(row=9, column=2, sticky="w")
        lblNeighbourScoreDes.grid(row=10, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblInfRateScoreAc.grid(row=11, column=0, sticky="w", padx=(7, 0))
        lblInfRateScoreAc2.grid(row=11, column=1, sticky="w")
        lblInfRateScore.grid(row=11, column=2, sticky="w")
        lblInfRateScoreDes.grid(row=12, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblDeathRateScoreAc.grid(row=13, column=0, sticky="w", padx=(7, 0))
        lblDeathRateScoreAc2.grid(row=13, column=1, sticky="w")
        lblDeathRateScore.grid(row=13, column=2, sticky="w")
        lblDeathRateScoreDes.grid(row=14, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblExplain3.grid(row=17, column=2, sticky="w", pady=(15, 0), padx=(7, 0))
        lblExplain4.grid(row=18, column=2, sticky="w", padx=(7, 0))
        lblExplain5.grid(row=19, column=2, sticky="w", padx=(7, 0))
        lblExplain6.grid(row=20, column=2, sticky="w", padx=(7, 0))

        lblExplain7.grid(row=21, column=2, stick="w", pady=(15, 0), padx=(7, 0))

    def populateUncategorisedFrame(self, C, ovrUncategorisedScore, finalNScore, startingPopScore, rrScore, idsScore):
        pass

    def populateNeighbourFrame(self, C, ovrNeighbourScore, slocScore, snhbScore):
        pass

    def populateInfectionFrame(self, C, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore):
        pass

    def populateEffortFrame(self, C, ovrEffortScore, tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, depAreaScore):
        pass

    def populateDeathFrame(self, C, ovrDeathRateScore, benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore):
        pass
