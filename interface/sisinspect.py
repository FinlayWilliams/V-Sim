import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

class SISInspectInterface(tk.Frame):
    # Default constructor passing in the master object (base frame) and the controller (the BaseApp class)
    # it also creates and places all widgets for this interface
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.index = 0

        #################################### Instantiating Information Frame ########################################

        # These are the basic controls of this page alling the user to navigate
        mainFrame = tk.Frame(self, bg="#654e78")
        controlBar = tk.Frame(mainFrame, bg="#453354")
        btnReturn = tk.Button(controlBar, wraplength=41, width=7, text="Return Home", font=("Arial", 7),
                              relief="ridge", fg="white", bg="#6e6e6e",
                               command=lambda: controller.display("SISInspectInterface", "HomeInterface"))
        self.lblControl = tk.Label(controlBar, bg="#453354", text="",
                              font=("Arial", 14, "italic"), fg="white" )
        btnOverview = tk.Button(mainFrame, text="Overview", font=("Arial", 9), width=13,
                                command=lambda : self.switchInfoFrame(0, 1))
        btnPopulation = tk.Button(mainFrame, text="Population", font=("Arial", 9), width=13,
                                  command=lambda : self.switchInfoFrame(1, 1))
        btnPhysicalSize = tk.Button(mainFrame, text="Physical Size", font=("Arial", 9), width=13,
                                    command=lambda : self.switchInfoFrame(2, 1))
        btnNeighbourSets = tk.Button(mainFrame, text="Neighbour Sets", font=("Arial", 9), width=13,
                                     command=lambda : self.switchInfoFrame(3, 1))
        btnInfectionRates = tk.Button(mainFrame, text="Infection Rates", font=("Arial", 9), width=13,
                                      command=lambda : self.switchInfoFrame(4, 1))
        btnDeathRates = tk.Button(mainFrame, text="Death Rates", font=("Arial", 9), width=13,
                                  command=lambda : self.switchInfoFrame(5, 1))
        btnMiscellaneous = tk.Button(mainFrame, text="Miscellaneous", font=("Arial", 9), width=13,
                                     command=lambda : self.switchInfoFrame(6, 1))

        # This area will contain the assessment and a starter list is created
        self.informationFrame = tk.Frame(mainFrame, bg="#453354")
        self.frames = [tk.Frame(self.informationFrame, bg="red"), tk.Frame(self.informationFrame, bg="blue"),
                       tk.Frame(self.informationFrame, bg="green"), tk.Frame(self.informationFrame, bg="yellow"),
                       tk.Frame(self.informationFrame, bg="#654e78"), tk.Frame(self.informationFrame, bg="#453354"),
                       tk.Frame(self.informationFrame, bg="#6e6e6e")]

        # This is the legend footer of the page
        lblLegend1 = tk.Label(mainFrame, bg="#2ca02c", width=25, pady=4, text="(S) Susceptible",
                              font=("Arial", 9), fg="white")
        lblLegend2 = tk.Label(mainFrame, bg="#9467bd", width=25, pady=4, text="(IR) Random-Scanning",
                              font=("Arial", 9), fg="white")
        lblLegend3 = tk.Label(mainFrame, bg="#1f77b4", width=27, pady=4, text="(IL) Local-Scanning",
                              font=("Arial", 9), fg="white")
        lblLegend4 = tk.Label(mainFrame, bg="#17becf", width=27, pady=4, text="(IP) Peer-to-Peer",
                              font=("Arial", 9), fg="white")
        lblLegend5 = tk.Label(mainFrame, bg="#d62728", width=27, pady=4,
                              text="(I) Infection Types Grouped", font=("Arial", 9), fg="white")

        ####################################### Placing Information Frame ###########################################

        mainFrame.place(relheight=1, relwidth=0.6)
        controlBar.place(relheight=0.087, relwidth=1)
        btnReturn.place(x=21, y=21)
        self.lblControl.pack(ipady=21)
        btnOverview.place(x=51, y=87)
        btnPopulation.place(x=166, y=87)
        btnPhysicalSize.place(x=281, y=87)
        btnNeighbourSets.place(x=396, y=87)
        btnInfectionRates.place(x=511, y=87)
        btnDeathRates.place(x=626, y=87)
        btnMiscellaneous.place(x=741, y=87)

        self.informationFrame.place(x=14, y=135, relheight=0.81, relwidth=0.97)

        lblLegend1.place(x=0, y=837)
        lblLegend2.place(x=172, y=837)
        lblLegend3.place(x=353, y=837)
        lblLegend4.place(x=548, y=837)
        lblLegend5.place(x=731, y=837)

        ########################################## Instantiating Graphs #############################################

        graphFrame = tk.Frame(self, bg="#453354")
        self.lblGraphTitle = tk.Label(graphFrame, bg="#453354", text="Assessment Overview", font=("Arial", 14, "italic"), fg="white")
        btnConfigure = tk.Button(graphFrame, wraplength=41, width=7, text="Configure Model", font=("Arial", 7),
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

        ############################################# Placing Graphs ################################################

        graphFrame.place(x=922, y=0, relheight=1, relwidth=0.4)
        self.lblGraphTitle.pack(ipady=21)
        btnConfigure.place(x=541, y=21)
        graphContainer.place(x=5, y=75, relheight=0.96, relwidth=1)
        self.updateGraphs()

    # Method: Updates the on-screen graphs
    def updateGraphs(self):
        S1, Ir1, Il1, Ip1 = self.controller.activeModel.runModel()
        I1 = Ir1 + Il1 + Ip1
        T1 = np.linspace(0, self.controller.activeModel.Timesteps, 101)

        # Setting the title
        self.lblGraphTitle.config(text="{} - Virus Propagation".format(self.controller.activeModel.Name))

        # Wiping all four axes of the figure (clearing all graphs)
        [self.ax[x].clear() for x in range(3)]

        # Plotting the first graph
        self.ax[0].plot(T1, S1, "#2ca02c", label="Susceptible")
        self.ax[0].plot(T1, Ir1, "#9467bd", label="Random-Scanning Infected")
        self.ax[0].plot(T1, Il1, "#1f77b4", label="Local Scanning Infected")
        self.ax[0].plot(T1, Ip1, "#17becf", label="Peer-to-Peer Infected")
        self.ax[0].set_xlabel("Timesteps (Days)")
        self.ax[0].set_ylabel("Node Count")
        self.ax[0].set_title("Node Population Sizes Over Time - S, IR, IL, IP")
        # Plotting the second graph
        self.ax[1].plot(T1, S1, '#2ca02c', label="Susceptible")
        self.ax[1].plot(T1, I1, '#d62728', label="All Infected")
        self.ax[1].set_xlabel("Timesteps (Days)")
        self.ax[1].set_ylabel("Node Count")
        self.ax[1].set_title("Node Population Sizes Over Time - S, I = (IR + IL + IP)")
        # Plotting the third graph
        pop = [S1[len(S1) - 1], Ir1[len(Ir1) - 1], Il1[len(Il1) - 1], Ip1[len(Ip1) - 1]]
        explode = (0.1, 0, 0, 0)
        labels = ["Susceptible: {:.0f}".format(pop[0]), "Random-Scanning Infected: {:.0f}".format(pop[1]),
                  "Local Scanning Infected: {:.0f}".format(pop[2]), "Peer-to-Peer Infected: {:.0f}".format(pop[3])]
        colours = ["#2ca02c", "#9467bd", "#1f77b4", "#17becf"]
        self.ax[2].pie(pop, explode=explode, labels=labels, colors=colours)
        self.ax[2].set_title("Population Sizes on Final Recorded Day #{}".format(self.controller.activeModel.Timesteps))

        self.canvas.draw()

    # Method: Called each time the page is set to display the assessment of the current model
    # also provides the functionality to switch between the frames
    def switchInfoFrame(self, index, stub):
        if index == 0:
            #self.frames[index].destroy()
            self.frames[self.index].pack_forget()
            self.index = 0
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Assessment Overview")
        if index == 1:
            #self.frames[index].destroy()
            self.frames[self.index].pack_forget()
            self.index = 1
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Population")
        if index == 2:
            #self.frames[index].destroy()
            self.frames[self.index].pack_forget()
            self.index = 2
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Physical Size")
        if index == 3:
            #self.frames[index].destroy()
            self.frames[self.index].pack_forget()
            self.index = 3
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Neighbour Sets")
        if index == 4:
            #self.frames[index].destroy()
            self.frames[self.index].pack_forget()
            self.index = 4
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Infection Rates")
        if index == 5:
            #self.frames[index].destroy()
            self.frames[self.index].pack_forget()
            self.index = 5
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Death Rates")
        if index == 6:
            #self.frames[index].destroy()
            self.frames[self.index].pack_forget()
            self.index = 6
            self.frames[index].pack(fill="both", expand=1)
            self.lblControl.config(text="Miscellaneous")

    # Method: Populates all of the information frames, ready to be deployed, the bulk of content on this page
    def populateFrames(self):
        modelScore = 0
        model = self.controller.activeModel

        # This loop ensures the frames are destroyed and reconstructed with correct information when the frame is opened
        if self.frames:
            for frame in self.frames:
                frame.destroy()

            self.frames = [tk.Frame(self.informationFrame, bg="red"), tk.Frame(self.informationFrame, bg="blue"),
                           tk.Frame(self.informationFrame, bg="green"), tk.Frame(self.informationFrame, bg="yellow"),
                           tk.Frame(self.informationFrame, bg="#654e78"), tk.Frame(self.informationFrame, bg="#453354"),
                           tk.Frame(self.informationFrame, bg="#6e6e6e")]

        # This section populates each of the frames with updated information conforming to the active models simulation
        # There are many if statements indicating thresholds that change the displayed information while also scoring
        # the active model

        ########## Population Frame #########
        lblTitle2 = tk.Label(self.frames[1], text="Bitch")
        lblTitle2.pack()

        ########## Size Frame #########

        ########## Neighbour Sets Frame #########

        ########## Infection Rates Frame #########

        ########## Death Rates Frame #########

        ########## Miscellaneous Frame #########

        ########## Overview Frame ########## (Done last to score correctly)
        lbl1 = tk.Label(self.frames[0], text="{} Overview".format(model.Name), font=("Arial", 12))

        lblScoreAc = tk.Label(self.frames[0], text="{}".format(modelScore), font=("Arial", 10))
        lblScore = tk.Label(self.frames[0], text=": Overall Model Score", font=("Arial", 10))
        lblScoreDes = tk.Label(self.frames[0], font=("Arial", 10), bg="green")
        if modelScore < 1:
            lblScoreDes.config(text="A low score; This model has a configuration that results in a generally slower and less potent propagation.")
        if modelScore < 2:
            lblScoreDes.config(text="A medium score; This model has a configuration that results in an average propagation of a virus.")
        if modelScore < 3:
            lblScoreDes.config(text="A high score; This model has a configuration that results in a fast and potent virus propagation.")
        lblExplain = tk.Label(self.frames[0], text="The score is broken down into different categories and combine to produce the overall score.", font=("Arial", 10))
        lblExplain2 = tk.Label(self.frames[0], text="The scores for those categories are as follow:", font=("Arial", 10))

        lbl1.grid(row=0, column=1, sticky="w")
        lblScoreAc.grid(row=1, column=0, sticky="w")
        lblScore.grid(row=1, column=1, sticky="w")
        lblScoreDes.grid(row=2, column=1, sticky="w")
        lblExplain.grid(row=3, column=1, sticky="w", pady=(3, 0))
        lblExplain.grid(row=3, column=1, sticky="w", pady=(3, 0))

