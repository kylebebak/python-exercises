"""
Client of EdgeWeightedGraph and KruskalMST, which in turn uses the
UF (union find) data structure. Finds the maximum reduction in edge
weight obtained by removing edges from a graph such that the
remaining edges still span the graph.

The graph is parsed from an input file passed to this script via a
positional argument.
"""

import sys, time

from custom.graph_edge import Edge, EdgeWeightedGraph
from custom.mst import KruskalMST

start_time = time.time()
with open(sys.argv[1]) as f:
    # read through file to determine number of vertices in graph
    g = EdgeWeightedGraph(len(f.readlines()))
with open(sys.argv[1]) as f:
    # build graph from file
    for i, line in enumerate(f):
        weights = line.strip().split(',')
        for j, weight in enumerate(weights):
            if j >= i and weight != '-':
                g.add_edge(Edge(i, j, int(weight)))

# build MST, and find reduction in total edge weight
# as compared with original graph
mst = KruskalMST(g)
reduction = 0
for e in g.edges():
    if e not in mst.edges():
        reduction += e.get_weight()

print(reduction)
print('Duration: {0}s'.format(time.time() - start_time))
