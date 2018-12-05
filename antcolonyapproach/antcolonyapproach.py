import time
import math
import random

class antapproach(object):
    def __init__(self,input, n=15, iteration=3500, a = 1, b = 1 , r = 0.9, q = 0.5, s = 2):
        self.input=input
        self.n = n # number of ants
        self.iteration = iteration
        self.a = a # parameter alpha; See definition of parameters at https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms#Convergence
        self.b = b # Parameter beta
        self.r = r # pheromone evaporation coefficient 
        self.q = q # it's a constant
        self.s = s # Update strategy
        
    def algo(self):
        start_time = time.time() # Start clock
        
        dataset = self.input
        for i in range(len(dataset)):
            for j in range(len(dataset)):
                if dataset[i][j] == 0 or dataset[i][j]==-1:
                    dataset[i][j] = math.inf
                    
                    
        l = len(dataset)
        nodes = combine(dataset, l)
        parameters = antcolony(self.n, self.iteration, self.a, self.b, self.r, self.q, self.s)
        dist, OptimalTour = parameters.ant(nodes)
        OptimalTour = [x+1 for x in OptimalTour]
        
        OptimalTour = list(OptimalTour)
        
        if OptimalTour[0] != 1:
            for i in list(range(0,l)):
                if OptimalTour[i] == 1:
                    j = i
            List1 = OptimalTour[0:j]
            List2 = OptimalTour[j:l]
            OptimalTour = List2 + List1
        
        OptimalTour.append(1)

        
        end_time = time.time() # End clock
        return OptimalTour, dist, (end_time-start_time)  
        
class combine(object):
    def __init__(self,dataset,l):
        self.dataset = dataset
        self.l = l # Number of nodes
        self.pheromone = [[1/(l*l) for j in range(l)] for i in range(l)]
  
class antcolony(object):
    def __init__(self,n,iteration,a,b,r,q,s):
        self.n = n # number of ants
        self.iteration = iteration
        self.a = a # parameter alpha; See definition of parameters at https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms#Convergence
        self.b = b # Parameter beta
        self.r = r # pheromone evaporation coefficient 
        self.q = q # it's a constant
        self.s = s # Update strategy
    
    def pheromoneupdate(self, nodes, run):
        for i, row in enumerate(nodes.pheromone):
            for j, col in enumerate(row):
                nodes.pheromone[i][j] = nodes.pheromone[i][j]*self.r
                for ant in run:
                    nodes.pheromone[i][j] = nodes.pheromone[i][j] + ant.updateself[i][j]

    
    def ant(self, nodes):
        # Set optimal tour to be infinite 
        mindist = math.inf
        # Create an empty list for optimal tour
        OptimalTour = []
        for iteration in range(self.iteration):
            run = [selection(self, nodes) for i in range(self.n)]
            for ant in run:
                for i in range(nodes.l-1):
                    ant.nextvisit()
                ant.distance = ant.distance + nodes.dataset[ant.tour[-1]][ant.tour[0]]
                if ant.distance < mindist:
                    mindist = ant.distance
                    OptimalTour = [] + ant.tour
                ant.updateit() # Local update of pheromone
            self.pheromoneupdate(nodes, run)
        return mindist, OptimalTour
                               
class selection(object):
    def __init__(self, parameters, nodes):
        self.colony = parameters
        self.nodes = nodes
        self.distance=0
        self.tour = [] # Tour yet
        self.update = [] # Local update of pheromone
        self.next = [i for i in range(nodes.l)] # next possible visits
        # probability to visit a node
        self.prob = [[0 if i==j else 1/float(nodes.dataset[i][j]) for j in range(nodes.l)] for i in range(nodes.l)]
        # Select first node between 0 and (l-1) randomly
        first = random.randint(0,(nodes.l-1)) 
        # first = 0 # It did not work by changing first city to 0. I shall later update this.
        self.tour.append(first) # Add start to the tour
        self.current = first # Current node
        self.next.remove(first) # Remove start from the next possible visits
               
    def nextvisit(self):
        p = [0 for i in range(self.nodes.l)]  # probabilities for moving to a node in the next step
        sum = 0
        for i in self.next:
            sum = sum + self.nodes.pheromone[self.current][i]**self.colony.a * self.prob[self.current][i]**self.colony.b
        for i in range(self.nodes.l):
            if i in self.next:
                if self.nodes.dataset[self.current][i] != math.inf:
                    try:
                        p[i] = (self.nodes.pheromone[self.current][i]**self.colony.a * self.prob[self.current][i]**self.colony.b) /(sum)               
                    except ZeroDivisionError:
                        pass            # To avoid division by zero since sum is originally 0
        # select next node
        select = 0
        randomvalue = random.random() # Select a random value between 0 and 1
        for i, d in enumerate(p):
            randomvalue = randomvalue - d
            if randomvalue <= 0:
                select = i
                break
        
        try:
            self.next.remove(select) # To avoid ValueError
        except ValueError:
            pass
            
        self.tour.append(select) 
        self.distance = self.distance + self.nodes.dataset[self.current][select]
        self.current = select
        
    def updateit(self):
        self.updateself = [[0 for j in range(self.nodes.l)] for i in range(self.nodes.l)]
        for k in range(1, len(self.tour)):
            i = self.tour[k - 1]
            j = self.tour[k]
            if self.colony.s == 1:
                self.updateself[i][j] = self.colony.q
            elif self.colony.s == 2:
                self.updateself[i][j] = self.colony.q / self.nodes.dataset[i][j]
            else:  # ant-cycle system
                self.updateself[i][j] = self.colony.q / self.distance
