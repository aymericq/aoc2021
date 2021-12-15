import math
from typing import Tuple, List, Dict


class Node(object):
    def __init__(self, risk, neighbors):
        self.risk = risk
        self.neighbors = neighbors


def neighbors_for(x: int, y: int, max_x: int, max_y: int) -> List[Tuple[int, int]]:
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < max_x:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < max_y:
        neighbors.append((x, y + 1))

    return neighbors


def parse_input(lines: List[str]) -> Tuple[Dict[Tuple, Node], int, int]:
    graph = {}
    max_x, max_y = len(lines[0]) - 1, len(lines) - 1
    for y, line in enumerate(lines):
        for x, risk in enumerate(line):
            neighbors = neighbors_for(x, y, max_x, max_y)
            graph[(x, y)] = Node(risk, neighbors)
    return graph, max_x, max_y


def dijkstra(graph: Dict[Tuple[int, int], Node], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    unvisited_set = set(graph.keys())
    distances = {}
    curr_node = start
    distances[curr_node] = 0
    end_node_not_visited = True
    while end_node_not_visited:
        for neighbor in graph[curr_node].neighbors:
            if neighbor in unvisited_set:
                tentative_new_dist = distances[curr_node] + graph[neighbor].risk
                if neighbor not in distances or tentative_new_dist < distances[neighbor]:
                    distances[neighbor] = tentative_new_dist
        unvisited_set.remove(curr_node)
        if end not in unvisited_set:
            end_node_not_visited = False
        else:
            curr_node = min(filter(lambda key: key in unvisited_set, distances), key=lambda x: distances[x])

    return distances[end]


def a_star(graph: Dict[Tuple[int, int], Node], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    # Reproduced from wikipedia's pseudocode
    h = lambda x: (end[0] - x[0]) + (end[1] - x[1])  # Heuristic is Manhattan's distance to the end node

    open_set = {start}
    came_from = {}

    g_score = {key: math.inf for key in graph.keys()}
    g_score[start] = 0

    f_score = {key: math.inf for key in graph.keys()}
    f_score[start] = h(start)

    while len(open_set) > 0:
        curr_node = min(open_set, key=lambda x: f_score[x])
        if curr_node == end:
            return f_score[end]
        else:
            open_set.remove(curr_node)
            for neighbor in graph[curr_node].neighbors:
                tentative_g_score = g_score[curr_node] + graph[neighbor].risk
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = curr_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + h(neighbor)
                    if neighbor not in open_set:
                        open_set.add(neighbor)


def assemble_tiles(tiles):
    lines = [[] for i in range(len(tiles) * len(tiles[0][0]))]
    for j_tile in range(len(tiles)):
        for i_line in range(len(tiles[j_tile][0])):
            for i_tile in range(len(tiles[j_tile])):
                lines[len(tiles[j_tile][i_tile]) * j_tile + i_line] += tiles[j_tile][i_tile][i_line]
    return lines


def tile_input(input_lines: List[str]) -> List[str]:
    parsed_map = [[int(char) for char in line.strip()] for line in input_lines]
    tiles = [[0 for i in range(5)] for j in range(5)]
    tiles[0][0] = parsed_map
    for i in range(1, 5):
        new_map = [[risk + 1 if risk + 1 < 10 else 1 for risk in line] for line in tiles[0][i - 1]]
        tiles[0][i] = new_map
    for j in range(1, 5):
        for i in range(0, 5):
            new_map = [[risk + 1 if risk + 1 < 10 else 1 for risk in line] for line in tiles[j - 1][i]]
            tiles[j][i] = new_map
    lines = assemble_tiles(tiles)
    return lines


def pretty_print_map(lines):
    for line in lines:
        print("".join([str(char) for char in line]))


def main():
    with open('input', 'r') as fd:
        lines = tile_input(fd.readlines())
        print("input has size", len(lines), len(lines[0]))
        graph, max_x, max_y = parse_input(lines)
        start = (0, 0)
        end = (max_x, max_y)
        # shortest_path = ijkstra(graph, start, end) # Too slow :'(
        shortest_path = a_star(graph, start, end)
        print("The path of least risk through the cave has a total risk of:", shortest_path)


if __name__ == "__main__":
    main()
