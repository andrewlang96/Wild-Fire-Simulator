import pandas as pd
import random
from colorama import Fore, Back, Style
from datetime import datetime as dt
import os
import platform
from time import sleep



class Tree:
    def __init__(self):
        upper_burn = 0.005 #This is a value that im unsure about defining. it is the upper bound of the fraction of the age of a tree to its burn time.
        self.age = 0 #number of cycles survived
        self.groth_rate = random.random() #0<x<1 amount that tree grows per cycle
        self.heat_resistence = random.random() #0<x<1 heat resistence factor gained per cycle survived
        self.heat_potential = random.uniform(0.5, 0.9) #0<x<1 Potential heat output per size of tree per cycle
        self.seed_prob = random.uniform(0, 0.5) #The probability that this tree will contribute to the seeding of an empty adjacent plot
        self.is_burning = False
        self.burn_duration_factor = random.uniform(0, upper_burn) #0<x<upper_burn Cycles of burn time per age
        self.burn_duration = None #Number of cycles that the tree will burn. To be assigned once the tree ignites.
        self.burn_cycle_count = 0 #Number of cycles that the tree has been burning
        self.experienced_temperature = 0 #Temperature that the tree is experiencing
        self.sprite = f"{Fore.GREEN} +{Style.RESET_ALL}"
        self.dead_fall = 0 #Amount of dead flameable material unter tree
        self.dead_fall_age = 0 #Amout of time since dead fall last burned off


    def update_age(self, step=1): #Increse the age of the tree by step up to max age
        self.age += step
        self.dead_fall_age += step
        self.update_sprite()


    def update_deadfall(self):
        self.dead_fall_age += 1
        self.dead_fall += 10 ** ((self.dead_fall_age/20) - 50)


    def get_size(self, max_size=10): #Return updated size of the tree as a function of its age
        size = self.groth_rate * self.age
        return size
        # if size <= max_size:
        #     return size
        # else:
        #     return max_size


    def update_sprite(self):
        if self.is_burning:
            self.sprite = f"{Fore.RED} @{Style.RESET_ALL}" #Red sprite


    def get_heat_resistence(self): #Return updated resistence of the tree as a function of its size
        resistence = (self.heat_resistence * self.age) - self.dead_fall
        return resistence


    # def ignition_check(self, heat): #Check of current temperature is sufficient to ignite the tree
    #     if heat >= self.heat_resistence:
    #         self.is_burning = True
    #         # self.burn_duration = self.get_burn_duration()


    def get_heat_output(self): #Returns how much heat a burning tree is putting out as a function of its size
        if self.is_burning:
            return self.heat_potential * self.get_size()
        else:
            return 0


    def get_burn_duration(self): #Return the amount of time that a tree will burn after igniting
        burnout = round(self.burn_duration_factor * self.age)
        if burnout > 0:
            return burnout
        else:
            return 1



class Forest:
    def __init__(self, height=50, width=50, tree_rate=0.01, fire_rate=0.00003):
        self.height = height
        self.width = width
        self.tree_rate = tree_rate #Probability that each empty plot will start growing a tree each cycle
        self.fire_rate = fire_rate #Probability that each try will spontaniously ignite each cycle
        self.plot_count = height * width #number of trees that the forest can accomedate
        self.forest = [None for i in range(self.plot_count)] #List of all the trees in the forest.


    def check_plot_temperature(self, tree): #Returns the sum of the heat output from the 8 plots surounding the tree
        temp = 0
        ind = self.forest.index(tree)
        adjacent_plots = [ind+1, ind-1, ind+1-self.width, ind-1-self.width, ind+1+self.width, #Index of ever plot adjacent to the tree
                          ind-1+self.width, ind-self.width, ind+self.width]
        for i in adjacent_plots:
            try:
                if self.forest[i] == None:
                    pass
                else:
                    temp += self.forest[i].get_heat_output()
            except IndexError:
                pass
        return temp


    def update_forest(self):
        for ind, plot in enumerate(self.forest): #Update expeienced temperature of each tree and check if any tree is burned out.
            if plot == None: #If the plot has no tree
                if random.random() <= self.tree_rate: #Check if tree will grow
                    self.forest[ind] = Tree() #Plant a tree
                    self.forest[ind].update_sprite()
            else: #The plot has a tree
                if random.random() < self.fire_rate: #Check if tree will spontaniously ignite:
                    self.forest[ind].is_burning = True #Tree ignites
                    self.forest[ind].update_sprite()
                    self.forest[ind].burn_duration = self.forest[ind].get_burn_duration()
                if not plot.is_burning: #Tree is not burning
                    self.forest[ind].update_age()
                    self.forest[ind].update_deadfall()
                    self.forest[ind].experienced_temperature = self.check_plot_temperature(plot) #Update experienced temperature of the tree for this cycle
                else: #Tree is burning
                    if self.forest[ind].burn_cycle_count >= self.forest[ind].burn_duration: #Tree has burnt out
                        self.forest[ind] = None #Reset to empty plot
                    else: #Tree has not burnt out
                        self.forest[ind].burn_cycle_count += 1
        for ind, plot in enumerate(self.forest): #Check if any trees will ignite due to their experienced temperature.
            if ((plot != None) and not (plot.is_burning)): #The plot has a tree that is not burning
                if plot.experienced_temperature > plot.get_heat_resistence(): #Eperienced heat excedes heat resistence of the tree
                    self.forest[ind].is_burning = True #Tree catches on fire
                    self.forest[ind].update_sprite()
                    self.forest[ind].burn_duration = self.forest[ind].get_burn_duration()
                if plot.experienced_temperature > 0:
                    plot.dead_fall_age = 0
                    plot.dead_fall = 0


    def display_forest(self): #Take list of trees and print their associated sprites to the terminal window
        for i in range(self.height):
            row = "".join([tree.sprite if tree != None else "  " for tree in self.forest[i*self.width:(i+1)*self.width]])
            print(row)


    def get_tree_df(self): #Generate pandas df of existing trees in the forest and their specs
        trees = [tree for tree in self.forest if tree != None]
        tree_specs = {"tree": [tree for tree in trees],
                      "height": [tree.get_size() for tree in trees],
                      "age": [tree.age for tree in trees],
                      "heat dencity": [tree.heat_potential for tree in trees],
                      "heat potential": [(tree.heat_potential * tree.get_size()) for tree in trees],
                      "dead fall": [tree.dead_fall for tree in trees]}
        tree_df = pd.DataFrame(tree_specs)
        return tree_df


    def clear(self): #Clear terminal window
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")



def main():
    f = Forest(50, 50, fire_rate=0.00003, tree_rate=0.01)
    sleep_time = 0.05 #Delay time between each fram of the simulation
    valid_commands = {"q": "End simulation", #Valid commands and their associated function
                      "": "Continue Simulation",
                      "fr": "Change fire rate",
                      "tf": "Display tree data frame",
                      "?": "display valid commands"}
    while True:
        command = input("> ") #Prompt user for input
        if command == "": #Continue itterating the simulation
            f.clear()
            f.update_forest()
            f.display_forest()
            sleep(sleep_time)
        elif command == "fr": #Display current fire rate and prompt user to enter a new rate
            print(f"The current fire rate is {f.fire_rate}")
            try:
                f.fire_rate = float(input("Enter the new fire rate: "))
            except ValueError: #If the input cant be converted to float then nothing happens
                pass
        elif command == "q": #End the simulation
            heights = [i.get_size() for i in f.forest if i != None]
            break
        elif command == "tf": #Display truncated tree data frame
            print(f.get_tree_df())
        elif command == "?": #Display valid commands and their associated functions
            for command in valid_commands:
                print(f"{command}: {valid_commands[command]}")



if __name__ == "__main__":
    main()


