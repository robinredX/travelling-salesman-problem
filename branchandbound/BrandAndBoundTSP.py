import numpy
import math
import copy
from node import TreeNode

vertex_count = 6
start_vertex = 1
upper_bound = math.inf

graph = {'1': [{'2':'15'}, {'4':'7'}, {'5':'10'}],
    '2': [{'3':'9'}, {'4':'11'}, {'6':'9'}],
    '3': [{'5':'12'}, {'6':'7'}],
    '4': [{'5':'8'}, {'6':'14'}],
    '5': [{'6':'8'}]}

def weighted_adjmatrix(adjlist, nodes):
    '''Returns a (weighted) adjacency matrix as a NumPy array.'''
    matrix = []
    for node in nodes:
        weights = {endnode:float(weight)
                   for w in adjlist.get(node, {})
                   for endnode, weight in w.items()}
        matrix.append([weights.get(endnode, 0) for endnode in nodes])
    matrix = numpy.array(matrix)
    return matrix + matrix.transpose()

def calculate_reduction(matrix, vertex_from, vertex_to):
    index_from = vertex_from - 1
    index_to = vertex_to - 1
    reduction_cost = 0
    #start with matrix as it is passed in
    reduced_matrix = matrix
    #set the values to infinity for the vertices passed in
    if (vertex_from != 0 and vertex_to != 0):
        reduced_matrix[index_from, index_to] = math.inf
        #set the reverse also as we can't go back later
        reduced_matrix[index_to, index_from] = math.inf
    #row level reduction
    for i, row in enumerate(reduced_matrix, 0):
        #set the vertex from row to infinity
        if (i == index_from and vertex_from != 0):
            row[row != math.inf] = math.inf
        shortest_edge = min(row)
        if (shortest_edge == math.inf):
            shortest_edge = 0
        reduction_cost += shortest_edge
        #leave infinity alone
        row[row != math.inf] -= shortest_edge
    #col level reduction - use the transpose
    for j, col in enumerate(reduced_matrix.transpose(), 0):
        #set the vertex to col to infinity
        if (j == index_to and vertex_to != 0):
            col[col != math.inf] = math.inf
        shortest_edge = min(col)
        if (shortest_edge == math.inf):
            shortest_edge = 0
        reduction_cost += shortest_edge
        #leave infinity alone
        col[col != math.inf] -= shortest_edge
    return reduced_matrix, reduction_cost

def get_possible_edges_for_vertex(working_node):
    #out of bounds error
    matrix = working_node.reduced_matrix
    row = matrix[working_node.index_in_matrix]
    available_vertices = []
    for y in enumerate(row):
        if y[1] != math.inf:
            #remove the return to the first node option if not last node
            if (y[0] + 1 != start_vertex):
                available_vertices.append(y[0] + 1)
            elif (len(working_node.path_so_far) == vertex_count):
                available_vertices.append(y[0] + 1)
    working_node.number_of_children = len(available_vertices)
    return available_vertices

#used to find the next best un-pruned vertex
def find_lowest_cost_next_vertex(parent_node, nodes_list):
    available_vertices = get_possible_edges_for_vertex(parent_node)
    lowest_cost = math.inf
    least_cost_vertex = 0
    least_cost_node = None
    for vertex in available_vertices:
        # need to copy this every loop to prevent carry over changes
        path = copy.deepcopy(parent_node.path_so_far)
        matrix = copy.deepcopy(parent_node.reduced_matrix)
        path.append(vertex)
        # check for existing node in the list by path
        exiting_node = find_node_in_list_by_path(path, nodes_list)
        if (exiting_node != None):
            if (exiting_node.status != "pruned" and exiting_node.status != "searched"):
                tree_node = exiting_node
            else:
                #reduce the number of children of the parent node
                parent_node.number_of_children = parent_node.number_of_children - 1
                continue
        else:
            # actual cost of going between current vertices
            actual_cost = matrix[parent_node.index_in_matrix, vertex - 1]
            # reduced matrix and cost for node being calculated
            reduced_matrix, reduction_cost = calculate_reduction(matrix, parent_node.vertex_id, vertex)
            cost = reduction_cost + parent_node.cost + actual_cost
            # add node to the list since we have calculated it
            tree_node = TreeNode(len(nodes_list) + 1, vertex, reduced_matrix, cost, vertex - 1, path, parent_node.node_id, -1)
            nodes_list.append(tree_node)
        if tree_node.cost < lowest_cost:
            lowest_cost = tree_node.cost
            least_cost_vertex = tree_node.vertex_id
            least_cost_node = tree_node
    return least_cost_vertex, least_cost_node, nodes_list

# used for finding node by its parent_node_id
def find_node_in_list_by_node_id(node_id, node_list):
    for i, node in enumerate(node_list):
        if node.node_id == node_id:
            return node
    return None

#used for checking if the proposed part path has already been calculated
def find_node_in_list_by_path(path, node_list):
    for i, node in enumerate(node_list):
        if node.path_so_far == path:
            return node
    return None

#used to cascade down a path of the tree using the lowest not tested paths
def deep_dive_from_node(working_vertex_id, parent_node, tree_nodes):

    #do a deep dive to the best available leaf
    while working_vertex_id != 0:
        working_path = parent_node.path_so_far
        working_bound = parent_node.cost
        working_node = parent_node
        #if workind bound is greater than shortest path so far, prune it
        if working_bound >= upper_bound:
            working_node.status = "pruned"
            break
        working_vertex_id, parent_node, tree_nodes = find_lowest_cost_next_vertex(parent_node, tree_nodes)
    return working_path, working_bound, working_node

def branch_and_bound():
    #import the data
    data = weighted_adjmatrix(graph, nodes=list('123456'))
    #ensure all the zeros or negative values are set to inifinity,
    #zero has a special meaining for this algorithnm
    data[data == 0] = math.inf
    #set the upper bound to infinity
    upper_bound = math.inf
    #perform the initial reduction and get the lower bound
    starting_reduced_matrix, lower_bound = calculate_reduction(data, 0, 0)
    #created the first node in the state space tree
    tree_nodes = []
    working_node = TreeNode(1, 1, starting_reduced_matrix, lower_bound, 0, [1], 0, -1)
    tree_nodes.append(working_node)

    while (working_node != None):

        #do a deep dive to the first leaf
        working_path, working_bound, working_node = deep_dive_from_node(working_node.vertex_id, working_node, tree_nodes)
        print(working_path)

        #if we have a loop set the upper bound else keep looking for a loop
        if working_path[0] == working_path[-1]:
            print("Tour")
            status = "searched"
            #set upper bound to the result of the dive if lower
            if working_bound < upper_bound:
                upper_bound = working_bound
                best_path = working_path
            print("Upper bound: " , upper_bound)
            print("Best path found:", best_path)
        else:
            print("No Tour")
            status = "pruned"

        while working_node.number_of_children < 2:
            if working_node.vertex_id != start_vertex:
                working_node.status = status
                print(working_node.vertex_id)
            working_node = find_node_in_list_by_node_id(working_node.parent_node_id, tree_nodes)
            if(working_node == None):
                break

branch_and_bound()

