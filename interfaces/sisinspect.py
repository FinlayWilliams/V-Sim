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
        btnOverview = tk.Button(mainFrame, text="Overview", font=("Arial", 9), width=21, command=lambda : self.switchInfoFrame(0, 1))
        btnNeighbourSet = tk.Button(mainFrame, text="Neighbour Sets", font=("Arial", 9), width=21, command=lambda : self.switchInfoFrame(1, 1))
        btnInfectionRate = tk.Button(mainFrame, text="Infection Rates", font=("Arial", 9), width=21, command=lambda : self.switchInfoFrame(2, 1))
        btnEffort = tk.Button(mainFrame, text="Payload Effort", font=("Arial", 9), width=21, command=lambda : self.switchInfoFrame(3, 1))
        btnDeath = tk.Button(mainFrame, text="Death Rates", font=("Arial", 9), width=21, command=lambda : self.switchInfoFrame(4, 1))
        btnSingleFactors = tk.Button(mainFrame, text="Single Factors", font=("Arial", 9), width=21, command=lambda : self.switchInfoFrame(5, 1))

        # This area will contain the assessment and a starter list is created
        self.informationFrame = tk.Frame(mainFrame, bg="#e0e0e0")
        self.frames = [tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                       tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                       tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0")]

        # This is the legend footer of the page
        lblLegend1 = tk.Label(mainFrame, bg="#2ca02c", width=32, pady=4, text="(S) Susceptible", font=("Arial", 9), fg="white")
        lblLegend2 = tk.Label(mainFrame, bg="#9467bd", width=32, pady=4, text="(IR) Random-Scanning", font=("Arial", 9), fg="white")
        lblLegend3 = tk.Label(mainFrame, bg="#1f77b4", width=32, pady=4, text="(IL) Local-Scanning", font=("Arial", 9), fg="white")
        lblLegend4 = tk.Label(mainFrame, bg="#17becf", width=32, pady=4, text="(IP) Peer-to-Peer", font=("Arial", 9), fg="white")
        lblLegend5 = tk.Label(mainFrame, bg="#d62728", width=33, pady=4, text="(I) Infection Types Grouped", font=("Arial", 9), fg="white")

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

        self.lblFinalN = tk.Label(graphFrame, bg="#654e78", fg="black", font=("Arial", 13))

        ########################################### Placing Everything ###############################################
        mainFrame.place(relheight=1, relwidth=0.6)
        controlBar.place(relheight=0.07, relwidth=1)
        btnReturn.place(x=21, y=21)
        self.lblControl.pack(ipady=21)
        btnOverview.place(x=15, y=87)
        btnNeighbourSet.place(x=207, y=87)
        btnInfectionRate.place(x=399, y=87)
        btnEffort.place(x=591, y=87)
        btnDeath.place(x=975, y=87)
        btnSingleFactors.place(x=778, y=87)
        self.informationFrame.place(x=14, y=124, relheight=0.85, relwidth=0.97)
        lblLegend1.place(x=0, y=1021)
        lblLegend2.place(x=230, y=1021)
        lblLegend3.place(x=460, y=1021)
        lblLegend4.place(x=690, y=1021)
        lblLegend5.place(x=920, y=1021)
        # Graphs
        graphFrame.place(x=1152, y=0, relheight=1, relwidth=0.4)
        self.lblGraphTitle.pack(ipady=21, padx=(0, 30))
        btnConfigure.place(x=680, y=21)
        graphContainer.place(x=5, y=75, relheight=0.94, relwidth=1)
        self.lblFinalN.place(x=250, y=1000)
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
            self.lblControl.config(text="Neighbour Sets")
        if index == 2:
            self.frames[self.index].pack_forget()
            self.index = 2
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Infection Rates")
        if index == 3:
            self.frames[self.index].pack_forget()
            self.index = 3
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Payload Effort")
        if index == 4:
            self.frames[self.index].pack_forget()
            self.index = 4
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Lifespans and Death rates")
        if index == 5:
            self.frames[self.index].pack_forget()
            self.index = 5
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Single Factors")

    # Populates all of the information frames, ready to be deployed, the bulk of content on this page
    def populateFrames(self):
        # This loop ensures the frames are destroyed and reconstructed with correct information when the frame is opened
        if self.frames:
            for frame in self.frames:
                frame.destroy()

            self.frames = [tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                           tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                           tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0")]

        # Configuration prefix made small here in in the following methods due to need to reuse
        config = self.controller.activeConfiguration
        S1, Ir1, Il1, Ip1 = config.runSimulation()

        ovrSingleFactorScore, startingPopScore, rrScore, idsScore, ovrNeighbourScore, slocScore, \
        snhbScore, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore, ovrEffortScore, \
        tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, depAreaScore, ovrDeathRateScore, \
        benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore = config.calculateScores()

        # This section populates each of the frames with updated information conforming to the active models simulation
        # by calling the methods that add the page widgets
        # There are many if statements indicating thresholds that change the displayed information
        self.populateOverview(config, ovrSingleFactorScore, ovrNeighbourScore, ovrInfectionScore, ovrEffortScore, ovrDeathRateScore)
        self.populateNeighbourFrame(config, ovrNeighbourScore, slocScore, snhbScore)
        self.populateInfectionFrame(config, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore)
        self.populateEffortFrame(config, ovrEffortScore, tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, depAreaScore)
        self.populateDeathFrame(config, ovrDeathRateScore, benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore)
        self.populateSingleFactorFrame(config, ovrSingleFactorScore, startingPopScore, rrScore, idsScore)

    # The following 8 methods are the assessment frame contents
    def populateOverview(self, C, ovrSingleFactorScore, ovrNeighbourScore, ovrInfectionScore, ovrEffortScore, ovrDeathRateScore):
        Jeff = 0

        lbl1 = tk.Label(self.frames[0], text="{} - Assessment Overview and Simulation Scores".format(C.Name), font=("Arial", 12), bg="#e0e0e0")

        lblScoreAc = tk.Label(self.frames[0], text="{}  ".format(ovrSingleFactorScore + ovrNeighbourScore + ovrInfectionScore + ovrEffortScore + ovrDeathRateScore), font=("Arial", 14, "bold"), bg="#e0e0e0")
        lblScore = tk.Label(self.frames[0], text="> Overall Simulation Score", font=("Arial", 12, "bold", "italic"), bg="#e0e0e0")
        lblScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblScoreAc.config(fg="#2d802f")
            lblScoreDes.config(text="This model has a configuration that results in a generally slower and less potent propagation.")
        if 1 <= Jeff < 3:
            lblScoreAc.config(fg="#b35827")
            lblScoreDes.config(text="This model has a configuration that results in an expected / average propagation of a virus.")
        if Jeff >= 3:
            lblScoreAc.config(fg="#b81d28")
            lblScoreDes.config(text="This configuration results in a fast and potent virus propagation.")

        lblExplain = tk.Label(self.frames[0], text="The assessment is broken down into different categories and combine to produce an overall score and explanatory breakdown\n", font=("Arial", 10, "italic"), bg="#e0e0e0")

        lblNeighbourScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrNeighbourScore), font=("Arial", 12, "bold"), bg="#e0e0e0")
        lblNeighbourScore = tk.Label(self.frames[0], text="> Neighbour Sets Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblNeighbourScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblNeighbourScoreV.config(fg="#2d802f")
            lblNeighbourScoreDes.config(text="This section looks into the attack surface of Local Scanning (IL) and Peer-to-Peer (IP) infection methods as the proportion "
                                             "of the Susceptible (S) population they can target is limited, unlike Random Scanning (IR). \n\n"
                                             "In this simulation, the Neighbour Sets make for small attack ranges. The Local Scanning and Peer-to-Peer infection methods are capped severly.")
        if 1 <= Jeff < 3:
            lblNeighbourScoreV.config(fg="#e68f39")
            lblNeighbourScoreDes.config(text="This section looks into the attack surface of Local Scanning (IL) and Peer-to-Peer (IP) infection methods as the proportion "
                                             "of the Susceptible (S) population they can target is limited, unlike Random Scanning (IR). \n\n"
                                             "In this simulation, the Neighbour Sets make for average attack ranges. The Local Scanning and Peer-to-Peer infection have enough of an attack vector to do damage.")
        if Jeff >= 3:
            lblNeighbourScoreV.config(fg="#b81d28")
            lblNeighbourScoreDes.config(text="This section looks into the attack surface of Local Scanning (IL) and Peer-to-Peer (IP) infection methods as the proportion "
                                             "of the Susceptible (S) population they can target is limited, unlike Random Scanning (IR). \n\n"
                                             "In this simulation, the Neighbour Sets make for large attack ranges. The Local Scanning and Peer-to-Peer infection methods can reach a huge amount of the population.")

        lblInfScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrInfectionScore), font=("Arial", 12, "bold"), bg="#e0e0e0")
        lblInfScore = tk.Label(self.frames[0], text="> Infection Rates Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblInfScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblInfScoreV.config(fg="#2d802f")
            lblInfScoreDes.config(text="The Infection Rates section explores the calculated rates that describe how well an Infected (I) Node propagates the infection. \n\n"
                                       "The calculated Infection Rates are low, a minimal propagation of the botnet has been achieved.")
        if 1 <= Jeff < 3:
            lblInfScoreV.config(fg="#e68f39")
            lblInfScoreDes.config(text="The Infection Rates section explores the calculated rates that describe how well an Infected (I) Node propagates the infection. \n\n"
                                       "The calculated Infection Rates are average, an expected propagation of the botnet has occured.")
        if Jeff >= 3:
            lblInfScoreV.config(fg="#b81d28")
            lblInfScoreDes.config(text="The Infection Rates section explores the calculated rates that describe how well an Infected (I) Node propagates the infection. \n\n"
                                       "The calculated Infection Rates are high, a maxiaml propagation of the botnet has occured.")

        lblEffortScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrEffortScore), font=("Arial", 12, "bold"), bg="#e0e0e0")
        lblEffortScore = tk.Label(self.frames[0], text="> Payload Effort Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblEffortScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblEffortScoreV.config(fg="#2d802f")
            lblEffortScoreDes.config(text="The Payload Effort section analyses the factors contributing to the amount of 'Effort' both Susceptible (S) and Infected (I) Nodes "
                                          "exert when sending data across the network to other Nodes. \n\n"
                                          "Here, the Effort required to send payloads of information across the network to other nodes is minimal, better than average.")
        if 1 <= Jeff < 3:
            lblEffortScoreV.config(fg="#e68f39")
            lblEffortScoreDes.config(text="The Payload Effort section analyses the factors contributing to the amount of 'Effort' both Susceptible (S) and Infected (I) Nodes "
                                          "exert when sending data across the network to other Nodes. \n\n"
                                          "Here, the Effort required to send payloads of information across the network to other nodes is average, the expected effort.")
        if Jeff >= 3:
            lblEffortScoreV.config(fg="#b81d28")
            lblEffortScoreDes.config(text="The Payload Effort section analyses the factors contributing to the amount of 'Effort' both Susceptible (S) and Infected (I) Nodes "
                                          "exert when sending data across the network to other Nodes. \n\n"
                                          "Here, the Effort required to send payloads of information across the network to other nodes is large, making life difficult for Nodes.")

        lblDthScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrDeathRateScore), font=("Arial", 12, "bold"), bg="#e0e0e0")
        lblDthScore = tk.Label(self.frames[0], text="> Lifespan and Death Rates Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblDthScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblDthScoreV.config(fg="#2d802f")
            lblDthScoreDes.config(text="This section examines the factors contributing to both Susceptible (S) and Infected (I) Nodes' Lifespans, and the corresponding Death Rates. \n\n"
                                       "This configuration results in high Lifespans and low Death Rates. Nodes live extended durations and malicious activity is minimal.")
        if 1 <= Jeff < 3:
            lblDthScoreV.config(fg="#e68f39")
            lblDthScoreDes.config(text="This section examines the factors contributing to both Susceptible (S) and Infected (I) Nodes' Lifespans, and the corresponding Death Rates. \n\n"
                                       "The node Lifespans are average, as well as the Death Rates. Nodes live the expected durations and malicious activity is present.")
        if Jeff >= 3:
            lblDthScoreV.config(fg="#b81d28")
            lblDthScoreDes.config(text="This section examines the factors contributing to both Susceptible (S) and Infected (I) Nodes' Lifespans, and the corresponding Death Rates. \n\n"
                                       "This configuration results in low Lifespans and high Death Rates. Nodes live reduced durations and malicious activity is substantial.")

        lblSFScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrSingleFactorScore), font=("Arial", 12, "bold"), bg="#e0e0e0")
        lblSFScore = tk.Label(self.frames[0], text="> Single Factor Scores", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblSFScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblSFScoreV.config(fg="#2d802f")
            lblSFScoreDes.config(text="This section looks at three particular starting conditions: Starting Population Sizes, Admin Engagement, and Intrusion Detection System"
                                      " (IDS) usage. \n\n"
                                      "In this simulation, these Single Factors have helped achieve a minimal virus propagation.")
        if 1 <= Jeff < 3:
            lblSFScoreV.config(fg="#e68f39")
            lblSFScoreDes.config(text="This section looks at three particular starting conditions: Starting Population Sizes, Admin Engagement, and Intrusion Detection System"
                                      " (IDS) usage. \n\n"
                                      "In this simulation, these Single Factors are at the expected thresholds and result in the expected botnet presence.")
        if Jeff >= 3:
            lblSFScoreV.config(fg="#b81d28")
            lblSFScoreDes.config(text="This section looks at three particular starting conditions: Starting Population Sizes, Admin Engagement, and Intrusion Detection System"
                                      " (IDS) usage. \n\n"
                                      "In this simulation, these Single Factors have contributed to a higher virus propagation.")


        lblExplain3 = tk.Label(self.frames[0], text="The overall score ranges from a minimum of ___ to ___ and to a maximum of ___", font=("Arial", 10, "italic"), bg="#e0e0e0")
        lblExplain4 = tk.Label(self.frames[0], text="Below ___ is a High Score - an Ideal Model Score for Minimal Virus Propagation, ", font=("Arial", 10, "italic"), bg="#e0e0e0", fg="#2d802f")
        lblExplain5 = tk.Label(self.frames[0], text="Between ___ and ___ is Medium Score - a Sub-Optimal Score but Relatively Safe,", font=("Arial", 10, "italic"), bg="#e0e0e0", fg="#e68f39")
        lblExplain6 = tk.Label(self.frames[0], text="Above ___ is Lower Score - a Dangerous Score Indicating Optimal Conditions for Virus Propagation", font=("Arial", 10, "italic"), bg="#e0e0e0", fg="#b81d28")
        lblExplain7 = tk.Label(self.frames[0], text="Press the labelled buttons above to inspect the correspoinding categories' score breakdown.", font=("Arial", 10, "italic"), bg="#e0e0e0")

        lbl1.grid(row=0, column=2, sticky="w", pady=(7, 15), padx=(7, 0))

        lblScoreAc.grid(row=1, column=0, sticky="w", padx=(9, 0))
        lblScore.grid(row=1, column=2, sticky="w")
        lblScoreDes.grid(row=2, column=2, sticky="w", padx=(7, 0))

        lblExplain.grid(row=3, column=2, sticky="w", pady=(10, 0), padx=(7, 0))

        lblNeighbourScoreV.grid(row=5, column=0, sticky="w", padx=(9, 0))
        lblNeighbourScore.grid(row=5, column=2, sticky="w")
        lblNeighbourScoreDes.grid(row=6, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblInfScoreV.grid(row=7, column=0, sticky="w", padx=(9, 0))
        lblInfScore.grid(row=7, column=2, sticky="w")
        lblInfScoreDes.grid(row=8, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblEffortScoreV.grid(row=9, column=0, sticky="w", padx=(9, 0))
        lblEffortScore.grid(row=9, column=2, sticky="w")
        lblEffortScoreDes.grid(row=10, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblDthScoreV.grid(row=11, column=0, sticky="w", padx=(9, 0))
        lblDthScore.grid(row=11, column=2, sticky="w")
        lblDthScoreDes.grid(row=12, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblSFScoreV.grid(row=13, column=0, sticky="w", padx=(9, 0))
        lblSFScore.grid(row=13, column=2, sticky="w")
        lblSFScoreDes.grid(row=14, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblExplain3.grid(row=17, column=2, sticky="w", pady=(15, 0), padx=(7, 0))
        lblExplain4.grid(row=18, column=2, sticky="w", padx=(7, 0))
        lblExplain5.grid(row=19, column=2, sticky="w", padx=(7, 0))
        lblExplain6.grid(row=20, column=2, sticky="w", padx=(7, 0))

        lblExplain7.grid(row=21, column=2, stick="w", pady=(15, 0), padx=(7, 0))

    def populateNeighbourFrame(self, config, ovrNeighbourScore, slocScore, snhbScore):
        Jeff = 0
        C = config
        lblNeighbourOvrV = tk.Label(self.frames[1], text="{}  ".format(ovrNeighbourScore), font=("Arial", 14, "bold"), bg="#e0e0e0")
        lblNeighbour = tk.Label(self.frames[1], text="> Overall Neighbour Sets Score", font=("Arial", 12, "bold", "italic"), bg="#e0e0e0")
        lblNeighbourDes = tk.Label(self.frames[1], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblNeighbourOvrV.config(fg="#2d802f")
            lblNeighbourDes.config(
                text="The Neighbour Sets make for small attack ranges. The Local Scanning and Peer-to-Peer infection methods are capped severly.")
        if 1 <= Jeff < 3:
            lblNeighbourOvrV.config(fg="#e68f39")
            lblNeighbourDes.config(
                text="The Neighbour Sets make for average attack ranges. The Local Scanning and Peer-to-Peer infection have enough of an attack vector to do damage.")
        if Jeff >= 3:
            lblNeighbourOvrV.config(fg="#b81d28")
            lblNeighbourDes.config(
                text="The Neighbour Sets make for large attack ranges. The Local Scanning and Peer-to-Peer infection methods can reach a huge amount of the population.")

        lblExplain = tk.Label(self.frames[1], text="This sections covers the two neighbour sets, the attack ranges for the Local Scanning and Peer-to-Peer infection methods.\n",
                              font=("Arial", 10, "italic"), bg="#e0e0e0")

        lblSLocScoreV = tk.Label(self.frames[1], text="{}  ".format(slocScore), font=("Arial", 12, "bold"), bg="#e0e0e0")
        lblSLocScore = tk.Label(self.frames[1], text="> SLoc Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblSLocDes = tk.Label(self.frames[1], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                text="SLoc is the variable that describes the quantity of locally available nodes in the network, for any Susceptible (S) node.\n\nIn the model, "
                     "this is represented as a fraction of the S population. The fraction of the S population does not change as the simulation progresses but the"
                     " S value does, meaning in the simulation the actual value of SLoc also does.\n\nSLoc is calculated by dividing the entire population (N) across the"
                     "number of Wireless Sensor Networks (WSN), and taking that fraction of N in each WSN from the S population.\n\nThe Local Scanning (IL) infection"
                     "method can only target nodes within the SLoc subset; decided by the infection method only scanning for a nodes' local neighbours.")
        lblSLocScoreDes = tk.Label(self.frames[1], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblSLocScoreV.config(fg="#2d802f")
            lblSLocScoreDes.config(text="In this case, the SLoc fraction was {}. This is decided directly by the WSN count of {}.\n\nIn V-Sim, the maximum number "
                                        "of WSNs is 50 - the lowest is 1 - so the {} WSNs in this simulation was enough to ensure that the number of S nodes reachable by (IL) "
                                        "infection method was limited to only {}%.".format(C.SLocFraction, C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))
        if 1 <= Jeff < 3:
            lblSLocScoreV.config(fg="#e68f39")
            lblSLocScoreDes.config(text="In this case, the SLoc fraction was {}. This is decided directly by the WSN count of {}.\n\nIn V-Sim, the maximum number "
                                        "of WSNs is 50 - the lowest is 1 - so the {} WSNs in this simulation allowed the number of S nodes reachable by IL to be an average / expected "
                                        "amount. The IL bots had access to {}% of the total S population at any given point.".format(C.SLocFraction, C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))
        if Jeff >= 3:
            lblSLocScoreV.config(fg="#b81d28")
            lblSLocScoreDes.config(text="In this case, the SLoc fraction was {}. This is decided directly by the WSN count of {}.\n\nIn V-Sim, the maximum number "
                                        "of WSNs is 50 - the lowest being 1; the {} WSNs in this simulation allowed the IL infection method a much larger than expected attack window "
                                        "and had access to {}% of the entire S population.".format(C.SLocFraction, C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))

        lblSNhbScoreV = tk.Label(self.frames[1], text="{}  ".format(snhbScore), font=("Arial", 12, "bold"), bg="#e0e0e0")
        lblSNhbScore = tk.Label(self.frames[1], text="> SNhb Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblSNhbDes = tk.Label(self.frames[1], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
            text="SNhb is the variable that describes the directly available neighbours, for any Susceptible (S) node - all nodes reachable within the transmission distance;"
                 " also describing the Peer-to-Peer (IP) attack surface as the infection method only propagating payloads through directly connected neighbour."
                 "\n\nSimilarly to SLoc, SNhb is represented as a fraction of the S population, and the actual value changes along with S.\n\nSNhb is calculated by "
                 "calculating the density of nodes in each WSN by dividing the average population of N in each WSN across the deployment area, and then multiplying "
                 " the density by the transmission range to find out how many nodes can be discovered. Finally, this number becomes the fraction of nodes available to reach in each WSN; "
                 "this value is then taken from the S population.\n\nIP has the most limited attack surface, high density and long transmission ranges will increase "
                 "the SNhb attack surface greatly.")
        lblSNhbScoreDes = tk.Label(self.frames[1], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblSNhbScoreV.config(fg="#2d802f")
            lblSNhbScoreDes.config(text="The SNhhb fraction was {}. A smaller than average fraction of S available to IP. This number relies heavily on Density and "
                                        "Transmission Range; this simulations density of {} and transmission range combined to ensure the number of S nodes reachable by (IP) "
                                        "infection method was limited to only {}% of the entire population. The nodes in this deployment were spaced out enough that Peer-to-Peer bots"
                                        "could not propagate effectively.".format(C.SLocFraction, C.density, C.transmissionRange, C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))
        if 1 <= Jeff < 3:
            lblSNhbScoreV.config(fg="#e68f39")
            lblSNhbScoreDes.config(text="The SNhhb fraction was {}. An average fraction of S available to IP. This number relies heavily on Density and "
                      "Transmission Range; this simulations density of {} and transmission range combined to allow the number of S nodes reachable by (IP) "
                      "infection method an expected {}% of the entire population.".format(C.SLocFraction, C.density, C.transmissionRange, C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))
        if Jeff >= 3:
            lblSNhbScoreV.config(fg="#b81d28")
            lblSNhbScoreDes.config(text="The SNhhb fraction was {}. A large fraction of S available to IP. This number relies heavily on Density and "
                                        "Transmission Range; this simulations density of {} and transmission range combined to allow the number of S nodes reachable by (IP) "
                                        "infection method a higher than average {}% of the entire population. The nodes in this deployment were close enough that Peer-to-Peer bots"
                                        "could propagate very effectively.".format(C.SLocFraction, C.density, C.transmissionRange, C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))

        lblNeighbourOvrV.grid(row=1, column=0, sticky="w", padx=(9, 0), pady=7)
        lblNeighbour.grid(row=1, column=2, sticky="w")
        lblNeighbourDes.grid(row=2, column=2, sticky="w", padx=(7, 0))

        lblExplain.grid(row=3, column=2, sticky="w", pady=(10, 0), padx=(7, 0))

        lblSLocScoreV.grid(row=5, column=0, sticky="w", padx=(9, 0))
        lblSLocScore.grid(row=5, column=2, sticky="w")
        lblSLocDes.grid(row=6, column=2, sticky="w", padx=(7, 0))
        lblSLocScoreDes.grid(row=7, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblSNhbScoreV.grid(row=8, column=0, sticky="w", padx=(9, 0))
        lblSNhbScore.grid(row=8, column=2, sticky="w")
        lblSNhbDes.grid(row=9, column=2, sticky="w", padx=(7, 0))
        lblSNhbScoreDes.grid(row=10, column=2, sticky="w", padx=(7, 0), pady=(0, 10))


    def populateInfectionFrame(self, config, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore):
        Jeff = 0
        C = config
        lblinfOvrV = tk.Label(self.frames[2], text="{}  ".format(ovrInfectionScore), font=("Arial", 14, "bold"), bg="#e0e0e0")
        lblinfOvr = tk.Label(self.frames[2], text="> Overall Infection Rates Score", font=("Arial", 12, "bold", "italic"),
                                bg="#e0e0e0")
        lblinfOvrDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblinfOvrV.config(fg="#2d802f")
            lblinfOvrDes.config(
                text="The Infection Rates are low, a minimal propagation of the botnet has been achieved.")
        if 1 <= Jeff < 3:
            lblinfOvrV.config(fg="#e68f39")
            lblinfOvrDes.config(
                text="The Infection Rates are average, an expected propagation of the botnet has occured.")
        if Jeff >= 3:
            lblinfOvrV.config(fg="#b81d28")
            lblinfOvrDes.config(text="The Infection Rates are high, a maxiaml propagation of the botnet has occured.")

        lblExplain = tk.Label(self.frames[2],
                              text="This sections covers the Infection Rates, and how they have been achieved.\n",
                              font=("Arial", 10, "italic"), bg="#e0e0e0")

        lblScanScoreV = tk.Label(self.frames[2], text="{}  ".format(scanningScore), font=("Arial", 12, "bold"),bg="#e0e0e0")
        lblScanScore = tk.Label(self.frames[2], text="> Scanning Rate Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblScanDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                              text="The Scanning Rate variable is simple the rate at which Infected (I) Nodes scan to make contact with S nodes. The default and reccomended value "
                                   "for this is 27 scans per second. This figure is based off of other IoT-based botnets such as the Mirai botnet, but can theoretically reach lower or"
                                   "much higher values.")
        lblScanScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblScanScoreV.config(fg="#2d802f")
            lblScanScoreDes.config(
                text="In this simulation, the Scanning Rate was below average at {} scans per second.".format(C.botScanningRate))
        if 1 <= Jeff < 3:
            lblScanScoreV.config(fg="#e68f39")
            lblScanScoreDes.config(
                text="In this simulation, the Scanning Rate was an average {} scans per second.".format(C.botScanningRate))
        if Jeff >= 3:
            lblScanScoreV.config(fg="#b81d28")
            lblScanScoreDes.config(
                text="In this simulation, the Scanning Rate was higher than average at {} scans per second.".format(C.botScanningRate))

        lblPSuccess = tk.Label(self.frames[2], font=("Arial", 10, "bold"), bg="#e0e0e0", wraplength=1050, justify="left", text="PSuccess")

        lblPSuccessDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                  text="The next three scores are for the PSuccess values for all infection types - IR, IL, and IP.\n\nThe PSuccess value "
                                       "describes the rate of a successful rate of connection, per scan, per second (the Scanning Rate). Multiplying PSuccess by the "
                                       "Scanning Rate forms the Contact Rate for each infection method.\n\nThese values "
                                       "are theoretical, estimated based off of how successful a connection should be; this is reflected in the definitions of the rates. "
                                       "It is noted that changing these values comes at estimates of how successful or not a connection should be; lacking real world data "
                                       "on the subject - informed guesses will decide these rates when deciding them."
                                       "\n\nIR scans the entire S population, which will result in an abundance of connection failures despite having the largest attack "
                                       "surface by far. IL scans the local group, which will result in less but still many failed connections. IP forwards traffic to "
                                       "direct neighbours, resulting in a very high connection chance.\n")

        lblIrPSucScoreV = tk.Label(self.frames[2], text="{}  ".format(irPScore), font=("Arial", 12, "bold"),
                                 bg="#e0e0e0")
        lblIrPSucScore = tk.Label(self.frames[2], text="> IR PSuccess Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblIrPSucScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblIrPSucScoreV.config(fg="#2d802f")
            lblIrPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a lower than expected value - minimising chances of successful connections for IR.".format(C.IrPsuccess))
        if 1 <= Jeff < 3:
            lblIrPSucScoreV.config(fg="#e68f39")
            lblIrPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, ensuring the expected chance of successful connections for IR.".format(C.IrPsuccess))
        if Jeff >= 3:
            lblIrPSucScoreV.config(fg="#b81d28")
            lblIrPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a higher than expected value - maximising chances of successful connections for IR.".format(C.IrPsuccess))

        lblIlPSucScoreV = tk.Label(self.frames[2], text="{}  ".format(ilPScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblIlPSucScore = tk.Label(self.frames[2], text="> IL PSuccess Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblIlPSucScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblIlPSucScoreV.config(fg="#2d802f")
            lblIlPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a lower than expected value - minimising chances of successful connections for IL.".format(C.IlPsuccess))
        if 1 <= Jeff < 3:
            lblIlPSucScoreV.config(fg="#e68f39")
            lblIlPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, ensuring the expected chance of successful connections for IL.".format(C.IlPsuccess))
        if Jeff >= 3:
            lblIlPSucScoreV.config(fg="#b81d28")
            lblIlPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a higher than expected value - maximising chances of successful connections for IL.".format(C.IlPsuccess))

        lblIpPSucScoreV = tk.Label(self.frames[2], text="{}  ".format(ipPScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblIpPSucScore = tk.Label(self.frames[2], text="> IP PSuccess Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblIpPSucScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblIpPSucScoreV.config(fg="#2d802f")
            lblIpPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a lower than expected value - minimising chances of successful connections for IP.\n".format(
                    C.IpPsuccess))
        if 1 <= Jeff < 3:
            lblIpPSucScoreV.config(fg="#e68f39")
            lblIpPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, ensuring the expected chance of successful connections for IP.\n".format(
                    C.IpPsuccess))
        if Jeff >= 3:
            lblIpPSucScoreV.config(fg="#b81d28")
            lblIpPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a higher than expected value - maximising chances of successful connections for IP.\n".format(
                    C.IpPsuccess))

        lblPTrScoreV = tk.Label(self.frames[2], text="{}  ".format(ipPScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblPTrScore = tk.Label(self.frames[2], text="> PTransmission Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblPTrDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                  text="PTransmission is a variable that describes the rate of a successful transmission of a virus payload from any I node to an S node, "
                                       "per successful contact, per second; The Contact Rate multiplied by the PTransmission value equals the infection rate."
                                       "\n\nSimilar to PSuccess, this value is estimated based off of how expected a successful transmission should be; this figure"
                                       "greatly impacts the propagation. The default and reccomended figure is defined based off of other viruses, and should be"
                                       "a realtively small number when factoring in the chances of a successful connection, and other factors such as security.")

        lblPTrScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblPTrScoreV.config(fg="#2d802f")
            lblPTrScoreDes.config(
                text="The PTransmission value for this simulation was {}, a lower than expected value - minimising chances of successful payload deliverance for I nodes."
                     "\nInfection Rate for IR: {}. Infection Rate for IL: {}. Infection Rate for IP: {}.".format(
                     C.Ptransmission, C.bR, C.bL, C.bP))
        if 1 <= Jeff < 3:
            lblPTrScoreV.config(fg="#e68f39")
            lblPTrScoreDes.config(
                text="The PTransmission value for this simulation was {}, a lower than expected value - minimising chances of successful payload deliverance for I nodes."
                     "\nInfection Rate for IR: {}. Infection Rate for IL: {}. Infection Rate for IP: {}.".format(
                     C.Ptransmission, C.bR, C.bL, C.bP))
        if Jeff >= 3:
            lblPTrScoreV.config(fg="#b81d28")
            lblPTrScoreDes.config(
                text="The PTransmission value for this simulation was {}, a lower than expected value - minimising chances of successful payload deliverance for I nodes."
                     "\nInfection Rate for IR: {}. Infection Rate for IL: {}. Infection Rate for IP: {}.".format(
                     C.Ptransmission, C.bR, C.bL, C.bP))

        lblinfOvrV.grid(row=1, column=0, sticky="w", padx=(9, 0), pady=7)
        lblinfOvr.grid(row=1, column=2, sticky="w")
        lblinfOvrDes.grid(row=2, column=2, sticky="w", padx=(7, 0))

        lblExplain.grid(row=3, column=2, sticky="w", pady=(10, 0), padx=(7, 0))

        lblScanScoreV.grid(row=5, column=0, sticky="w", padx=(9, 0))
        lblScanScore.grid(row=5, column=2, sticky="w")
        lblScanDes.grid(row=6, column=2, sticky="w", padx=(7, 0))
        lblScanScoreDes.grid(row=7, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblPSuccess.grid(row=8, column=2, sticky="w", padx=(9, 0))

        lblPSuccessDes.grid(row=9, column=2, sticky="w", padx=(9, 0))

        lblIrPSucScoreV.grid(row=10, column=0, sticky="w", padx=(7, 0))
        lblIrPSucScore.grid(row=10, column=2, sticky="w")
        lblIrPSucScoreDes.grid(row=11, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblIlPSucScoreV.grid(row=12, column=0, sticky="w", padx=(9, 0))
        lblIlPSucScore.grid(row=12, column=2, sticky="w")
        lblIlPSucScoreDes.grid(row=13, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblIpPSucScoreV.grid(row=14, column=0, sticky="w", padx=(9, 0))
        lblIpPSucScore.grid(row=14, column=2, sticky="w")
        lblIpPSucScoreDes.grid(row=15, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblPTrScoreV.grid(row=16, column=0, sticky="w", padx=(9, 0))
        lblPTrScore.grid(row=16, column=2, sticky="w")
        lblPTrDes.grid(row=17, column=2, sticky="w", padx=(7, 0))
        lblPTrScoreDes.grid(row=18, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

    def populateEffortFrame(self, config, ovrEffortScore, tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, depAreaScore):
        pass

    def populateDeathFrame(self, config, ovrDeathRateScore, benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore):
        pass

    def populateSingleFactorFrame(self, config, ovrUncategorisedScore, startingPopScore, rrScore, idsScore):
        pass
