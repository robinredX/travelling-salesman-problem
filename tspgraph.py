import networkx as nx
import matplotlib.pyplot as plt
from Generator import Generator
import math

class TSPGraphViewer:

    def draw_graph_from_adj_matrix(matrix):

        # create networkx graph
        G=nx.Graph()

        row_pos = 0
        # add edges
        for row in matrix:
            col_pos = 0
            for col in row:
                if (col != math.inf and col != -1):
                    G.add_edge(row_pos + 1, col_pos + 1, label=col)
                col_pos +=1
            row_pos +=1

        # set layout and other settings
        graph_pos=nx.shell_layout(G)
        node_size=1000

        # draw graph
        nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=0.3, node_color='green')
        nx.draw_networkx_edges(G,graph_pos,width=1,alpha=0.3,edge_color='blue')
        nx.draw_networkx_labels(G, graph_pos,font_size=12, font_family='sans-serif')

        nx.draw_networkx_edge_labels(G, graph_pos, edge_labels={(u, v): d["label"] for u, v, d in G.edges(data=True)},
                                     label_pos=0.3)

        # show graph
        plt.axis("off")
        plt.show()

    generator = Generator()
    matrix = generator.generate(5, 5, 2, 15, True)

    # if edge labels is not specified, numeric labels (0, 1, 2...) will be used
    draw_graph_from_adj_matrix(matrix)
