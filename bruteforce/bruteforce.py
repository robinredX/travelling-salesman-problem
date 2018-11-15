from os import path
import numpy
import math
import itertools as it
import time

def bruteforce(filename):
    start_time = time.time()
    file = path.join(filename)
    dataset = numpy.loadtxt(file)
    dataset[dataset == 0] = math.inf
    # number of nodes
    l = numpy.ma.size(dataset,1)
    # Calculate permutations = total possible tours
    perm = list(range(1,(l+1)))
    perm = list(it.permutations(perm))
    distance = [0]*len(perm)
    mindist = math.inf    
    OptimalTour = []
    for selection in perm:
        start = 0
        distance = 0
        i = 0
        while i < l-1:
            new = selection[i]-1
            distance = distance + dataset[start, new]
            start = new
            i += 1
        new = 0
        distance = distance + dataset[start, new]
        if distance < mindist:
            mindist = distance
            OptimalTour = selection
        end_time = time.time()
    print("Optimal Tour:", OptimalTour, ", Optimal Cost:", int(mindist), ", time taken:", (end_time-start_time))    
