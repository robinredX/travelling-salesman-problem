import numpy as np
import heapq

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

DISTANCES =[ 
                        [INFINITY,  34, 36, 37, 31, 33, 35], #1
                        [34,  INFINITY, 29, 23, 22, 25, 24], #2
                        [36, 29,  INFINITY, 17, 12, 18, 17], #3
                        [37, 23, 17,  INFINITY, 32, 30, 29], #4
                        [31, 22, 12, 32,  INFINITY, 26, 24], #5
                        [33, 25, 18, 30, 26,  INFINITY, 19], #6
                        [35, 24, 17, 29, 24,  19, INFINITY]  #7
     
                   ]

upperBound = np.inf
bestSol= []

def reduceMatrix(matrix, lowerBound):
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


def chooseSplittingEdge(matrix):
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






def includeEdge(matrix, i,j, lowerBound):

    matrix[j,i] = INFINITY
    matrix[i,:] = np.full((1,matrix.shape[1]), np.nan)
    matrix[:,j] = np.full((1,matrix.shape[0]), np.nan)



    matrix, lowerBound = reduceMatrix(matrix, lowerBound)


    return matrix, lowerBound


def excludeEdge(matrix, i, j,lowerBound):
    matrix[i,j] = INFINITY
    matrix, lowerBound = reduceMatrix(matrix, lowerBound)
    return matrix, lowerBound


def isValidSolution (matrix, solution):
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
    print(partialSolution)

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




def branchAndBound(matrix, lowerBound, solution,  depth, name = "root"):
    global upperBound
    global bestSol



    print("----------------------")
    print(name)
    print("depth: ", depth)
    print('initial lowerBound: ', lowerBound)
    print('current upperBound: ', upperBound)
    print('\nCurrentMatrix:\n ', matrix)

    if lowerBound > upperBound:
        print ("lower bound is : ",lowerBound, "and higher than the found upperBound: ",upperBound, " prunned")
        return

    if depth == matrix.shape[0] :
        if isValidSolution(matrix, solution):
            print("found solution: ")
            print(solution)
            print("cost: ", lowerBound)
            if lowerBound < upperBound:
                upperBound = lowerBound
                bestSol = solution.copy()
            return matrix
        else:
            if depth == matrix.shape[0] :
                print('no valid solution')
                return


    i,j = chooseSplittingEdge(matrix)
    print("split on: ", i+1, " ", j+1)


    includeEdgeMat,IncludeLowerBound = includeEdge(np.copy(matrix), i,j, lowerBound)
    edgeToPrint = str(i+1) + "," + str(j+1)
    edge = str(i) + "," + str(j)
    # print("include(",edgeToPrint," )", "\nCost: ", IncludeLowerBound," \nMatrix: \n",includeEdgeMat )
    print("include(",edgeToPrint," )", "\nCost: ", IncludeLowerBound)
    solution.append(edgeToPrint)
    branchAndBound(includeEdgeMat, IncludeLowerBound, solution, depth+1, name = "Solution with " + edgeToPrint)
    solution.pop()

    excludeEdgeMat,excludeLowerBound = excludeEdge(np.copy(matrix), i, j, lowerBound)
    print("exclude(",i+1," ",j+1," )",  "\nCost: ", excludeLowerBound)

    branchAndBound(excludeEdgeMat, excludeLowerBound, solution, depth+1,name = "Solution without " + edgeToPrint)

def main():
    x = np.array(DISTANCES)
    lowerBound = 0
    
    reducedMat,lowerBound = reduceMatrix(x,lowerBound)

    print(lowerBound)
    branchAndBound(reducedMat, lowerBound,[], 0)


    print("Final Solution = ", bestSol)
    print("Final Cost = ", upperBound)


    




main()