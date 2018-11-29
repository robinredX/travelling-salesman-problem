import math

class Greedy:

    def __init__(self, matrix):
        self.matrix = matrix

    def greedy_tsp(self):
        tour = [0]
        total_cost = 0

        visited_nodes = [(0, 0)]
        row = self.matrix[0]

        while len(visited_nodes) < len(self.matrix):

            for node in visited_nodes:
                row[node[0]] = math.inf


            min_weight = min([x for x in row if x > 0])

            visit = row.index(min_weight), min_weight
            visited_nodes.append(visit)

            tour.append(visit[0])
            total_cost += visit[1]

            row = self.matrix[visit[0]]

        return tour, total_cost


# Run Example

# import Parser
# import time
#
# f = open('test_files/asymmetric/ft53.atsp', 'r')
# parser = Parser.Parser()
# matrix = parser.parse_file(f)


# inf = math.inf
# matrix = [
#     [inf,   0,  10, 19,  123],
#     [12,  inf,  4,  123, 23],
#     [10,  3,  inf,  6,   20],
#     [2,   20, 6,  inf,   4],
#     [789, 2,  20, 4,   inf]
# ]


# g = Greedy(matrix)
# start_time = time.time()
# tour, cost = g.greedy_tsp()
#
# print("--- %s milliseconds ---" % ((time.time() - start_time)*1000))
#
# print(tour)
# print(cost)
