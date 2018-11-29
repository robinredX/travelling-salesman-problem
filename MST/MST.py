import math

class Node:

    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.children = []


    def add_child(self, node):
        self.children.append(node)


    def get_rev_children(self):
        children = self.children[:]
        children.reverse()
        return children


    def __str__(self, level=0):
        ret = "\t" * level + 'Value: ' + repr(self.value) + ', Index: ' + repr(self.index) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'



class MST:

    def __init__(self, matrix):
        self.matrix = matrix
        self.dimension = len(matrix)


    def print_mst(self, parent):
        print("Edge \tWeight")
        for i in range(1, self.dimension):
            print(parent[i], "-", i, "\t", self.matrix[parent[i]][i])


    def construct_tree(self, parents):
        root = Node(0, 0)

        for i, node in enumerate(parents):
            if root.index == node:
                child = Node(i, self.matrix[parents[i]][i])
                child = self.construct_children(child, parents)
                root.add_child(child)
        return root


    def construct_children(self, node, parents):
        for i, value in enumerate(parents):
            if node.index == value:
                child = Node(i, self.matrix[parents[i]][i])
                child = self.construct_children(child, parents)
                node.add_child(child)
        return node


    def dfs(self, tree):
        tour = [tree.index]
        if tree.children:
            for child in tree.children:
                tour.extend(self.dfs(child))

        return tour


    def tour_cost(self, tour):
        cost = 0
        print('tour len: ', len(tour))
        for i in range(1, len(tour)):
            print(self.matrix[tour[i-1]][tour[i]])
            cost += self.matrix[tour[i-1]][tour[i]]

        return cost


    def get_min_key_index(self, key_values, mst_set):
        minimum_node = None
        minimum = math.inf

        for node in range(self.dimension):
            if key_values[node] < minimum and not mst_set[node]:
                minimum = key_values[node]
                minimum_node = node

        return minimum_node


    def mst(self):
        key_values = [math.inf for i in range(self.dimension)]
        mst_set = [False for i in range(self.dimension)]
        parents = [-1 for i in range(self.dimension)]

        key_values[0] = 0

        while mst_set.count(False) > 0:
            min_key_index = self.get_min_key_index(key_values, mst_set)
            mst_set[min_key_index] = True

            cur_row = self.matrix[min_key_index]

            for node in range(self.dimension):
                if cur_row[node] > 0 and cur_row[node] != math.inf \
                        and not mst_set[node] and key_values[node] > cur_row[node]:
                    key_values[node] = cur_row[node]
                    parents[node] = min_key_index

        self.print_mst(parents)

        tree = self.construct_tree(parents)
        print(tree)
        tour = self.dfs(tree)
        tour.append(0)
        cost = self.tour_cost(tour)
        return tour, cost


# Run Example

# import time
# import Parser
#
# f = open('test_files/asymmetric/ft53.atsp', 'r')
# parser = Parser.Parser()
# matrix = parser.parse_file(f)


# inf = math.inf
# matrix = [
#     [inf,   0,  10, 19,  123],
#     [12,  inf,  4,  4, 23],
#     [10,  3,  inf,  6,   20],
#     [2,   20, 6,  inf,   4],
#     [789, 2,  20, 4,   inf]
# ]


# mst = MST(matrix)
#
# start_time = time.time()
#
# tour, cost = mst.mst()
#
# print("--- %s milliseconds ---" % ((time.time() - start_time)*1000))
# print(tour)
# print(cost)
