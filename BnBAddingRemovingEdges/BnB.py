import numpy as np
import heapq
import copy
import time

INFINITY = np.inf

# DISTANCES = [ 
#                [INFINITY, 3, 93, 13, 33, 9, 57],
#                [4, INFINITY, 77, 42, 21, 16, 34],
#                [45, 17, INFINITY, 36, 16, 28, 25],
#                [39, 90, 80, INFINITY, 56, 7, 91],
#                [28, 46, 88, 33, INFINITY, 25, 57],
#                [3, 88, 18, 46, 92, INFINITY, 7],
#                [44, 26, 33, 27, 84, 39, INFINITY]
#             ]

# DISTANCES = [ 
#                [INFINITY, 20, 30, 10, 11],
#                [15, INFINITY, 16, 4, 2],
#                [3, 5, INFINITY, 2, 4],
#                [19, 6, 18, INFINITY, 3],
#                [16, 4, 7, 16, INFINITY]
#             ]

class AddRemoveEdges:

    def __init__(self, matrix):
        self.matrix = matrix
        self.upperBound = np.inf
        self.bestSol = []

    def reduceMatrix(self, matrix, lowerBound):
        rows = matrix.shape[0]
        cols = matrix.shape[1]
        if(rows ==  0 or cols == 0):
            return matrix, lowerBound

        # print(matrix)
        rowsMin = np.nanmin(matrix,axis =1)
        where_are_NaNs = np.isnan(rowsMin)
        where_are_Inf = np.isinf(rowsMin)
        rowsMin[where_are_NaNs] = 0
        rowsMin[where_are_Inf] = 0
        rowsMin = rowsMin.reshape(rows,1)

        # print("rowsMin: ", rowsMin)
        matrix = matrix  - rowsMin

        colsMin = np.nanmin(matrix, axis = 0)
        where_are_NaNs = np.isnan(colsMin)
        where_are_Inf = np.isinf(colsMin)
        colsMin[where_are_NaNs] = 0
        colsMin[where_are_Inf] = 0
        colsMin = colsMin.reshape(1,cols)

        # print("cols Min : ", colsMin)

        matrix = matrix - colsMin

        lowerBound = lowerBound +  np.sum(rowsMin) + np.sum(colsMin)

        return matrix,lowerBound


    def chooseSplittingEdge(self, matrix):
        rows = matrix.shape[0]
        cols = matrix.shape[1]

        splittingCandidateRow = -1
        splittingCandidateCol = -1

        maximumLowerBound = - np.inf
        smallestInRow = np.inf
        smallestInCol = np.inf
        for i in range(0, rows):
            for j in range(0, cols):
                if matrix[i][j] == 0:
                    matrix [i][j] = -1
                    rowMinCandidates = [x for x in matrix[i,:] if ( x >= 0)]
                    colMinCandidates = [x for x in matrix[:, j] if x >= 0]
                    if rowMinCandidates != []:
                        smallestInRow = min( rowMinCandidates)
                    if colMinCandidates !=[]:
                        smallestInCol = min(colMinCandidates)
                    matrix[i][j] = 0

                    if smallestInCol + smallestInRow > maximumLowerBound:
                        maximumLowerBound = smallestInRow + smallestInCol
                        splittingCandidateCol = j
                        splittingCandidateRow = i

        # print("maximumLowerBound for splitting: ", maximumLowerBound)
        return splittingCandidateRow, splittingCandidateCol

    def includeEdge(self, matrix, i,j, lowerBound):

        matrix[j,i] = INFINITY
        matrix[i,:] = np.full((1,matrix.shape[1]), np.nan)
        matrix[:,j] = np.full((1,matrix.shape[0]), np.nan)

        matrix, lowerBound = self.reduceMatrix(matrix, lowerBound)
        return matrix, lowerBound


    def excludeEdge(self, matrix, i, j,lowerBound):
        matrix[i,j] = INFINITY
        matrix, lowerBound = self.reduceMatrix(matrix, lowerBound)
        return matrix, lowerBound

    def edges_to_node(self, solution):
        current_vertex = "1"
        node_list = []
        edges = copy.deepcopy(solution)
        while len(edges) > 0:
            for pair in edges:
                nodes = pair.split(",")
                if nodes[0] == current_vertex:
                    node_list.append(current_vertex)
                    current_vertex = nodes[1]
                    edges.remove(pair)
        node_list.append("1")
        return node_list



    def isValidSolution (self, matrix, solution):
        if len(solution) < matrix.shape[0]:
            return False

        partialSolution = np.full((1, matrix.shape[0]), -1)
        partialSolution = partialSolution[0]
        print(partialSolution)
        for edge in solution:
            source = edge.split(",")[0]
            target = edge.split(",")[1]
            source = int(source)
            target = int(target)
            source = source -1
            target = target -1
            partialSolution[source] = target
        print("Partial Solution", partialSolution)

        first = 0
        last = partialSolution[0]
        visitedNodes = np.full((1, matrix.shape[0]), False)
        visitedNodes = visitedNodes[0]
        visitedNodes [first] = True
        while first != last:
            if visitedNodes[last] == True:
                return False
            visitedNodes[last] = True
            last = partialSolution[last]
            print(last+1)

        # print(visitedNodes.tolist())
        # print(all(visitedNodes.tolist()))
        if all(visitedNodes.tolist()):
            return True

        return False

    def branchAndBound(self, matrix, lowerBound, solution,  depth, name = "root"):
        print("----------------------")
        print(name)
        print("depth: ", depth)
        print('initial lowerBound: ', lowerBound)
        print('current upperBound: ', self.upperBound)
        print('\nCurrentMatrix:\n ', matrix)

        if lowerBound > self.upperBound:
            print ("lower bound is : ",lowerBound, "and higher than the found upperBound: ",self.upperBound, " prunned")
            return

        if depth == matrix.shape[0] :
            if self.isValidSolution(matrix, solution):
                print("found solution: ")
                print(solution)
                print("cost: ", lowerBound)
                if lowerBound < self.upperBound:
                    self.upperBound = lowerBound
                    self.bestSol = solution.copy()
                return matrix
            else:
                if depth == matrix.shape[0] :
                    print('no valid solution')
                    return


        i,j = self.chooseSplittingEdge(matrix)
        print("split on: ", i+1, " ", j+1)


        includeEdgeMat,IncludeLowerBound = self.includeEdge(np.copy(matrix), i,j, lowerBound)
        edgeToPrint = str(i+1) + "," + str(j+1)
        edge = str(i) + "," + str(j)
        # print("include(",edgeToPrint," )", "\nCost: ", IncludeLowerBound," \nMatrix: \n",includeEdgeMat )
        print("include(",edgeToPrint," )", "\nCost: ", IncludeLowerBound)
        solution.append(edgeToPrint)
        self.branchAndBound(includeEdgeMat, IncludeLowerBound, solution, depth+1, name = "Solution with " + edgeToPrint)
        solution.pop()

        excludeEdgeMat,excludeLowerBound = self.excludeEdge(np.copy(matrix), i, j, lowerBound)
        print("exclude(",i+1," ",j+1," )",  "\nCost: ", excludeLowerBound)

        self.branchAndBound(excludeEdgeMat, excludeLowerBound, solution, depth+1,name = "Solution without " + edgeToPrint)

    def main(self):
        start_time = time.time()
        x = np.array(self.matrix)
        #ensure all the zeros or negative values are set to inifinity,
        #zero has a special meaining for this algorithnm
        x[x <= 0] = np.inf
        lowerBound = 0

        reducedMat,lowerBound = self.reduceMatrix(x,lowerBound)

        print(lowerBound)
        self.branchAndBound(reducedMat, lowerBound,[], 0)
        return self.upperBound, self.edges_to_node(self.bestSol), time.time() - start_time

        #print("Final Solution = ", bestSol)
        #print("Final Cost = ", upperBound)

#main()
