import math
import time


class GreedyTsp( object ):
    def __init__(self, matrix):
        self.matrix = matrix

    def greedy_tsp(self):
        start_time = time.time()
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

        total_cost += self.matrix[tour[-1]][0] if self.matrix[tour[-1]][0] < math.inf else 0
        tour.append(0)
        end_time = time.time()
        return total_cost, tour, (end_time-start_time)


    def run_time_limit_iteration(self, time_limit, start_node):
        elapse_time = 0
        start_time=time.time()
        min_cost = float("inf")
        opt_path=[]
        while (time.time()-start_time)<time_limit:
            cost, path, time_elapse = self.greedy_tsp()
            if cost<min_cost:
                min_cost = cost
                opt_path = path

        end_time = time.time()
        return min_cost, opt_path, (end_time-start_time)


if __name__ == '__main__':
    # Run Example

    import Parser

    # f = open('test_files/asymmetric/ft53.atsp', 'r')
    # parser = Parser.Parser()
    # matrix = parser.parse_file(f)


    inf = math.inf
    matrix = [
         [inf,   0,  10, 19,  123],
         [12,  inf,  4,  123, 23],
         [10,  3,  inf,  6,   20],
         [2,   20, 6,  inf,   4],
         [789, 2,  20, 4,   inf]
     ]


    g = GreedyTsp(matrix)
    start_time = time.time()
    cost, tour, runtime = g.greedy_tsp()

    print("--- %s milliseconds ---" % ((time.time() - start_time)*1000))
    print(tour)
    print(cost)
