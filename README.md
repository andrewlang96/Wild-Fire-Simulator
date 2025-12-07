# Wiled Fire Simulator 

This project is intended to help visually explore how wild fires may be simulated using a number of parameters that govern the spread of fire, such as tree growth rate, potential energy density of fuel, and dead-fall accumulation. While the values assigned to these parameters are not based on any real world data, the user is able to change the values of these parameters and observe the resultant changes in the simulation. I'm interested in bringing the simulation into alignment with experimentally observed phenomena by tuning these values. In doing so I hope to better understand what variables are critical for simulating and predicting the behavior of these systems. 

#### Features
![Simulation Demo](demo.gif)
This program is a command line application that displays ascii graphics to represents the wild fire. The user enters commands in the command line to interact with the simulation. Valid commands include (Entered without quotation marks)

* "q" This command the end the simulation
- "" An empty input will iterate the simulation by one step. The simulation can be run continuously by holding down the enter key.
- "fr" This command will display the current fire rate (The rate at which any tree will spontaneously catch fire) and offer the opportunity to enter a new value for the fire rate. The default fire rate is 0.00003.
- "tf" This command displays a truncated version of a data frame that contains all the trees in the simulated forest and their associated parameters.
- "?" This command will display a list of valid commands.

#### Program Execution
To run this program simply run the file ***forest.py*** in the terminal window and then hold down the **Enter** key to allow the simulation to progress.