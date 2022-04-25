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
        btnReturn = tk.Button(controlBar, wraplength=41, width=7, text="Return Home", font=("Arial", 7), relief="ridge",
                              fg="white", bg="#6e6e6e",
                              command=lambda: controller.display("SISInspectInterface", "HomeInterface"))
        self.lblControl = tk.Label(controlBar, bg="#453354", text="", font=("Arial", 14, "italic"), fg="white")
        btnOverview = tk.Button(mainFrame, text="Overview", font=("Arial", 9), width=21,
                                command=lambda: self.switchInfoFrame(0, 1))
        btnNeighbourSet = tk.Button(mainFrame, text="Neighbour Sets", font=("Arial", 9), width=21,
                                    command=lambda: self.switchInfoFrame(1, 1))
        btnInfectionRate = tk.Button(mainFrame, text="Infection Rates", font=("Arial", 9), width=21,
                                     command=lambda: self.switchInfoFrame(2, 1))
        btnEffort = tk.Button(mainFrame, text="Payload Effort", font=("Arial", 9), width=21,
                              command=lambda: self.switchInfoFrame(3, 1))
        btnDeath = tk.Button(mainFrame, text="Death Rates", font=("Arial", 9), width=21,
                             command=lambda: self.switchInfoFrame(4, 1))
        btnSingleFactors = tk.Button(mainFrame, text="Single Factors", font=("Arial", 9), width=21,
                                     command=lambda: self.switchInfoFrame(5, 1))

        # This area will contain the assessment and a starter list is created
        self.informationFrame = tk.Frame(mainFrame, bg="#e0e0e0")
        self.frames = [tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                       tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0"),
                       tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="#e0e0e0")]

        # This is the legend footer of the page
        lblLegend1 = tk.Label(mainFrame, bg="#2ca02c", width=32, pady=4, text="(S) Susceptible", font=("Arial", 9),
                              fg="white")
        lblLegend2 = tk.Label(mainFrame, bg="#9467bd", width=32, pady=4, text="(IR) Random-Scanning", font=("Arial", 9),
                              fg="white")
        lblLegend3 = tk.Label(mainFrame, bg="#1f77b4", width=32, pady=4, text="(IL) Local-Scanning", font=("Arial", 9),
                              fg="white")
        lblLegend4 = tk.Label(mainFrame, bg="#17becf", width=32, pady=4, text="(IP) Peer-to-Peer", font=("Arial", 9),
                              fg="white")
        lblLegend5 = tk.Label(mainFrame, bg="#d62728", width=33, pady=4, text="(I) Infection Types Grouped",
                              font=("Arial", 9), fg="white")

        # This contains all graph-side widgets
        graphFrame = tk.Frame(self, bg="#453354")
        self.lblGraphTitle = tk.Label(graphFrame, bg="#453354", text="Assessment Overview",
                                      font=("Arial", 14, "italic"), fg="white")
        btnConfigure = tk.Button(graphFrame, wraplength=60, width=10, text="Control Configuration", font=("Arial", 7),
                                 relief="ridge", fg="white", bg="#6e6e6e",
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
        btnDeath.place(x=778, y=87)
        btnSingleFactors.place(x=975, y=87)
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
        self.ax[0].axvline(linewidth=0.5, color="#a8a8a8", x=self.controller.activeConfiguration.Timesteps / 2,
                           linestyle="--")
        # Plotting the second graph
        self.ax[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.ax[1].plot(T1, I1, '#d62728', label="All Infected")
        self.ax[1].set_xlabel("Timesteps (Hours)")
        self.ax[1].set_ylabel("Node Count")
        self.ax[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        self.ax[1].axvline(linewidth=0.5, color="#a8a8a8", x=self.controller.activeConfiguration.Timesteps / 2,
                           linestyle="--")
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
            self.ax[2].set_title(
                "Population Sizes on Final Recorded Hour #{}".format(self.controller.activeConfiguration.Timesteps))
        else:
            explode = (0.1, 0, 0, 0)
            labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning Infected: {:.0f}".format(pop[1]),
                      "Local Scanning Infected: {:.0f}".format(pop[2]), "Peer-to-Peer Infected: {:.0f}".format(pop[3])]
            colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
            self.ax[2].pie(pop, explode=explode, labels=labels, colors=colours, shadow=True)
            self.ax[2].set_title(
                "Population Sizes on Final Recorded Hour ({})".format(self.controller.activeConfiguration.Timesteps))

        self.lblFinalN.config(text="Population Sizes Totalled (Final N Value): {:.0f}".format(S1[-1] + I1[-1],
                                                                                              self.controller.activeConfiguration.N))

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
        tranRangeScore, msgSizeScore, msgPowerScore, bttryScore, distanceScore, ovrDeathRateScore, \
        benignLifespanScore, IrLifespanScore, IlLifespanScore, IpLifespanScore = config.calculateScores()

        # This section populates each of the frames with updated information conforming to the active models simulation
        # by calling the methods that add the page widgets
        # There are many if statements indicating thresholds that change the displayed information
        self.populateOverview(config, ovrSingleFactorScore, ovrNeighbourScore, ovrInfectionScore, ovrEffortScore,
                              ovrDeathRateScore)
        self.populateNeighbourFrame(config, ovrNeighbourScore, slocScore, snhbScore)
        self.populateInfectionFrame(config, ovrInfectionScore, scanningScore, irPScore, ilPScore, ipPScore, PTrScore)
        self.populateEffortFrame(config, ovrEffortScore, tranRangeScore, msgSizeScore, msgPowerScore, distanceScore)
        self.populateDeathFrame(config, ovrDeathRateScore, bttryScore, benignLifespanScore, IrLifespanScore,
                                IlLifespanScore, IpLifespanScore)
        self.populateSingleFactorFrame(config, ovrSingleFactorScore, startingPopScore, rrScore, idsScore)

    # The following 8 methods are the assessment frame contents
    def populateOverview(self, C, ovrSingleFactorScore, ovrNeighbourScore, ovrInfectionScore, ovrEffortScore,
                         ovrDeathRateScore):
        Jeff = 0

        lbl1 = tk.Label(self.frames[0], text="{} - Assessment Overview and Simulation Scores".format(C.Name),
                        font=("Arial", 12), bg="#e0e0e0")

        lblScoreAc = tk.Label(self.frames[0], text="{}  ".format(
            ovrSingleFactorScore + ovrNeighbourScore + ovrInfectionScore + ovrEffortScore + ovrDeathRateScore),
                              font=("Arial", 14, "bold"), bg="#e0e0e0")
        lblScore = tk.Label(self.frames[0], text="> Overall Simulation Score", font=("Arial", 12, "bold", "italic"),
                            bg="#e0e0e0")
        lblScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblScoreAc.config(fg="#2d802f")
            lblScoreDes.config(
                text="This model has a configuration that results in a generally slower and less potent propagation.")
        if 1 <= Jeff < 3:
            lblScoreAc.config(fg="#b35827")
            lblScoreDes.config(
                text="This model has a configuration that results in an expected / average propagation of a virus.")
        if Jeff >= 3:
            lblScoreAc.config(fg="#b81d28")
            lblScoreDes.config(text="This configuration results in a fast and potent virus propagation.")

        lblExplain = tk.Label(self.frames[0],
                              text="The assessment is broken down into different categories and combine to produce an overall score and explanatory breakdown\n",
                              font=("Arial", 10, "italic"), bg="#e0e0e0")

        lblNeighbourScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrNeighbourScore), font=("Arial", 12, "bold"),
                                      bg="#e0e0e0")
        lblNeighbourScore = tk.Label(self.frames[0], text="> Neighbour Sets Score", font=("Arial", 10, "bold"),
                                     bg="#e0e0e0")
        lblNeighbourScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050,
                                        justify="left")
        if Jeff < 1:
            lblNeighbourScoreV.config(fg="#2d802f")
            lblNeighbourScoreDes.config(
                text="This section looks into the attack surface of Local Scanning (IL) and Peer-to-Peer (IP) infection methods as the proportion "
                     "of the Susceptible (S) population they can target is limited, unlike Random Scanning (IR). \n\n"
                     "In this simulation, the Neighbour Sets make for small attack ranges. The Local Scanning and Peer-to-Peer infection methods are capped severly.")
        if 1 <= Jeff < 3:
            lblNeighbourScoreV.config(fg="#e68f39")
            lblNeighbourScoreDes.config(
                text="This section looks into the attack surface of Local Scanning (IL) and Peer-to-Peer (IP) infection methods as the proportion "
                     "of the Susceptible (S) population they can target is limited, unlike Random Scanning (IR). \n\n"
                     "In this simulation, the Neighbour Sets make for average attack ranges. The Local Scanning and Peer-to-Peer infection have enough of an attack vector to do damage.")
        if Jeff >= 3:
            lblNeighbourScoreV.config(fg="#b81d28")
            lblNeighbourScoreDes.config(
                text="This section looks into the attack surface of Local Scanning (IL) and Peer-to-Peer (IP) infection methods as the proportion "
                     "of the Susceptible (S) population they can target is limited, unlike Random Scanning (IR). \n\n"
                     "In this simulation, the Neighbour Sets make for large attack ranges. The Local Scanning and Peer-to-Peer infection methods can reach a huge amount of the population.")

        lblInfScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrInfectionScore), font=("Arial", 12, "bold"),
                                bg="#e0e0e0")
        lblInfScore = tk.Label(self.frames[0], text="> Infection Rates Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblInfScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblInfScoreV.config(fg="#2d802f")
            lblInfScoreDes.config(
                text="The Infection Rates section explores the calculated rates that describe how well an Infected (I) Node propagates the infection. \n\n"
                     "The calculated Infection Rates are low, a minimal propagation of the botnet has been achieved.")
        if 1 <= Jeff < 3:
            lblInfScoreV.config(fg="#e68f39")
            lblInfScoreDes.config(
                text="The Infection Rates section explores the calculated rates that describe how well an Infected (I) Node propagates the infection. \n\n"
                     "The calculated Infection Rates are average, an expected propagation of the botnet has occured.")
        if Jeff >= 3:
            lblInfScoreV.config(fg="#b81d28")
            lblInfScoreDes.config(
                text="The Infection Rates section explores the calculated rates that describe how well an Infected (I) Node propagates the infection. \n\n"
                     "The calculated Infection Rates are high, a maxiaml propagation of the botnet has occured.")

        lblEffortScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrEffortScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblEffortScore = tk.Label(self.frames[0], text="> Payload Effort Score", font=("Arial", 10, "bold"),
                                  bg="#e0e0e0")
        lblEffortScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblEffortScoreV.config(fg="#2d802f")
            lblEffortScoreDes.config(
                text="The Payload Effort section analyses the factors contributing to the amount of 'Effort' both Susceptible (S) and Infected (I) Nodes "
                     "exert when sending data across the network to other Nodes. \n\n"
                     "Here, the Effort required to send payloads of information across the network to other nodes is minimal, better than average.")
        if 1 <= Jeff < 3:
            lblEffortScoreV.config(fg="#e68f39")
            lblEffortScoreDes.config(
                text="The Payload Effort section analyses the factors contributing to the amount of 'Effort' both Susceptible (S) and Infected (I) Nodes "
                     "exert when sending data across the network to other Nodes. \n\n"
                     "Here, the Effort required to send payloads of information across the network to other nodes is average, the expected effort.")
        if Jeff >= 3:
            lblEffortScoreV.config(fg="#b81d28")
            lblEffortScoreDes.config(
                text="The Payload Effort section analyses the factors contributing to the amount of 'Effort' both Susceptible (S) and Infected (I) Nodes "
                     "exert when sending data across the network to other Nodes. \n\n"
                     "Here, the Effort required to send payloads of information across the network to other nodes is large, making life difficult for Nodes.")

        lblDthScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrDeathRateScore), font=("Arial", 12, "bold"),
                                bg="#e0e0e0")
        lblDthScore = tk.Label(self.frames[0], text="> Lifespan and Death Rates Score", font=("Arial", 10, "bold"),
                               bg="#e0e0e0")
        lblDthScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblDthScoreV.config(fg="#2d802f")
            lblDthScoreDes.config(
                text="This section examines the factors contributing to both Susceptible (S) and Infected (I) Nodes' Lifespans, and the corresponding Death Rates. \n\n"
                     "This configuration results in high Lifespans and low Death Rates. Nodes live extended durations and malicious activity is minimal.")
        if 1 <= Jeff < 3:
            lblDthScoreV.config(fg="#e68f39")
            lblDthScoreDes.config(
                text="This section examines the factors contributing to both Susceptible (S) and Infected (I) Nodes' Lifespans, and the corresponding Death Rates. \n\n"
                     "The node Lifespans are average, as well as the Death Rates. Nodes live the expected durations and malicious activity is present.")
        if Jeff >= 3:
            lblDthScoreV.config(fg="#b81d28")
            lblDthScoreDes.config(
                text="This section examines the factors contributing to both Susceptible (S) and Infected (I) Nodes' Lifespans, and the corresponding Death Rates. \n\n"
                     "This configuration results in low Lifespans and high Death Rates. Nodes live reduced durations and malicious activity is substantial.")

        lblSFScoreV = tk.Label(self.frames[0], text="{}  ".format(ovrSingleFactorScore), font=("Arial", 12, "bold"),
                               bg="#e0e0e0")
        lblSFScore = tk.Label(self.frames[0], text="> Single Factor Scores", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblSFScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblSFScoreV.config(fg="#2d802f")
            lblSFScoreDes.config(
                text="This section looks at three particular starting conditions: Starting Population Sizes, Admin Engagement, and Intrusion Detection System"
                     " (IDS) usage. \n\n"
                     "In this simulation, these Single Factors have helped achieve a minimal virus propagation.\n\n\n")
        if 1 <= Jeff < 3:
            lblSFScoreV.config(fg="#e68f39")
            lblSFScoreDes.config(
                text="This section looks at three particular starting conditions: Starting Population Sizes, Admin Engagement, and Intrusion Detection System"
                     " (IDS) usage. \n\n"
                     "In this simulation, these Single Factors are at the expected thresholds and result in the expected botnet presence.\n\n\n")
        if Jeff >= 3:
            lblSFScoreV.config(fg="#b81d28")
            lblSFScoreDes.config(
                text="This section looks at three particular starting conditions: Starting Population Sizes, Admin Engagement, and Intrusion Detection System"
                     " (IDS) usage. \n\n"
                     "In this simulation, these Single Factors have contributed to a higher virus propagation.\n\n\n")

        lblExplain3 = tk.Label(self.frames[0],
                               text="The overall score ranges from a minimum of ___ to ___ and to a maximum of ___",
                               font=("Arial", 10, "italic"), bg="#e0e0e0")
        lblExplain4 = tk.Label(self.frames[0],
                               text="Below ___ is a High Score - an Ideal Model Score for Minimal Virus Propagation, ",
                               font=("Arial", 10, "italic"), bg="#e0e0e0", fg="#2d802f")
        lblExplain5 = tk.Label(self.frames[0],
                               text="Between ___ and ___ is Medium Score - a Sub-Optimal Score but Relatively Safe,",
                               font=("Arial", 10, "italic"), bg="#e0e0e0", fg="#e68f39")
        lblExplain6 = tk.Label(self.frames[0],
                               text="Above ___ is Lower Score - a Dangerous Score Indicating Optimal Conditions for Virus Propagation",
                               font=("Arial", 10, "italic"), bg="#e0e0e0", fg="#b81d28")
        lblExplain7 = tk.Label(self.frames[0],
                               text="Press the labelled buttons above to inspect the correspoinding categories' score breakdown.",
                               font=("Arial", 10, "italic"), bg="#e0e0e0")

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
        lblNeighbourOvrV = tk.Label(self.frames[1], text="{}  ".format(ovrNeighbourScore), font=("Arial", 14, "bold"),
                                    bg="#e0e0e0")
        lblNeighbour = tk.Label(self.frames[1], text="> Overall Neighbour Sets Score",
                                font=("Arial", 12, "bold", "italic"), bg="#e0e0e0")
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

        lblExplain = tk.Label(self.frames[1],
                              text="This sections covers the two neighbour sets, the attack ranges for the Local Scanning and Peer-to-Peer infection methods.\n",
                              font=("Arial", 10, "italic"), bg="#e0e0e0")

        lblSLocScoreV = tk.Label(self.frames[1], text="{}  ".format(slocScore), font=("Arial", 12, "bold"),
                                 bg="#e0e0e0")
        lblSLocScore = tk.Label(self.frames[1], text="> SLoc Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblSLocDes = tk.Label(self.frames[1], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                              text="SLoc is the variable that describes the quantity of locally available nodes in the network, for any Susceptible (S) node.\n\nIn the model, "
                                   "this is represented as a fraction of the S population. The fraction of the S population does not change as the simulation progresses but the"
                                   " S value does, meaning in the simulation the actual value of SLoc also does.\n\nSLoc is calculated by dividing the entire population (N) across the"
                                   "number of Wireless Sensor Networks (WSN), and taking that fraction of N in each WSN from the S population.\n\nThe Local Scanning (IL) infection"
                                   "method can only target nodes within the SLoc subset; decided by the infection method only scanning for a nodes' local neighbours.")
        lblSLocScoreDes = tk.Label(self.frames[1], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if 4 <= slocScore <= 5:
            lblSLocScoreV.config(fg="#2d802f")
            lblSLocScoreDes.config(
                text="In this case, the SLoc fraction was {}. This is decided directly by the WSN count of {}.\n\nIn V-Sim, the maximum number "
                     "of WSNs is 50 - the lowest is 1 - so the {} WSNs in this simulation was enough to ensure that the number of S nodes reachable by (IL) "
                     "infection method was limited to only {}%.\n".format(C.SLocFraction, C.WSNnumber, C.WSNnumber,
                                                                          C.SLocFraction * 100))
        if slocScore == 3:
            lblSLocScoreV.config(fg="#e68f39")
            lblSLocScoreDes.config(
                text="In this case, the SLoc fraction was {}. This is decided directly by the WSN count of {}.\n\nIn V-Sim, the maximum number "
                     "of WSNs is 50 - the lowest is 1 - so the {} WSNs in this simulation allowed the number of S nodes reachable by IL to be an average / expected "
                     "amount. The IL bots had access to {}% of the total S population at any given point.\n".format(
                    C.SLocFraction, C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))
        if 1 <= slocScore <= 2:
            lblSLocScoreV.config(fg="#b81d28")
            lblSLocScoreDes.config(
                text="In this case, the SLoc fraction was {}. This is decided directly by the WSN count of {}.\n\nIn V-Sim, the maximum number "
                     "of WSNs is 50 - the lowest being 1; the {} WSNs in this simulation allowed the IL infection method a much larger than expected attack window "
                     "and had access to {}% of the entire S population.\n".format(C.SLocFraction, C.WSNnumber,
                                                                                  C.WSNnumber, C.SLocFraction * 100))

        lblSNhbScoreV = tk.Label(self.frames[1], text="{}  ".format(snhbScore), font=("Arial", 12, "bold"),
                                 bg="#e0e0e0")
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
        if snhbScore == 4:
            lblSNhbScoreV.config(fg="#2d802f")
            lblSNhbScoreDes.config(
                text="The SNhhb fraction was {}. A smaller than average fraction of S available to IP. This number relies heavily on Density and "
                     "Transmission Range; this simulations density of {} and transmission range combined to ensure the number of S nodes reachable by (IP) "
                     "infection method was limited to only {}% of the entire population. The nodes in this deployment were spaced out enough that Peer-to-Peer bots"
                     "could not propagate effectively.".format(C.SLocFraction, C.density, C.transmissionRange,
                                                               C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))
        if 2 <= snhbScore == 3:
            lblSNhbScoreV.config(fg="#e68f39")
            lblSNhbScoreDes.config(
                text="The SNhhb fraction was {}. An average fraction of S available to IP. This number relies heavily on Density and "
                     "Transmission Range; this simulations density of {} and transmission range combined to allow the number of S nodes reachable by (IP) "
                     "infection method an expected {}% of the entire population.".format(C.SLocFraction, C.density,
                                                                                         C.transmissionRange,
                                                                                         C.WSNnumber, C.WSNnumber,
                                                                                         C.SLocFraction * 100))
        if snhbScore == 1:
            lblSNhbScoreV.config(fg="#b81d28")
            lblSNhbScoreDes.config(
                text="The SNhhb fraction was {}. A large fraction of S available to IP. This number relies heavily on Density and "
                     "Transmission Range; this simulations density of {} and transmission range combined to allow the number of S nodes reachable by (IP) "
                     "infection method a higher than average {}% of the entire population. The nodes in this deployment were close enough that Peer-to-Peer bots"
                     "could propagate very effectively.".format(C.SLocFraction, C.density, C.transmissionRange,
                                                                C.WSNnumber, C.WSNnumber, C.SLocFraction * 100))

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
        lblinfOvrV = tk.Label(self.frames[2], text="{}  ".format(ovrInfectionScore), font=("Arial", 14, "bold"),
                              bg="#e0e0e0")
        lblinfOvr = tk.Label(self.frames[2], text="> Overall Infection Rates Score",
                             font=("Arial", 12, "bold", "italic"),
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

        lblScanScoreV = tk.Label(self.frames[2], text="{}  ".format(scanningScore), font=("Arial", 12, "bold"),
                                 bg="#e0e0e0")
        lblScanScore = tk.Label(self.frames[2], text="> Scanning Rate Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblScanDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                              text="The Scanning Rate variable is simple the rate at which Infected (I) Nodes scan to make contact with S nodes. The default and reccomended value "
                                   "for this is 27 scans per second. This figure is based off of other IoT-based botnets such as the Mirai botnet, but can theoretically reach lower or"
                                   "much higher values.")
        lblScanScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if 4 <= scanningScore <= 5:
            lblScanScoreV.config(fg="#2d802f")
            lblScanScoreDes.config(
                text="In this simulation, the Scanning Rate was below average at {} scans per second.".format(
                    C.botScanningRate))
        if scanningScore == 3:
            lblScanScoreV.config(fg="#e68f39")
            lblScanScoreDes.config(
                text="In this simulation, the Scanning Rate was an average {} scans per second.".format(
                    C.botScanningRate))
        if 1 <= scanningScore <= 2:
            lblScanScoreV.config(fg="#b81d28")
            lblScanScoreDes.config(
                text="In this simulation, the Scanning Rate was higher than average at {} scans per second.".format(
                    C.botScanningRate))

        lblPSuccess = tk.Label(self.frames[2], font=("Arial", 10, "bold"), bg="#e0e0e0", wraplength=1050,
                               justify="left", text="PSuccess")

        lblPSuccessDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                  text="The next three scores are for the PSuccess values for all infection types - IR, IL, and IP.\n\nThe PSuccess value "
                                       "describes the rate of a successful rate of connection, per scan, per second (the Scanning Rate). Multiplying PSuccess by the "
                                       "Scanning Rate forms the Contact Rate for each infection method.\n\nThese values "
                                       "are theoretical, estimated based off of how successful a connection should be; this is reflected in the definitions of the rates. "
                                       "It is noted that changing these values comes at estimates of how successful or not a connection should be; lacking real world data "
                                       "on the subject - informed guesses will decide these rates when deciding them."
                                       "\n\nIR scans the entire S population, which will result in an abundance of connection failures despite having the largest attack "
                                       "surface. \nIL scans the local group, which will result in less but still many failed connections. \nIP forwards traffic to "
                                       "direct neighbours, resulting in a very high connection chance.\n")

        lblIrPSucScoreV = tk.Label(self.frames[2], text="{}  ".format(irPScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblIrPSucScore = tk.Label(self.frames[2], text="> IR PSuccess Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblIrPSucScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if 4 <= irPScore <= 5:
            lblIrPSucScoreV.config(fg="#2d802f")
            lblIrPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a lower than expected value - minimising chances of successful connections for IR.".format(
                    C.IrPsuccess))
        if irPScore == 3:
            lblIrPSucScoreV.config(fg="#e68f39")
            lblIrPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, ensuring the expected chance of successful connections for IR.".format(
                    C.IrPsuccess))
        if 1 <= irPScore <= 2:
            lblIrPSucScoreV.config(fg="#b81d28")
            lblIrPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a higher than expected value - maximising chances of successful connections for IR.".format(
                    C.IrPsuccess))

        lblIlPSucScoreV = tk.Label(self.frames[2], text="{}  ".format(ilPScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblIlPSucScore = tk.Label(self.frames[2], text="> IL PSuccess Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblIlPSucScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if 4 <= ilPScore <= 5:
            lblIlPSucScoreV.config(fg="#2d802f")
            lblIlPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a lower than expected value - minimising chances of successful connections for IL.".format(
                    C.IlPsuccess))
        if ilPScore == 3:
            lblIlPSucScoreV.config(fg="#e68f39")
            lblIlPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, ensuring the expected chance of successful connections for IL.".format(
                    C.IlPsuccess))
        if 1 <= ilPScore <= 2:
            lblIlPSucScoreV.config(fg="#b81d28")
            lblIlPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a higher than expected value - maximising chances of successful connections for IL.".format(
                    C.IlPsuccess))

        lblIpPSucScoreV = tk.Label(self.frames[2], text="{}  ".format(ipPScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblIpPSucScore = tk.Label(self.frames[2], text="> IP PSuccess Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblIpPSucScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if 4 <= ipPScore <= 5:
            lblIpPSucScoreV.config(fg="#2d802f")
            lblIpPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a lower than expected value - minimising chances of successful connections for IP.\n".format(
                    C.IpPsuccess))
        if ipPScore == 3:
            lblIpPSucScoreV.config(fg="#e68f39")
            lblIpPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, ensuring the expected chance of successful connections for IP.\n".format(
                    C.IpPsuccess))
        if 1 <= ipPScore <= 2:
            lblIpPSucScoreV.config(fg="#b81d28")
            lblIpPSucScoreDes.config(
                text="The PSuccess value for this simulation was {}, a higher than expected value - maximising chances of successful connections for IP.\n".format(
                    C.IpPsuccess))

        lblPTrScoreV = tk.Label(self.frames[2], text="{}  ".format(PTrScore), font=("Arial", 12, "bold"),
                                bg="#e0e0e0")
        lblPTrScore = tk.Label(self.frames[2], text="> PTransmission Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblPTrDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                             text="PTransmission is a variable that describes the rate of a successful transmission of a virus payload from any I node to an S node, "
                                  "per successful contact, per second; The Contact Rate multiplied by the PTransmission value equals the infection rate."
                                  "\n\nSimilar to PSuccess, this value is estimated based off of how expected a successful transmission should be; this figure"
                                  "greatly impacts the propagation. The default and reccomended figure is defined based off of other viruses, and should be"
                                  "a realtively small number when factoring in the chances of a successful connection, and other factors such as security.")

        lblPTrScoreDes = tk.Label(self.frames[2], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if 4 <= PTrScore <= 5:
            lblPTrScoreV.config(fg="#2d802f")
            lblPTrScoreDes.config(
                text="The PTransmission value for this simulation was {}, a lower than expected value - minimising chances of successful payload deliverance for I nodes."
                     "\nInfection Rate for IR: {}. Infection Rate for IL: {}. Infection Rate for IP: {}.".format(
                    C.Ptransmission, C.bR, C.bL, C.bP))
        if PTrScore == 3:
            lblPTrScoreV.config(fg="#e68f39")
            lblPTrScoreDes.config(
                text="The PTransmission value for this simulation was {}, a lower than expected value - minimising chances of successful payload deliverance for I nodes."
                     "\nInfection Rate for IR: {}. Infection Rate for IL: {}. Infection Rate for IP: {}.".format(
                    C.Ptransmission, C.bR, C.bL, C.bP))
        if 1 <= PTrScore <= 2:
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

    def populateEffortFrame(self, config, ovrEffortScore, tranRangeScore, msgSizeScore, msgPowerScore, distanceScore):
        Jeff = 0
        C = config
        lblEffortOvrV = tk.Label(self.frames[3], text="{}  ".format(ovrEffortScore), font=("Arial", 14, "bold"),
                                 bg="#e0e0e0")
        lblEffortOvr = tk.Label(self.frames[3], text="> Overall Effort Score",
                                font=("Arial", 12, "bold", "italic"),
                                bg="#e0e0e0")
        lblEffortOvrDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblEffortOvrV.config(fg="#2d802f")
            lblEffortOvrDes.config(
                text="The Effort required to send payloads of information across the network to other nodes is minimal, better than average.")
        if 1 <= Jeff < 3:
            lblEffortOvrV.config(fg="#e68f39")
            lblEffortOvrDes.config(
                text="The Effort required to send payloads of information across the network to other nodes is average, the expected effort.")
        if Jeff >= 3:
            lblEffortOvrV.config(fg="#b81d28")
            lblEffortOvrDes.config(
                text="The Effort required to send payloads of information across the network to other nodes is large, making life difficult for Nodes.")

        lblExplain = tk.Label(self.frames[3],
                              text="This sections covers the factors contributing towards Payload Effort.",
                              font=("Arial", 10, "italic"), bg="#e0e0e0", wraplength=1050, justify="left")

        lblExplain2 = tk.Label(self.frames[3],
                               text="Each node in the network has a limited battery capacity, the propagation of payloads across the network will drain the battery over time; so the effort to send"
                                    "a message will impact the lifespans of the nodes heavily.\n\n"
                                    "The factors contributing to effort are:\n\n"
                                    "Message Size, the Power Required to Send Data Across the Network, and the Distance Between Nodes\n",
                               font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")

        lblTransmissionScoreV = tk.Label(self.frames[3], text="{}  ".format(tranRangeScore), font=("Arial", 12, "bold"),
                                         bg="#e0e0e0")
        lblTransmissionScore = tk.Label(self.frames[3], text="> Transmission Range Score", font=("Arial", 10, "bold"),
                                        bg="#e0e0e0")
        lblTransmissionDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                      text="The Transmission Range variable is simply the distance in meters that any node is able to send a message (a payload).\n\n"
                                           "The average and expected range is 10m, however this can theoretically be much lower or higher.")
        lblTransmissionScoreDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050,
                                           justify="left")
        if 4 <= tranRangeScore <= 5:
            lblTransmissionScoreV.config(fg="#2d802f")
            lblTransmissionScoreDes.config(
                text="In this simulation, the Transmission Range was lower than average at {}m.\n"
                     "This results in nodes requiring closer placement to one another in order to communicate.".format(
                    C.transmissionRange))
        if tranRangeScore == 3:
            lblTransmissionScoreV.config(fg="#e68f39")
            lblTransmissionScoreDes.config(
                text="In this simulation, the Transmission Range was an expected {}m.\n"
                     "This results in nodes delivering payloads to an expected maximum.".format(C.transmissionRange))
        if 1 <= tranRangeScore <= 2:
            lblTransmissionScoreV.config(fg="#b81d28")
            lblTransmissionScoreDes.config(
                text="In this simulation, the Transmission Range was higher than average at {}m.\n"
                     "This allows any node to have a greatly increased chance of being able to reach another; including I nodes propagating viruses.".format(
                    C.transmissionRange))

        lblMsgSizeScoreV = tk.Label(self.frames[3], text="{}  ".format(msgSizeScore), font=("Arial", 12, "bold"),
                                    bg="#e0e0e0")
        lblMsgSizeScore = tk.Label(self.frames[3], text="> Mean Message Size Score", font=("Arial", 10, "bold"),
                                   bg="#e0e0e0")

        lblMsgSizeDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                 text="This variable describes the mean size of a message sent across the network, from node to node - the typical message size a sensor node sends.\n\n"
                                      "The typical size is 50 Bytes, but this will vary dependent on the type of botnet and the traffic it generates. ")

        lblMsgSizeScoreDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if msgSizeScore == 3:
            lblMsgSizeScoreV.config(fg="#2d802f")
            lblMsgSizeScoreDes.config(
                text="The Mean Message Size in this simulation was a lower than average {} Bytes.".format(
                    C.meanMessageSize))
        if msgSizeScore == 2:
            lblMsgSizeScoreV.config(fg="#e68f39")
            lblMsgSizeScoreDes.config(
                text="The Mean Message Size in this simulation was an expected {} Bytes.".format(C.meanMessageSize))
        if msgSizeScore == 1:
            lblMsgSizeScoreV.config(fg="#b81d28")
            lblMsgSizeScoreDes.config(
                text="The Mean Message Size in this simulation was a higher than average {} Bytes.".format(
                    C.meanMessageSize))

        lblMsgPowerScoreV = tk.Label(self.frames[3], text="{}  ".format(msgPowerScore), font=("Arial", 12, "bold"),
                                     bg="#e0e0e0")
        lblMsgPowerScore = tk.Label(self.frames[3], text="> Mean Message Power Score", font=("Arial", 10, "bold"),
                                    bg="#e0e0e0")

        lblMsgPowerDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                  text="This variable is simply the mean amount of power consumed in order to send 1 Byte of data to another Node.")

        lblMsgPowerScoreDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050,
                                       justify="left")
        if msgPowerScore == 3:
            lblMsgPowerScoreV.config(fg="#2d802f")
            lblMsgPowerScoreDes.config(
                text="The Mean Message Size in this simulation was a lower than average {} Bytes.".format(
                    C.meanPower))
        if msgPowerScore == 2:
            lblMsgPowerScoreV.config(fg="#e68f39")
            lblMsgPowerScoreDes.config(
                text="The Mean Message Size in this simulation was an expected {} Bytes.".format(C.meanPower))
        if msgPowerScore == 1:
            lblMsgPowerScoreV.config(fg="#b81d28")
            lblMsgPowerScoreDes.config(
                text="The Mean Message Size in this simulation was a higher than average {} Bytes.".format(C.meanPower))

        lblDistanceScoreV = tk.Label(self.frames[3], text="{}  ".format(distanceScore), font=("Arial", 12, "bold"),
                                     bg="#e0e0e0")
        lblDistanceScore = tk.Label(self.frames[3], text="> Distance Score", font=("Arial", 10, "bold"), bg="#e0e0e0")

        lblDistanceDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                  text="The Distance variable specifies the average distance (in meters) between any two nodes in a WSN. It is a direct factor inside of"
                                       "calculating Payload Effort.\n\n"
                                       "It is calculated by dividing the average area inside of any WSN by the average proportion of the entire N population"
                                       "in any given WSN; for this particular model, even node distribution and uniformity is assumed")

        lblDistanceScoreDes = tk.Label(self.frames[3], font=("Arial", 10), bg="#e0e0e0", wraplength=1050,
                                       justify="left")
        if Jeff < 1:
            lblDistanceScoreV.config(fg="#2d802f")
            lblDistanceScoreDes.config(
                text="The Distance in this simulation was a lower than average {}m.\n\n"
                     "This means nodes have much less distance to spend effort on sending messages.".format(C.distance))
        if 1 <= Jeff < 3:
            lblDistanceScoreV.config(fg="#e68f39")
            lblDistanceScoreDes.config(
                text="The Distance in this simulation was an average {}m.\n\n"
                     "Nodes spend the expected amount of effort when considering the distance between them.".format(
                    C.distance))
        if Jeff >= 3:
            lblDistanceScoreV.config(fg="#b81d28")
            lblDistanceScoreDes.config(
                text="The Distance in this simulation was a higher than average {}m.\n\n"
                     "This means nodes have much more distance to spend effort on sending messages.".format(C.distance))

        lblEffortOvrV.grid(row=1, column=0, sticky="w", padx=(9, 0), pady=7)
        lblEffortOvr.grid(row=1, column=2, sticky="w")
        lblEffortOvrDes.grid(row=2, column=2, sticky="w", padx=(7, 0))

        lblExplain.grid(row=3, column=2, sticky="w", pady=(10, 0), padx=(7, 0))
        lblExplain2.grid(row=4, column=2, sticky="w", pady=(10, 0), padx=(7, 0))

        lblTransmissionScoreV.grid(row=5, column=0, sticky="w", padx=(9, 0))
        lblTransmissionScore.grid(row=5, column=2, sticky="w")
        lblTransmissionDes.grid(row=6, column=2, sticky="w", padx=(7, 0))
        lblTransmissionScoreDes.grid(row=7, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblMsgSizeScoreV.grid(row=8, column=0, sticky="w", padx=(7, 0))
        lblMsgSizeScore.grid(row=8, column=2, sticky="w")
        lblMsgSizeDes.grid(row=9, column=2, sticky="w", padx=(9, 0))
        lblMsgSizeScoreDes.grid(row=10, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblMsgPowerScoreV.grid(row=11, column=0, sticky="w", padx=(7, 0))
        lblMsgPowerScore.grid(row=11, column=2, sticky="w")
        lblMsgPowerDes.grid(row=12, column=2, sticky="w", padx=(9, 0))
        lblMsgPowerScoreDes.grid(row=13, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblDistanceScoreV.grid(row=16, column=0, sticky="w", padx=(9, 0))
        lblDistanceScore.grid(row=16, column=2, sticky="w")
        lblDistanceDes.grid(row=17, column=2, sticky="w", padx=(7, 0))
        lblDistanceScoreDes.grid(row=18, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

    def populateDeathFrame(self, config, ovrDeathRateScore, bttryScore, benignLifespanScore, IrLifespanScore,
                           IlLifespanScore, IpLifespanScore):
        Jeff = 0
        C = config
        lblDeathOvrV = tk.Label(self.frames[4], text="{}  ".format(ovrDeathRateScore), font=("Arial", 14, "bold"),
                                bg="#e0e0e0")
        lblDeathOvr = tk.Label(self.frames[4], text="> Overall Lifespan and Death Rates Score",
                               font=("Arial", 12, "bold", "italic"),
                               bg="#e0e0e0")
        lblDeathOvrDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblDeathOvrV.config(fg="#2d802f")
            lblDeathOvrDes.config(
                text="This configuration results in high Lifespans and low Death Rates. Nodes live extended durations and malicious activity is minimal.")
        if 1 <= Jeff < 3:
            lblDeathOvrV.config(fg="#e68f39")
            lblDeathOvrDes.config(
                text="The node Lifespans are average, as well as the Death Rates. Nodes live the expected durations and malicious activity is present.")
        if Jeff >= 3:
            lblDeathOvrV.config(fg="#b81d28")
            lblDeathOvrDes.config(
                text="This configuration results in low Lifespans and high Death Rates. Nodes live reduced durations and malicious activity is substantial.")

        lblExplain = tk.Label(self.frames[4],
                              text="This sections covers the factors contributing towards the node Lifespans and the corresponding Death Rates.",
                              font=("Arial", 10, "italic"), bg="#e0e0e0", wraplength=1050, justify="left")

        lblExplain2 = tk.Label(self.frames[4],
                               text="Assessed previously were the Contact Rates and the effort required to deliver a payload to another; these two factors describe the quantity of actions able to be "
                                    "performed before a nodes' finite battery has depleted. Furthermore, the formula 1 / Node Lifespan provides the Death Rate, the number multiplied to each population group describing deaths each timestep. "
                                    "This forms the Final N value - the amount of nodes still surviving; this model assumes there are"
                                    " no 'births' into the system. Finally, given enough time, all nodes will perish - but Death Rates can be immensely high or low, allowing nodes overly extended lifespans"
                                    " or devastatingly short ones, as well as anything in between.\n",
                               font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")

        lblbttryScoreV = tk.Label(self.frames[4], text="{}  ".format(bttryScore), font=("Arial", 12, "bold"),
                                  bg="#e0e0e0")
        lblbttryScore = tk.Label(self.frames[4], text="> Total Node Battery Capacity Score", font=("Arial", 10, "bold"),
                                 bg="#e0e0e0")
        lblbttryDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                               text="This variable is simply the Total Capacity of the Battery each node is equip with. The typical battery size for nodes found "
                                    "in Wireless Sensor Networks is 864000 mAs, but battery size options of "
                                    "one quater the size, as well as four times the size have been provided to show contrast and the impact of this variable.")
        lblbttryScoreDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050,
                                    justify="left")
        if bttryScore == 3:
            lblbttryScoreV.config(fg="#2d802f")
            lblbttryScoreDes.config(
                text="In this simulation, the Total Battery Capacity was higher than average at {} mAs. This results in nodes having much more power to spend on effort communicating, driving the Lifespans up, and the Death Rates down.".format(
                    C.totalBattery))
        if bttryScore == 2:
            lblbttryScoreV.config(fg="#e68f39")
            lblbttryScoreDes.config(
                text="In this simulation, the Total Battery Capacity was average at {} mAs. This results in nodes having the expected amount of power to spend on effort communicating.".format(
                    C.totalBattery))
        if bttryScore == 1:
            lblbttryScoreV.config(fg="#b81d28")
            lblbttryScoreDes.config(
                text="In this simulation, the Total Battery Capacity was lower than average at {} mAs. This results in nodes having much less power to spend on effort communicating, driving the Lifespans down, and the Death Rates up.".format(
                    C.totalBattery))

        lblBenignScoreV = tk.Label(self.frames[4], text="{}  ".format(benignLifespanScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblBenignScore = tk.Label(self.frames[4], text="> Benign Lifespan and Death Rate Score", font=("Arial", 10, "bold"),
                                  bg="#e0e0e0")

        lblBenignDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                text="This variable is the Benign Lifespan and Corresponding Death Rate for all nodes, both S and I. While all nodes will die at this rate due to "
                                     "standard node activity, each infection type has an additional Death Rate of its own"
                                     "definition. This is due to the fact that bot nodes perform additional activity - malicious activity propagating their virus payloads.\n\n"
                                     "In this model, the Contact Rate for S Nodes only impacts the Benign Death Rate; rates between 1-15 Contacts per second are expected, but can"
                                     "theoretically be much higher or lower.")

        lblBenignScoreDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblBenignScoreV.config(fg="#2d802f")
            lblBenignScoreDes.config(
                text="The Benign Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IR was {}.\n\n"
                     "The Lifespan and Death Rate due to standard activities result in nodes living longer and propagating less data overall.".format(
                    C.benignLifespan, C.dthB, C.contactRate))
        if 1 <= Jeff < 3:
            lblBenignScoreV.config(fg="#e68f39")
            lblBenignScoreDes.config(
                text="The Benign Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IR was {}.\n\n"
                     "The Lifespan and Death Rate due to standard activities result in nodes living an average duration and propagating an expected amount of data overall.".format(
                    C.benignLifespan, C.dthB, C.contactRate))
        if Jeff >= 3:
            lblBenignScoreV.config(fg="#b81d28")
            lblBenignScoreDes.config(
                text="The Benign Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IR was {}.\n\n"
                     "The Lifespan and Death Rate due to standard activities result in nodes living a shorter time and propagating more data overall.".format(
                    C.benignLifespan, C.dthB, C.contactRate))

        lblRandomScoreV = tk.Label(self.frames[4], text="{}  ".format(IrLifespanScore), font=("Arial", 12, "bold"),
                                   bg="#e0e0e0")
        lblRandomScore = tk.Label(self.frames[4], text="> Random Scanning Lifespan and Death Rate Score",
                                  font=("Arial", 10, "bold"),
                                  bg="#e0e0e0")

        lblRandomDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                                text="This variable is the Random Scanning Lifespan and Corresponding Death Rate for nodes specifically infected through Random Scanning (IR). "
                                     "This score, along with the following two, is calculated through how much malicious activity this infection method has performed.\n\n"
                                     "While all nodes propagate the same average amount of data, using the same amount of power to transmit it, and over the same average distance,"
                                     "each population group have their respective Contact Rates calculated differently - impacting the lifespans accordingly.")

        lblRandomScoreDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblRandomScoreV.config(fg="#2d802f")
            lblRandomScoreDes.config(
                text="The Random Scanning Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IR was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Random Scanning activity results in the IR population group living longer tha expected and performing much less malicious"
                     " activity.".format(C.randomLifespan, C.dthR, C.IrContactRate))
        if 1 <= Jeff < 3:
            lblRandomScoreV.config(fg="#e68f39")
            lblRandomScoreDes.config(
                text="The Random Scanning Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IR was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Random Scanning activity results in the IR population group living an average duration and performing the "
                     "expected amount of malicious activity.".format(C.randomLifespan, C.dthR, C.IrContactRate))
        if Jeff >= 3:
            lblRandomScoreV.config(fg="#b81d28")
            lblRandomScoreDes.config(
                text="The Random Scanning Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IR was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Random Scanning activity results in the IR population group living much shorter than expected and performing much more malicious"
                     " activity.".format(C.randomLifespan, C.dthR, C.IrContactRate))

        lblLocalScoreV = tk.Label(self.frames[4], text="{}  ".format(IlLifespanScore), font=("Arial", 12, "bold"),
                                  bg="#e0e0e0")
        lblLocalScore = tk.Label(self.frames[4], text="> Local Scanning Lifespan and Death Rate Score",
                                 font=("Arial", 10, "bold"),
                                 bg="#e0e0e0")

        lblLocalDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                               text="This variable is the Local Scanning Lifespan and Corresponding Death Rate for nodes specifically infected through Local Scanning (IL).\n\n"
                                    "Local Scanning, on average, should have a higher Death Rate than Random Scanning. This is due to the better chances of successful connection - and therefore"
                                    " more malicious activity.")

        lblLocalScoreDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblLocalScoreV.config(fg="#2d802f")
            lblLocalScoreDes.config(
                text="The Local Scanning Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IL was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Local Scanning activity results in the IL population group living longer tha expected and performing much less malicious"
                     " activity.".format(C.localLifespan, C.dthL, C.IlContactRate))
        if 1 <= Jeff < 3:
            lblLocalScoreV.config(fg="#e68f39")
            lblLocalScoreDes.config(
                text="The Local Scanning Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IL was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Local Scanning activity results in the IL population group living an average duration and performing the "
                     "expected amount of malicious activity.".format(C.localLifespan, C.dthL, C.IlContactRate))
        if Jeff >= 3:
            lblLocalScoreV.config(fg="#b81d28")
            lblLocalScoreDes.config(
                text="The Local Scanning Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IL was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Local Scanning activity results in the IL population group living much shorter than expected and performing much more malicious"
                     " activity.".format(C.localLifespan, C.dthL, C.IlContactRate))

        lblP2PScoreV = tk.Label(self.frames[4], text="{}  ".format(IpLifespanScore), font=("Arial", 12, "bold"),
                                bg="#e0e0e0")
        lblP2PScore = tk.Label(self.frames[4], text="> Peer-to-Peer Lifespan and Death Rate Score",
                               font=("Arial", 10, "bold"),
                               bg="#e0e0e0")

        lblP2PDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                             text="This variable is the Local Scanning Lifespan and Corresponding Death Rate for nodes specifically infected through Peer-to-Peer forwarding (IP).\n\n"
                                  "Peer-to-Peer, on average, should have a much higher Death Rate than both Random and Local Scanning. This is due to very high chances of successful "
                                  "connection - and therefore more malicious activity.")

        lblP2PScoreDes = tk.Label(self.frames[4], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff < 1:
            lblP2PScoreV.config(fg="#2d802f")
            lblP2PScoreDes.config(
                text="The Peer-to-Peer Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IL was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Local Scanning activity results in the IL population group living longer tha expected and performing much less malicious"
                     " activity.".format(C.peerToPeerLifespan, C.dthP, C.IpContactRate))
        if 1 <= Jeff < 3:
            lblP2PScoreV.config(fg="#e68f39")
            lblP2PScoreDes.config(
                text="The Peer-to-Peer Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IL was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Local Scanning activity results in the IL population group living an average duration and performing the "
                     "expected amount of malicious activity.".format(C.peerToPeerLifespan, C.dthP, C.IpContactRate))
        if Jeff >= 3:
            lblP2PScoreV.config(fg="#b81d28")
            lblP2PScoreDes.config(
                text="The Peer-to-Peer Lifespan was {}, and the corresponding Death Rate was {}. Additionally, the Contact Rate for IL was {}.\n\n"
                     "The Lifespan and Death Rate due to malicious Local Scanning activity results in the IL population group living much shorter than expected and performing much more malicious"
                     " activity.".format(C.peerToPeerLifespan, C.dthP, C.IpContactRate))

        lblDeathOvrV.grid(row=1, column=0, sticky="w", padx=(9, 0), pady=7)
        lblDeathOvr.grid(row=1, column=2, sticky="w")
        lblDeathOvrDes.grid(row=2, column=2, sticky="w", padx=(7, 0))

        lblExplain.grid(row=3, column=2, sticky="w", pady=(10, 0), padx=(7, 0))
        lblExplain2.grid(row=4, column=2, sticky="w", pady=(10, 0), padx=(7, 0))

        lblbttryScoreV.grid(row=5, column=0, sticky="w", padx=(9, 0))
        lblbttryScore.grid(row=5, column=2, sticky="w")
        lblbttryDes.grid(row=6, column=2, sticky="w", padx=(7, 0))
        lblbttryScoreDes.grid(row=7, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblBenignScoreV.grid(row=8, column=0, sticky="w", padx=(7, 0))
        lblBenignScore.grid(row=8, column=2, sticky="w")
        lblBenignDes.grid(row=9, column=2, sticky="w", padx=(9, 0))
        lblBenignScoreDes.grid(row=10, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblRandomScoreV.grid(row=11, column=0, sticky="w", padx=(7, 0))
        lblRandomScore.grid(row=11, column=2, sticky="w")
        lblRandomDes.grid(row=12, column=2, sticky="w", padx=(9, 0))
        lblRandomScoreDes.grid(row=13, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblLocalScoreV.grid(row=14, column=0, sticky="w", padx=(7, 0))
        lblLocalScore.grid(row=14, column=2, sticky="w")
        lblLocalDes.grid(row=15, column=2, sticky="w", padx=(9, 0))
        lblLocalScoreDes.grid(row=16, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblP2PScoreV.grid(row=17, column=0, sticky="w", padx=(7, 0))
        lblP2PScore.grid(row=17, column=2, sticky="w")
        lblP2PDes.grid(row=18, column=2, sticky="w", padx=(9, 0))
        lblP2PScoreDes.grid(row=19, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

    def populateSingleFactorFrame(self, config, ovrUncategorisedScore, startingPopScore, rrScore, idsScore):
        Jeff = 0
        C = config
        lblSFOvrV = tk.Label(self.frames[5], text="{}  ".format(ovrUncategorisedScore), font=("Arial", 14, "bold"),
                             bg="#e0e0e0")
        lblSFOvr = tk.Label(self.frames[5], text="> Overall Single Factors Score",
                            font=("Arial", 12, "bold", "italic"), bg="#e0e0e0")
        lblSFOvrDes = tk.Label(self.frames[5], font=("Arial", 10), bg="#e0e0e0")
        if Jeff < 1:
            lblSFOvrV.config(fg="#2d802f")
            lblSFOvrDes.config(
                text="In this simulation, these Single Factors have helped achieve a minimal virus propagation.")
        if 1 <= Jeff < 3:
            lblSFOvrV.config(fg="#e68f39")
            lblSFOvrDes.config(
                text="In this simulation, these Single Factors are at the expected thresholds and result in the expected botnet presence.")
        if Jeff >= 3:
            lblSFOvrV.config(fg="#b81d28")
            lblSFOvrDes.config(
                text="In this simulation, these Single Factors have contributed to a higher virus propagation.")

        lblExplain = tk.Label(self.frames[5],
                              text="This section looks at three particular starting conditions: Starting Population Sizes, Admin Engagement, and Intrusion Detection System"
                                   " (IDS) usage.\n\n"
                                   "The variables to be examined here share a common trait, each is based off of an estimated guess as to what would occur in reality if a scenario of a botnet"
                                   " attack occurred.",
                              font=("Arial", 10, "italic"), bg="#e0e0e0")

        lblStartScoreV = tk.Label(self.frames[5], text="{}  ".format(startingPopScore), font=("Arial", 12, "bold"),
                                  bg="#e0e0e0")
        lblStartScore = tk.Label(self.frames[5], text="> SLoc Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblStartDes = tk.Label(self.frames[5], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                               text="This variable decides the starting population sizes, the fraction of the total populaton N divided into either S or I nodes.\n\n"
                                    "The reccomended value for this model is for a single node to be divided into the I group to begin the attack. In this virus model, "
                                    "an abstraction of population spreads considering a range of different variables and rates deciding the change - a single node is enough to start a spread.\n\n"
                                    "The reality is that a strong and maintained attack force of bots is required for any botnet to gain traction and size. Despite this, "
                                    "a range of starting bot counts and N sizes are provided to demonstrate what different attack forces determine.\n")
        lblStartScoreDes = tk.Label(self.frames[5], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if Jeff == 0:
            lblStartScoreV.config(fg="#2d802f")
            lblStartScoreDes.config(
                text="Well done, with a starting I = {} - it is safe to say your systems were not attacked by a botnet!".format(
                    C.I))
        if Jeff < 1:
            lblStartScoreV.config(fg="#2d802f")
            lblStartScoreDes.config(
                text="Here the starting bot count was I = {}, pitched against S = {}.\n\n"
                     "A small attack force, the botnet will not peak as fast as expected.".format(C.I, C.S))
        if 1 <= Jeff < 3:
            lblStartScoreV.config(fg="#e68f39")
            lblStartScoreDes.config(
                text="Here the starting bot count was I = {}, pitched against S = {}.\n\n"
                     "A growing attack force, the botnet will peak in an expected amount of time.".format(C.I, C.S))
        if Jeff >= 3:
            lblStartScoreV.config(fg="#b81d28")
            lblStartScoreDes.config(
                text="Here the starting bot count was I = {}, pitched against S = {}.\n\n"
                     "A large starting attack force, the botnet will peak as faster than expected.".format(C.I, C.S))

        lblRRScoreV = tk.Label(self.frames[5], text="{}  ".format(rrScore), font=("Arial", 12, "bold"),
                               bg="#e0e0e0")
        lblRRScore = tk.Label(self.frames[5], text="> Security Level Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblRRDes = tk.Label(self.frames[5], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                            text="This variable is part of the model called the Recovery Rate - the rate at which nodes transition from the I populous back into S.\n\n"
                                 "The variable is based off of varying levels of Admin Engagement and Intervention during an attack - which is something only decided"
                                 " when a botnet attack actually occurs. The values for this rate are taken, like many others, directly from the proposers of the IoT-SIS Model.")
        lblRRScoreDes = tk.Label(self.frames[5], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if rrScore == 3:
            lblRRScoreV.config(fg="#2d802f")
            lblRRScoreDes.config(text="The Recovery Rate for this simulation was {}.\n\n"
                                      "The maximum Admin Engagement has been performed and reduced the number of nodes absorbed into the botnet.".format(
                C.recoveryRate))
        if rrScore == 2:
            lblRRScoreV.config(fg="#e68f39")
            lblRRScoreDes.config(text="The Recovery Rate for this simulation was {}.\n\n"
                                      "The medium Admin Engagement has been performed and reduced the number of nodes absorbed into the botnet, but increased engagement would result in a larger "
                                      "S population.".format(C.recoveryRate))
        if rrScore == 1:
            lblRRScoreV.config(fg="#b81d28")
            lblRRScoreDes.config(text="The Recovery Rate for this simulation was {}.\n\n"
                                      "The minimum Admin Engagement has been performed and increased the number of nodes absorbed into the botnet. There is room for much more engagement to "
                                      "reduce the state of infection.".format(C.recoveryRate))

        lblIDSScoreV = tk.Label(self.frames[5], text="{}  ".format(idsScore), font=("Arial", 12, "bold"),
                                bg="#e0e0e0")
        lblIDSScore = tk.Label(self.frames[5], text="> IDS Usage Score", font=("Arial", 10, "bold"), bg="#e0e0e0")
        lblIDSDes = tk.Label(self.frames[5], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left",
                             text="The final variable to be assessed is unique in multiple ways - it is the only binary choice option, but is more importantly not part of the original IoT-SIS model.\n\n"
                                  "The inclusion of this variable is a proof of concept, adding in another parameter to increase oppertunity and realism for real word applications.\n\n"
                                  "This variable acts the same as the Recovery Rate based off of admin engagement; the use of an Intrusion Detection System seeks to aid system admins identify"
                                  " and neutralise malicious traffic. Thus, activating this option will also increase the number of nodes recovering back to the S populous.")
        lblIDSScoreDes = tk.Label(self.frames[5], font=("Arial", 10), bg="#e0e0e0", wraplength=1050, justify="left")
        if idsScore == 2:
            lblIDSScoreV.config(fg="#2d802f")
            lblIDSScoreDes.config(
                text="An IDS has been activated for this sumulation and has aided the system admins manage the botnet attack.")
        if idsScore == 0:
            lblIDSScoreV.config(fg="#b81d28")
            lblIDSScoreDes.config(
                text="An IDS has not been activated for this simulation; the admins have had a harder task intervening in the attack and thus more nodes have been lost to the botnet.")

        lblSFOvrV.grid(row=1, column=0, sticky="w", padx=(9, 0), pady=7)
        lblSFOvr.grid(row=1, column=2, sticky="w")
        lblSFOvrDes.grid(row=2, column=2, sticky="w", padx=(7, 0))

        lblExplain.grid(row=3, column=2, sticky="w", pady=(10, 0), padx=(7, 0))

        lblStartScoreV.grid(row=5, column=0, sticky="w", padx=(9, 0))
        lblStartScore.grid(row=5, column=2, sticky="w")
        lblStartDes.grid(row=6, column=2, sticky="w", padx=(7, 0))
        lblStartScoreDes.grid(row=7, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblRRScoreV.grid(row=8, column=0, sticky="w", padx=(9, 0))
        lblRRScore.grid(row=8, column=2, sticky="w")
        lblRRDes.grid(row=9, column=2, sticky="w", padx=(7, 0))
        lblRRScoreDes.grid(row=10, column=2, sticky="w", padx=(7, 0), pady=(0, 10))

        lblIDSScoreV.grid(row=11, column=0, sticky="w", padx=(9, 0))
        lblIDSScore.grid(row=11, column=2, sticky="w")
        lblIDSDes.grid(row=12, column=2, sticky="w", padx=(7, 0))
        lblIDSScoreDes.grid(row=13, column=2, sticky="w", padx=(7, 0), pady=(0, 10))
