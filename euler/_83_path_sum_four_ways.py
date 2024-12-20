import argparse

from custom.dijkstra import dijkstra
from custom.graph import Graph

parser = argparse.ArgumentParser(description='Find the shortest path \
    from top-left to bottom right in the representation of the grid \
    passed in with the text file.')
parser.add_argument('file', help='the file passed in')
args = parser.parse_args()

g = Graph()

grid = []
with open(args.file) as f:
    for line in f.readlines():
        row = str.strip(line).split(',')
        grid.append(list(map(int, row)))

for r in range(len(grid)):
    row = grid[r]
    for c in range(len(row)):
        weight = grid[r][c]
        if r > 0:
            g.add_edge((r, c), (r-1, c), weight)
        if r < len(grid) - 1:
            g.add_edge((r, c), (r+1, c), weight)
        if c > 0:
            g.add_edge((r, c), (r, c-1), weight)
        if c < len(row) - 1:
            g.add_edge((r, c), (r, c+1), weight)

dist = dijkstra(g, g.get_vertex((0,0)))['dist']
for vertex, distance in dist.items():
    print(vertex, distance + grid[-1][-1])

