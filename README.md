# Wiled Fire Simulator 

This project is a celular autometa model of a wild fire that alows the user to adjust some peramiters of the fire and observe the resultant changes in the model. It is intended to help visually explore how wild fires may be simulated using a number of parameters that govern the spread of fire, such as tree growth rate, potential energy density of fuel, and dead-fall accumulation.

![Simulation Demo](demo.gif)
## Instalation
* Clone the repository
* Navigate to the directory
* (Optional) Set up a virtual environment
* Install dpendencies
  
  `bash
pip install -r requirements.txt
  `
## Usage
run the forest.py file in the command line
`bash
python3 forest.py
`
This program is a command line application that displays ascii graphics to represents the wild fire. The user enters commands in the command line to interact with the simulation. Valid commands include:

* **q** -  Ends the simulation
- **fr** -  Display the current fire rate (The rate at which any tree will spontaneously catch fire) and offer the opportunity to enter a new value for the fire rate. The default fire rate is 0.00003.
- **tf** - Display a truncated version of a data frame that contains all the trees in the simulated forest and their associated parameters.
- **?** - Display a list of valid commands.
- Press `Enter` without entering anything in the command line to advance the simulation foward one step, or hold down the the `Enter` key to to allow the simulation to progres
