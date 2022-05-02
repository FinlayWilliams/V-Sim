# V-Sim 
## A Virus Spread Simulation Tool for Botnet Propagation in IoT Devices

*COMP3000 Final Year Project*

### About the Application

V-Sim is a tool that simulates the IoT-SIS Virus Model proposed in *Modelling the Spread of Botnet Malware in IoT-Based Wireless Sensor Networks* by Dilara Acarali, Muttukrishnan Rajarajan, Nikos Komninos, and B. B. Zarpelão.

It models botnet virus propagation through IoT devices, such as IoT-based wireless sensor nodes.

The goal is to provide users with an in-depth understanding of not only how these models work, but of how IoT devices are impacted by botnets and viruses; what factors make the virus spread wider or lesser.

The application comes with a set of configurations displaying a range of different scenarios - but allows the user to create an many configurations as they desire - alterable in anyway, providing commentary and feedback on the resulting virus spread.

To run the application, either clone the repository into a IDE, or download V-Sim.zip from <a id="raw-url" href="https://github.com/FinlayWilliams/V-Sim/releases/download/FinalRelease/V-Sim.zip">HERE</a> (or check the <a id="raw-url" href="https://github.com/FinlayWilliams/IoT_SIS_Sim/releases">Releases Section</a> of this repository and find V-Sim.zip), extract the contents anywhere, and then navigate to (and run) main.exe.

The free online tool <a id ="raw-url" href="https://pypi.org/project/auto-py-to-exe/">auto-py-to-exe</a> was used to quickly convert the project files into a runnable application. 

### Application Interfaces:

#### Home Screen:
![alt text](https://i.gyazo.com/7e4f2f6954523219aaf98c7fa2b9ec3b.png "Application Home Screen")

This is the home screen, the interface reached when launching the application. From here, all saved IoT-SIS Model configurations can be accessed, as well as all of the features of the application.

#### Configuration Inspect Screen:
![alt text](https://i.gyazo.com/eabae6418496adb92b8d9e98297d35de.png "Application Configuration Inspect Screen")

The Configuration Inspection interface allows the exploration of all variables and conditions within the model, contributing towards the result (the virus propagation) of the selected configuration. From here, the configuration scores can be veiwed as well.

#### Configuration Control Screen:
![alt text](https://i.gyazo.com/13e1bcfd520b96a0df793b2384333a08.png "Application Configuration Inspect Screen")

This interface is where each configuration can be edited and controlled from. Each starting condition can be altered, with the outcome instantly observed. 

#### Configuration Comparison Screen:
![alt text](https://i.gyazo.com/eb6d82d1068d56d005b947c466d4f2d6.png "Application Configuration Inspect Screen")

Finally, the configuration comparison screen allows the user to select two different configurations and compare them side-by-side in order to quickly view which one has done better, and where.


### Legal, Ethical, Social, Professional Notice

This application provides the oppertunity to understand a complex issue within computing, and supplies knowledge on how to reduce the damage cause by botnets and virus propagation inside networks of IoT devices. 

The aim is to build an understanding on the topic; due to the nature of compartmental modelling, the results are an abstraction of real world events and are not 100% accurate. 

Furthermore, the results obtained should not be used directly in practise when developing applications or utilising tools defending real work networks.
