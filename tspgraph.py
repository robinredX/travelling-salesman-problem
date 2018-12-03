import networkx as nx
import matplotlib.pyplot as plt
from Generator import Generator
import math

class TSPGraphViewer:

    def draw_graph_from_adj_matrix(matrix):

        # create networkx graph
        G=nx.Graph()

        row_pos = 0
        # add edges from adj matrix
        for row in matrix:
            col_pos = 0
            for col in row:
                if (col != math.inf and col != -1):
                    G.add_edge(row_pos + 1, col_pos + 1, label=col)
                col_pos +=1
            row_pos +=1

        # set layout and other settings
        graph_pos=nx.shell_layout(G)
        node_size = 1000
        font_size = 12
        node_colour = 'green'
        vertex_count = len(matrix)
        if vertex_count > 10:
            node_size =500
            font_size = 8

        if vertex_count >= 30:
            graph_pos=nx.random_layout(G)
            node_size =250

        if vertex_count >=50:
            node_size =50
            node_colour = 'black'

        # draw graph
        nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=0.5, node_color=node_colour)
        nx.draw_networkx_edges(G,graph_pos,width=1,alpha=0.5,edge_color='blue')
        if vertex_count < 70:
            nx.draw_networkx_labels(G, graph_pos,font_size=font_size, font_family='sans-serif')

        if vertex_count <= 10:
            nx.draw_networkx_edge_labels(G, graph_pos, edge_labels={(u, v): d["label"] for u, v, d in G.edges(data=True)},
                                     label_pos=0.4, font_size=8)

        # show graph
        plt.axis("off")
        plt.show()

    generator = Generator()
    matrix = generator.generate(100, 5, 2, 15, True)

    draw_graph_from_adj_matrix(matrix)
