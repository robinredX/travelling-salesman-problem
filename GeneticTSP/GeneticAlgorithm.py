import math
import random
import numpy as np
import time
          
CHROMOSOME_LENGTH = 0
DISTANCES = []

POPULATION_SIZE = 10
GENERATION_NUM = 10

class Gene:
   def __init__(self, geneName = None, id = 0):
      self.geneName = geneName
      self.geneId = id

   def getGeneName(self):
      return self.geneName
 
   def getGeneId(self):
      return self.geneId    

   
   def __repr__(self):
      name = self.getGeneName()
      id = self.getGeneId() + 1
      return name


class Individual:
    def __init__(self, genes =[]):
        self.chromosomeGenes = genes
        self.fitness = 0
        print("const, len: ",len(self.chromosomeGenes))
        if len(self.chromosomeGenes) == 0  :
            for i in range (0, CHROMOSOME_LENGTH):
                self.chromosomeGenes.append(None)

    def __len__(self):
        return len(self.chromosomeGenes)

    def __repr__(self):
        geneString=""
        for i in range(0, len(self.chromosomeGenes)):
            geneString += str(self.chromosomeGenes[i]) + "->"
        return geneString

    def __getitem__(self, index):
      return self.chromosomeGenes[index]
   
    def __setitem__(self, key, value):
      self.chromosomeGenes[key] = value

    def setGeneAtIndex(self, gene , index):
        self.chromosomeGenes[index] = gene

    def getGeneAtIndex(self, index):
        return self.chromosomeGenes[index]

    def getChromosomeLength(self):
        return len(self.chromosomeGenes)

    def getFitness(self):
        initialFitness = 0
        for i in range (0, CHROMOSOME_LENGTH):
            if i == CHROMOSOME_LENGTH -1:
                break
            else:
                firstGene = self.chromosomeGenes[i]
                seconGene = self.chromosomeGenes[i+1]
                initialFitness += DISTANCES[firstGene.getGeneId()] [seconGene.getGeneId()]
        # print 
        initialFitness += DISTANCES[self.chromosomeGenes[-1].getGeneId()] [self.chromosomeGenes[0].getGeneId()]

        return initialFitness


class Population:
    def __init__(self, individuals =[], populationSize = 10):
        self.individuals = individuals
        self.populationSize = populationSize
        if len(self.individuals) == POPULATION_SIZE:
            return
        for i in range(0, populationSize):
            print(i)
            self.individuals.append(None)


    def getFittest(self):
        fittest = self.individuals[0]
        # print("first: ", fittest.getFitness)
        for i in range(0, self.populationSize):
            if fittest.getFitness() > self.individuals[i].getFitness():
                fittest = self.individuals[i]
        return fittest

    def getFitness(self):
        fitness = 0
        for i in range(0, len(self.individuals)):   
            ithIndividual = self.individuals[i]
            if(ithIndividual is not None):
                fitness += ithIndividual.getFitness()
        return fitness
    def getIndividualAtIndex(self, index):
        return self.individuals[index]


    def setIndividualAtIndex(self, individual, index = None):
        if index is None:
            self.individuals.append(individual)
        else:
            self.individuals[index] = individual



class Universe:
    def __init__(self, mutationRate = 0.5, elitism = True):
        self.mutationRate = mutationRate
        self.elitism = elitism
    
    def crossover(self, father, mother, mid = None):
        child = Individual(genes = [])
        midIndex = int(random.random() * father.getChromosomeLength())
        if mid is not None:
            midIndex = mid
        print("mid: ", midIndex)
        print("father: ", father)
        print("mother: ", mother)

        addedGenes = []
        print("initial: ", child)
        for i in range(0, midIndex):
            # print("from Father: ", i)
            child.setGeneAtIndex(father.getGeneAtIndex(i), i )
            addedGenes.append(father.getGeneAtIndex(i).getGeneId())
        print("child from father: ", child)

        if len(addedGenes) == CHROMOSOME_LENGTH:
            print("final child all from father ", child)
            return child

        index = 0
        for i in range(0, mother.getChromosomeLength()):
            candidate = mother.getGeneAtIndex(i)
            if candidate.getGeneId() not in  addedGenes:
                child.setGeneAtIndex(candidate, midIndex + index )
                addedGenes.append(candidate.getGeneId())
                index = index + 1


        child = self.mutate(child)
        print("final child: ", child)
        return child

    def mutate(self, individual):
        for i in range(0, individual.getChromosomeLength()):
            if random.random() < self.mutationRate:
                j = int(individual.getChromosomeLength() * random.random())

                firstMutatedGene = individual.getGeneAtIndex(i)
                secondMutatedGene = individual.getGeneAtIndex(j)
                individual.setGeneAtIndex(firstMutatedGene, j)
                individual.setGeneAtIndex(secondMutatedGene, i)
        return individual

    
    def rouletteSelction (self,  currentPoplulation, elitedIndividuals = [] ):

        universalFitness = currentPoplulation.getFitness()
        selectedIndividualForNexGeneration = currentPoplulation.getFittest()
        currentProportionalProbability = 0
        spinRouletteProbability = random.random()
        for i in range (0, currentPoplulation.populationSize):
            ithIndividual = currentPoplulation.getIndividualAtIndex(i)
            currentProportionalProbability += ithIndividual.getFitness() / universalFitness
            if (currentProportionalProbability > spinRouletteProbability):
                selectedIndividualForNexGeneration = ithIndividual
                break

        return selectedIndividualForNexGeneration



    def selection(self, currentPoplulation , type = "ROULETTE_WHEEL", elitedIndividuals = [] ):
        # print("currentPoplulation: " , currentPoplulation)
        return self.rouletteSelction(currentPoplulation = currentPoplulation, elitedIndividuals = [])

    def breed(self, currentPoplulation):
        nexGeneration = Population(populationSize = currentPoplulation.populationSize)
        elitedIndividual = currentPoplulation.getFittest()
        elitedIndividuals = [elitedIndividual]
        nexGeneration.setIndividualAtIndex(elitedIndividual, 0)
        nextGenerationSize = 1
        while nextGenerationSize < currentPoplulation.populationSize:
            fatherToMate = self.selection(currentPoplulation, elitedIndividuals)
            motherToMate = self.selection(currentPoplulation, elitedIndividuals)

            # print("current Pop: ", currentPoplulation.individuals)
            print("fatherToMate: ", fatherToMate)
            print("motherToMate: ", motherToMate)
            child = self.crossover(fatherToMate, motherToMate)
            # print("child: ", child)
            nexGeneration.setIndividualAtIndex(child, nextGenerationSize)
            nextGenerationSize += 1

        return nexGeneration



class Genetic:
    def __init__(self, matrix):
        """
        Takes cost matrix as a list and starts journey from 1st node.
        """
        self.matrix = matrix


    def main(self):
        start_time = time.time()
        cities =[]
        global DISTANCES
        global CHROMOSOME_LENGTH
        DISTANCES = self.matrix
        CHROMOSOME_LENGTH = len(self.matrix)
        self.matrix = np.array(self.matrix)
        for i in range (0, self.matrix.shape[0]):
            city = Gene(str(i + 1), i)
            cities.append(city)
        print(cities)
        tour1 = Individual(cities)
        initialPopulation = [tour1]
        for i in range(1, POPULATION_SIZE):
            newTour = Individual(cities.copy())
            random.shuffle(newTour)
            initialPopulation.append(newTour)

        print(initialPopulation)

        pop = Population(initialPopulation, POPULATION_SIZE)
        univ = Universe()
        for i in range(0,GENERATION_NUM):
            print("Pop: ,", pop.individuals)
            pop = univ.breed(pop)

        fittest = pop.getFittest()
        return fittest.getFitness(), fittest, time.time() - start_time
        #print("Fittest is : ", fittest, " , With Fitness: ", fittest.getFitness())


#main()
