import networkx as nx
import heapq


def create_distance_graph(edges):
    G = nx.Graph()

    for edge in edges:
        x, y, distance = edge
        G.add_edge(x, y, weight=distance)

    return G


def grid_to_graph(rows, cols):
    G = nx.Graph()
    # Add nodes to the graph
    for i in range(rows):
        for j in range(cols):
            G.add_node((i, j))

    # Add edges to the graph for up, down, right, and left movements
    for i in range(rows):
        for j in range(cols):
            # Connect up
            if i > 0:
                G.add_edge((i, j), (i - 1, j))
            # Connect down
            if i < rows - 1:
                G.add_edge((i, j), (i + 1, j))
            # Connect left
            if j > 0:
                G.add_edge((i, j), (i, j - 1))
            # Connect right
            if j < cols - 1:
                G.add_edge((i, j), (i, j + 1))

    return G


def dijkstra(graph, start, end):
    priority_queue = [(0, start)]  # (distance, node)
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor in graph[current_node]:
            distance = current_distance + 1  # Assuming unit weights for edges

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current = end

    while current is not None:
        path.insert(0, current)
        current = min((neighbor for neighbor in graph[current] if distances[neighbor] == distances[current] - 1), default=None)

    return path

class DisjointSet:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y
                self.rank[root_y] += 1

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]


def kruskal(graph):
    edges = []
    nodes = set()
    for node in graph:
        nodes.add(node)
        for neighbor, weight in graph[node].items():
            nodes.add(neighbor)
            edges.append((node, neighbor, weight['weight']))
    edges = sorted(edges, key=lambda item: item[2]) # Sort edges by weight

    mst_edges = []
    disjoint_set = DisjointSet(nodes)

    for edge in edges:
        x, y, weight = edge
        if disjoint_set.find(x) != disjoint_set.find(y):
            mst_edges.append(edge)
            disjoint_set.union(x, y)

    return mst_edges