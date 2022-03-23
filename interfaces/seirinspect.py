import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class SEIRInspectInterface(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.index = 0

        #################################### Instantiating Information Frame ########################################
        # These are the basic controls of this page alling the user to navigate
        mainFrame = tk.Frame(self, bg="#574b59")
        controlBar = tk.Frame(mainFrame, bg="#453354")
        btnReturn = tk.Button(controlBar, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                               command=lambda: controller.display("SEIRInspectInterface", "HomeInterface"))
        self.lblControl = tk.Label(controlBar, bg="#453354", text="",
                              font=("Arial", 14, "italic"), fg="white" )
        btnOverview = tk.Button(mainFrame, text="Overview", font=("Arial", 9), width=13,
                                command=lambda : self.switchInfoFrame(0, 1))
        btnPopulation = tk.Button(mainFrame, text="Population", font=("Arial", 9), width=13,
                                  command=lambda : self.switchInfoFrame(1, 1))
        btnBetaRate = tk.Button(mainFrame, text="Beta rate", font=("Arial", 9), width=13,
                                    command=self.controller.activeModel.calculateScores())
        btnGammaRate = tk.Button(mainFrame, text="Gamma rate", font=("Arial", 9), width=13,
                                     command=lambda : self.switchInfoFrame(3, 1))
        btnMuRate = tk.Button(mainFrame, text="Mu rate", font=("Arial", 9), width=13,
                                command=self.controller.activeModel.calculateScores())
        btnAlphaRate = tk.Button(mainFrame, text="Alpha rate", font=("Arial", 9), width=13,
                                 command=lambda: self.switchInfoFrame(3, 1))
        btnMiscellaneous = tk.Button(mainFrame, text="Miscellaneous", font=("Arial", 9), width=13,
                                     command=lambda : self.switchInfoFrame(6, 1))

        # This area will contain the assessment and a starter list is created
        self.informationFrame = tk.Frame(mainFrame, bg="#e0e0e0")
        self.frames = [tk.Frame(self.informationFrame, bg="#a8a8a8"), tk.Frame(self.informationFrame, bg="blue"),
                       tk.Frame(self.informationFrame, bg="green"), tk.Frame(self.informationFrame, bg="yellow"),
                       tk.Frame(self.informationFrame, bg="#654e78"), tk.Frame(self.informationFrame, bg="yellow"),
                       tk.Frame(self.informationFrame, bg="#654e78")]

        # This is the legend footer of the page
        lblLegend1 = tk.Label(mainFrame, bg="#2ca02c", width=25, pady=4, text="(S) Susceptible",
                              font=("Arial", 9), fg="white")
        lblLegend2 = tk.Label(mainFrame, bg="#d62728", width=25, pady=4, text="(E) Exposed",
                              font=("Arial", 9), fg="white")
        lblLegend3 = tk.Label(mainFrame, bg="#d62728", width=25, pady=4, text="(I) Infected",
                              font=("Arial", 9), fg="white")
        lblLegend4 = tk.Label(mainFrame, bg="#1f77b4", width=27, pady=4, text="(R) Recovered",
                              font=("Arial", 9), fg="white")

        ####################################### Placing Information Frame ###########################################
        mainFrame.place(relheight=1, relwidth=0.6)
        controlBar.place(relheight=0.087, relwidth=1)
        btnReturn.place(x=21, y=21)
        self.lblControl.pack(ipady=21)
        btnOverview.place(x=51, y=87)
        btnPopulation.place(x=166, y=87)
        btnBetaRate.place(x=281, y=87)
        btnGammaRate.place(x=396, y=87)
        btnMuRate.place(x=511, y=87)
        btnAlphaRate.place(x=626, y=87)
        btnMiscellaneous.place(x=741, y=87)
        self.informationFrame.place(x=14, y=124, relheight=0.83, relwidth=0.97)
        lblLegend1.place(x=0, y=837)
        lblLegend2.place(x=172, y=837)
        lblLegend3.place(x=353, y=837)
        lblLegend4.place(x=525, y=837)

        ########################################## Instantiating Graphs #############################################
        graphFrame = tk.Frame(self, bg="#453354")
        self.lblGraphTitle = tk.Label(graphFrame, bg="#453354", text="Assessment Overview", font=("Arial", 14, "italic"), fg="white")
        btnConfigure = tk.Button(graphFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
                                 relief="ridge", fg="white", bg="#6e6e6e",
                                 command=lambda: controller.display("SEIRInspectInterface", "SEIRControlInterface"))
        graphContainer = tk.Frame(graphFrame, bg="#654e78")

        figure = plt.figure(facecolor="#654e78")
        self.canvas = FigureCanvasTkAgg(figure, graphContainer)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.ax = [figure.add_subplot(3, 1, x + 1, facecolor="#453354") for x in range(3)]
        for x in range(2):
            self.ax[x].ticklabel_format(style="plain")
        figure.tight_layout(rect=[0.1, 0.03, 0.95, 0.95], h_pad=2)

        ############################################# Placing Graphs ################################################
        graphFrame.place(x=922, y=0, relheight=1, relwidth=0.4)
        self.lblGraphTitle.pack(ipady=21)
        btnConfigure.place(x=541, y=21)
        graphContainer.place(x=5, y=75, relheight=0.96, relwidth=1)
        self.updateGraphs()

    # Updates the on-screen graphs
    def updateGraphs(self):
        S1, E1, I1, R1 = self.controller.activeModel.runModel()
        T1 = np.linspace(0, self.controller.activeModel.Timesteps, 101)

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(2)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, S1, "#2ca02c", label="Exposed")
        self.ax[0].plot(T1, I1, "#d62728", label="Infected")
        self.ax[0].plot(T1, R1, "#1f77b4", label="Recovered")
        self.ax[0].set_xlabel("Timesteps (Days)")
        self.ax[0].set_ylabel("Population Count")
        self.ax[0].set_title("Population Sizes Over Time - S, I, R")
        # Plotting the second graph
        pop = [S1[len(S1) - 1], E1[len(I1) - 1], I1[len(I1) - 1], R1[len(R1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Exposed: {:.0f}".format(pop[1]),
                  "Infected: {:.0f}".format(pop[2]), "Recovered: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#d62728", "#1f77b4"]
        self.ax[1].pie(pop, explode=explode, labels=labels, colors=colours)
        self.ax[1].set_title(
            "Population Sizes on Final Recorded Day #{}".format(self.controller.activeModel.Timesteps))

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
            self.lblControl.config(text="Population")
        if index == 2:
            self.frames[self.index].pack_forget()
            self.index = 2
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Beta rate")
        if index == 3:
            self.frames[self.index].pack_forget()
            self.index = 3
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Gamma Rate")
        if index == 4:
            self.frames[self.index].pack_forget()
            self.index = 4
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Mu rate")
        if index == 5:
            self.frames[self.index].pack_forget()
            self.index = 5
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Alpha Rate")
        if index == 6:
            self.frames[self.index].pack_forget()
            self.index = 6
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Miscellaneous")

    # Populates all of the information frames, ready to be deployed, the bulk of content on this page
    def populateFrames(self):
        # This loop ensures the frames are destroyed and reconstructed with correct information when the frame is opened
        if self.frames:
            for frame in self.frames:
                frame.destroy()

            self.frames = [tk.Frame(self.informationFrame, bg="#e0e0e0"), tk.Frame(self.informationFrame, bg="blue"),
                           tk.Frame(self.informationFrame, bg="green"), tk.Frame(self.informationFrame, bg="yellow"),
                           tk.Frame(self.informationFrame, bg="#654e78"), tk.Frame(self.informationFrame, bg="yellow"),
                           tk.Frame(self.informationFrame, bg="#654e78")]

        model = self.controller.activeModel

        # This section populates each of the frames with updated information conforming to the active models simulation
        # By calling the methods that add the page widgets
        # There are many if statements indicating thresholds that change the displayed information

    # The following 7 methods are the assessment frame contents
    def populateOverview(self, model, populationScore, sizeScore, neighbourScore, infectionRateScore, deathRateScore, miscScore):
        pass

    def populatePopulationFrame(self, model, populationScore, startPopScore, endPopScore):
        pass

    def populateBetaFrame(self, model, sizeScore):
        pass

    def populateGammaFrame(self, model, neighbourScore):
        pass

    def populateMuFrame(self, model, infectionScore):
        pass

    def populateAlphaFrame(self, model, deathScore):
        pass

    def populateMiscFrame(self, model, miscScore):
        pass
