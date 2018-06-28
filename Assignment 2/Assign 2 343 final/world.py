#!/usr/bin/env python
#8168187
#Cameron McLennan
#COSC343 2018
from cosc343world import Creature, World
import numpy as np
import time
import matplotlib.pyplot as plt
import random
import csv
import collections
info = []
life = []
graph = []
averageArray = []
graph1 = []

totalAvgSurvivalRate = 0
# You can change this number to specify how many generations creatures are going to evolve over.
numGenerations = 450

# You can change this number to specify how many turns there are in the simulation of the world for a given generation.
numTurns = 150

# You can change this number to change the world type.  You have two choices - world 1 or 2 (described in
# the assignment 2 pdf document).
worldType=1

# You can change this number to modify the world size.
gridSize=24

# You can set this mode to True to have the same initial conditions for each simulation in each generation - good
# for development, when you want to have some determinism in how the world runs from generation to generation.
repeatableMode=False

# This is a class implementing you creature a.k.a MyCreature.  It extends the basic Creature, which provides the
# basic functionality of the creature for the world simulation.  Your job is to implement the AgentFunction
# that controls creature's behaviour by producing actions in response to percepts.
class MyCreature(Creature):
    randomGen = random.randint(0,1)
    randomGenSmall = randomGen/2
    chromosomeArray = [None]*12
    
 

    # Initialisation function.  This is where your creature
    # should be initialised with a chromosome in a random state.  You need to decide the format of your
    # chromosome and the model that it's going to parametrise.
    #
    # Input: numPercepts - the size of the percepts list that the creature will receive in each turn
    #        numActions - the size of the actions list that the creature must create on each turn
    def __init__(self, numPercepts, numActions, chrome=None):
        # Place your initialisation code here.  Ideally this should set up the creature's chromosome

        if chrome is None:
            self.chrome = np.random.uniform(0, 1, size=numActions)
        else:
            self.chrome = chrome

        # Do not remove this line at the end - it calls the constructors of the parent class.
        Creature.__init__(self)






    # This is the implementation of the agent function, which will be invoked on every turn of the simulation,
    # giving your creature a chance to perform an action.  You need to implement a model here that takes its parameters
    # from the chromosome and produces a set of actions from the provided percepts.
    #
    # Input: percepts - a list of percepts
    #        numAction - the size of the actions list that needs to be returned

    def AgentFunction(self, percepts, numActions):

        actions = [0] * numActions
        for i in range(len(percepts)):
            if percepts[i] == 3:
                actions[i] = self.chrome[i]
                
            if percepts[i] == 1:
                actions[1] ==  self.chrome[i]

        #
        # Here is where the eating occurs, with red strawberries being eaten if on top of,
        # and green ones being eaten only if the probability falls in favor of it.
        if percepts[4] == 2:
            actions[9] = self.chrome[9]
        if percepts[4] == 1:
            randProb = random.uniform(0,1)
            if randProb > 0.7:
                actions[9] == self.chrome[9]

        #
        # Monster Avoidance, one position of monster
        #    
        #if monster is botom left, move to top right
        if percepts[0] == 1:
            actions[8] = self.chrome[8]
        #if monster is botom middle, move to top middle
        if percepts[1] == 1:
            actions[7] = self.chrome[7]
        #if monster is botom right, move to top left
        if percepts[2] == 1:
            actions[6] = self.chrome[6]
        #if monster is middle left, move to middle right
        if percepts[3] == 1:
            actions[5] = self.chrome[5]
        #if monster is middle right, move to middle left
        if percepts[5] == 1:
            actions[3] = self.chrome[3]

        #
        # Monster Avoidance, two positions of monster
        #    
        if percepts[0] == 1 and percepts[1] == 1:
            actions[8] = self.chrome[8]
        
        if percepts[1] == 1 and percepts[2] == 1:
            actions[6] = self.chrome[6]
      
        if percepts[2] == 1 and percepts[3] == 1:
            actions[8] = self.chrome[8]

        if percepts[2] == 1 and percepts[5] == 1:
            actions[6] = self.chrome[6]

        if percepts[3] == 1 and percepts[6] == 1:
            actions[2] = self.chrome[2]

        if percepts[5] == 1 and percepts[5] == 1:
            actions[0] = self.chrome[0]

        if percepts[6] == 1 and percepts[7] == 1:
            actions[2] = self.chrome[2]

        if percepts[7] == 1 and percepts[8] == 1:
            actions[0] = self.chrome[0]

        if percepts[6] == 1 and percepts[8] == 1:
            actions[1] = self.chrome[1]

        if percepts[0] == 1 and percepts[2] == 1:
            actions[7] = self.chrome[7]

        if percepts[6] == 1 and percepts[0] == 1:
            actions[5] = self.chrome[5]

        if percepts[8] == 1 and percepts[2] == 1:
            actions[3] = self.chrome[3]

        if percepts[7] == 1 and percepts[3] == 1:
            actions[2] = self.chrome[2]

        if percepts[1] == 1 and percepts[5] == 1:
            actions[6] = self.chrome[6]

        return actions

# This function is called after every simulation, passing a list of the old population of creatures, whose fitness
# you need to evaluate and whose chromosomes you can use to create new creatures.
#
# Input: Creatures energy - current energy of the creature. If it is dead, do nothing to the 
#                           creatures energy. If it isn't dead, give it a heavy fitness weight
#        Creatures status - Takes in the health status of the creature to see if it is alive or dead 
#
# Returns: a fitness value for MyCreature.


def fitnessCalc(energy, dead):
    fitness = 0
    if not dead:
        fitness += 500
    return fitness 

# This function is called after every simulation, passing a list of the old population of creatures, whose fitness
# you need to evaluate and whose chromosomes you can use to create new creatures.
#
# Input: old_population - list of objects of MyCreature type that participated in the last simulation.  You
#                         can query the state of the creatures by using some built-in methods as well as any methods
#                         you decide to add to MyCreature class.  The length of the list is the size of
#                         the population.  You need to generate a new population of the same size.  Creatures from
#                         old population can be used in the new population - simulation will reset them to their
#                         starting state (not dead, new health, etc.).
#
# Returns: a list of MyCreature objects of the same length as the old_population, but with new creatures based on old_pop survivors.

def newPopulation(old_population):
    global numTurns
    global totalAvgSurvivalRate



    nSurvivors = 0
    avgLifeTime = 0
    fitnessScore = 0
    survivalRate = 0

    fitnessList = []

    # For each individual you can extract the following information left over
    # from the evaluation.  This will allow you to figure out how well an individual did in the
    # simulation of the world: whether the creature is dead or not, how much
    # energy did the creature have a the end of simulation (0 if dead), the tick number
    # indicating the time of creature's death (if dead).  You should use this information to build
    # a fitness function that scores how the individual did in the simulation.

    # 2D list used for gaining access to the creatures to eventually select a portion of them randomly
    # and perform a tournament on them to select two parents
    popMyList = [[0 for i in range(2)] for j in range(len(old_population))]
    for index, individual in enumerate(old_population):


        # You can read the creature's energy at the end of the simulation - it will be 0 if creature is dead.
        energy = individual.getEnergy()

        # This method tells you if the creature died during the simulation
        dead = individual.isDead()
        fitness = fitnessCalc(energy, dead)
        # creatureFitnessTable(creature, fitness)
        fitnessScore += fitness
        #fitnessList = fitnessList.append({fitness, individual.chrome}) #individual adding its fitness and chrome to a list

        # If the creature is dead, you can get its time of death (in units of turns)
        if dead:
            timeOfDeath = individual.timeOfDeath()
            avgLifeTime += timeOfDeath
        else:
            nSurvivors += 1
            avgLifeTime += numTurns

        # Adding the creatures fitness to the 2D list
        popMyList[index][0] = fitness
        # Adding the creatures index to the 2D list
        popMyList[index][1] = index

    # Calculating the survival rate of the generation
    survivalRate = ((nSurvivors / len(population)*100))

    # Appending the survivalRate variable to an array to print out
    averageArray.append(survivalRate)
    # Creating an average of each 100 of averages and adding them to a list
    if len(averageArray) % 100 == 0:
        avgSum = (sum(averageArray) / (len(averageArray)))
        
        graph1.append(avgSum)


    totalAvgSurvivalRate += survivalRate
    
    # Here are some statistics, which you may or may not find useful
    avgLifeTime = float(avgLifeTime)/float(len(population))
    avgFitness = float(fitnessScore)/float(len(population))

    graph.append(nSurvivors)

    print("Simulation stats:")
    print("Survival rate for this gen: " + str(survivalRate) + "%")
    print("  Survivors    : %d out of %d" % (nSurvivors, len(population)))
    info.append(nSurvivors)
    life.append(avgLifeTime)
    print("  Avg life time: %.1f turns" % avgLifeTime)

    # The information gathered above should allow you to build a fitness function that evaluates fitness of
    # every creature.  You should show the average fitness, but also use the fitness for selecting parents and
    # spawning then new creatures.



    # Based on the fitness you should select individuals for reproduction and create a
    # new population.  At the moment this is not done, and the same population with the same number
    # of individuals is returned for the next generation.

    new_population = []

    # Loop used to create 34 new creatures based on parent chromosomes
    for i in range(0,34):
        # subsection list to store the 5 random choices from the 2D population list above
        subsection = []

        # Adding a random creature to the subsection list 5 times
        for j in range(5):
            subsection.append(random.choice(popMyList))

        # Sorting the list
        subsection.sort()

        # Getting one of the two best from the sorted subsection list
        parent = old_population[subsection[4][1]]

        # Getting the other of the two best from the sorted subsection list
        parent1 = old_population[subsection[3][1]]

        # Assigning the child chromosome to one parent chromosome
        chromosomeChild = parent.chrome

        # Generates an int which decides where to split the current child chromosome to merge with the other parent chrome
        crossoverPoint = np.random.randint(0, 10)

        # From 0 - crossoverPoint, assign the other parents chromosomes to the child chromosome
        for k in range(0, crossoverPoint):
            chromosomeChild[k] = parent1.chrome[k]
        # Create a new child 
        child = MyCreature(numCreaturePercepts, numCreatureActions, chromosomeChild)
        # Add it to the future population list 
        new_population.append(child)
    #return the new population list
    return new_population



# Pygame window sometime doesn't spawn unless Matplotlib figure is not created, so best to keep the following two
# calls here.  You might also want to use matplotlib for plotting average fitness over generations.
plt.close('all')
fh=plt.figure()

# Create the world.  The worldType specifies the type of world to use (there are two types to chose from);
# gridSize specifies the size of the world, repeatable parameter allows you to run the simulation in exactly same way.
w = World(worldType=worldType, gridSize=gridSize, repeatable=repeatableMode)

#Get the number of creatures in the world
numCreatures = w.maxNumCreatures()

#Get the number of creature percepts
numCreaturePercepts = w.numCreaturePercepts()

#Get the number of creature actions
numCreatureActions = w.numCreatureActions()

# Create a list of initial creatures - instantiations of the MyCreature class that you implemented
population = list()
for i in range(numCreatures):
   c = MyCreature(numCreaturePercepts, numCreatureActions)
   population.append(c)

# Pass the first population to the world simulator
w.setNextGeneration(population)

# Runs the simulation to evaluate the first population
w.evaluate(numTurns)

# Show the visualisation of the initial creature behaviour (you can change the speed of the animation to 'slow',
# 'normal' or 'fast')
w.show_simulation(titleStr='Initial population', speed='fast')

for i in range(numGenerations):
    print("\nGeneration %d:" % (i+1))

    # Create a new population from the old one
    population = newPopulation(population)

    # Pass the new population to the world simulator
    w.setNextGeneration(population)

    # Run the simulation again to evaluate the next population
    w.evaluate(numTurns)

    # Show the visualisation of the final generation (you can change the speed of the animation to 'slow', 'normal' or
    # 'fast')
    if i==numGenerations-1:
        w.show_simulation(titleStr='Final population', speed='fast')




print("\n---------------------------------------------")
print("Average survival rate over " + str(numGenerations) + " generations: " + str(totalAvgSurvivalRate/numGenerations)+"%")
print("---------------------------------------------\n")


