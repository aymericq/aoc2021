import math
from typing import Tuple, List, Dict


class Node(object):
    def __init__(self, risk, neighbors):
        self.risk = risk
        self.neighbors = neighbors


def neighbors_for(x: int, y: int, max_x: int, max_y: int) -> List[Tuple[int]]:
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


def djikstra(graph, start, end):
    unvisited_set = set(graph.keys())
    distances = {key: math.inf for key in graph.keys()}
    curr_node = start
    distances[curr_node] = 0
    end_node_not_visited = True
    while end_node_not_visited:
        for neighbor in graph[curr_node].neighbors:
            if neighbor in unvisited_set:
                tentative_new_dist = distances[curr_node] + graph[neighbor].risk
                if tentative_new_dist < distances[neighbor]:
                    distances[neighbor] = tentative_new_dist
        unvisited_set.remove(curr_node)
        if end not in unvisited_set:
            end_node_not_visited = False
        else:
            curr_node = min(unvisited_set, key=lambda x: distances[x])

    return distances[end]


def assemble_tiles(tiles):
    lines = [[] for i in range(len(tiles) * len(tiles[0][0]))]
    for j_tile in range(len(tiles)):
        for i_line in range(len(tiles[j_tile][0])):
            for i_tile in range(len(tiles[j_tile])):
                lines[len(tiles[j_tile][i_tile])*j_tile + i_line] += tiles[j_tile][i_tile][i_line]
            print(lines[len(tiles)*j_tile + i_line])
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
        print(line)


def main():
    with open('input', 'r') as fd:
        lines = tile_input(fd.readlines())
        pretty_print_map(lines)
        print("input has size", len(lines), len(lines[0]))
        graph, max_x, max_y = parse_input(lines)
        print("max_x, max_y", max_x, max_y)
        start = (0, 0)
        end = (max_x, max_y)
        shortest_path = djikstra(graph, start, end)
        print(shortest_path)


if __name__ == "__main__":
    main()
