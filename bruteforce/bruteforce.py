from os import path
import numpy
import math
import itertools as it
import time

class brute(object):
    def __init__(self, filename):
        self.name = filename

    def algo(self):
        start_time = time.time() # Start clock
        file = path.join(self.name)
        dataset = numpy.loadtxt(file)
        dataset[dataset == 0] = math.inf
        # number of nodes
        l = numpy.ma.size(dataset,1)
        # Calculate permutations to get total possible tours
        perm = list(range(1,(l+1)))
        perm = list(it.permutations(perm))
        distance = [0]*len(perm)
        # Set optimal distance to be infinite
        mindist = math.inf    
        # Create an empty list for optimal tour
        OptimalTour = []
        # Run over every possible tour
        for selection in perm:
            # start from index 0 
            start = 0
            distance = 0
            i = 0
            while i < l-1:
                new = selection[i]-1
                # Update distance
                distance = distance + dataset[start, new]
                start = new
                i += 1
            # Set next node to be visited to first index of a tour
            new = 0
            # Update distance
            distance = distance + dataset[start, new]
            # Update minimum distance
            if distance < mindist:
                mindist = distance
                OptimalTour = selection
            end_time = time.time() # End clock
        print("Optimal Tour:", OptimalTour, ", Optimal Cost:", int(mindist), ", time taken:", (end_time-start_time))    
