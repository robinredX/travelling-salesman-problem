""" 
Brute Force Algorithm
{Robin Khatri, MLDM M1}
"""
import math
import itertools as it
import time


class Brute:
    def __init__(self, input, startnode = 0):
        """
        Takes cost matrix as a list and starts journey from 1st node.
        """
        self.input = input
        self.startnode = startnode
        
    def algo(self):
        start_time = time.time() # Start clock
        dataset = self.input        
        l = len(dataset) # number of nodes
        for i in list(range(0,1)):
            for j in list(range(0,l)):
                if dataset[i][j] == 0 :
                    dataset[i][j] == math.inf # Replaces 0 cost with infinity so as not to select incase of assymetric travelling salesman problem
        
        perm = list(range(1,(l+1)))
        perm = list(it.permutations(perm)) # Permutations
        distance = [0]*len(perm) # Initial distance
        mindist = math.inf # Initial optimal distance is infinity
        OptimalTour = [] # List to store optimal tour
        for selection in perm:
            # start from index 0 
            start = 0
            distance = 0
            i = 0
            while i < l-1:
                new = selection[i]-1
                # Update distance
                distance = distance + dataset[start][new]
                start = new
                i += 1
                
            # Set next node to be visited to first index of a tour
            new = 0
            
            # Update distance
            
            distance = distance + dataset[start][new]
            # Update minimum distance
            if distance < mindist:
                mindist = distance
                OptimalTour = selection
            """ 
            OptimalTour Start with node startnode
            """
            for i in list(range(0,l)):
                if i == 0:
                    j == i
                    
            list1 = OptimalTour[0:(j-1)]
            list2 = OptimalTour[(j-1):(l-1)]
            OptimalTour = list1 + list2
            end_time = time.time()

        return int(mindist), OptimalTour, end_time - start_time
        #print("Optimal Tour:", OptimalTour, ", Optimal Cost:", int(mindist), ", time taken:", (end_time-start_time))
        
#if __name__ == "__main__":
    #matrix = [[0,10,0,20,4],[5,0,9,0,2],[6,0,0,12,43],[8,8,9,0,22],[2,2,250,2,0]]
    start_time = time.time() # Start clock
    #result = Brute(matrix)
    #result.algo()
