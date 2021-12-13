from typing import List, Dict


class Node:
    def __init__(self, node_name: str, child_nodes: List[str]):
        self.node_name = node_name
        self.child_nodes = child_nodes
        self.node_type = "BIG" if node_name.isupper() else "SMALL"
        self.visited = False


def parse_graph(lines: List[str]):
    graph = {}
    for line in lines:
        node_a, node_b = line.strip().split('-')
        if node_a not in graph:
            graph[node_a] = Node(node_a, [node_b])
        else:
            graph[node_a].child_nodes.append(node_b)

        if node_a != "start" and node_b != "end":
            if node_b not in graph:
                graph[node_b] = Node(node_b, [node_a])
            else:
                graph[node_b].child_nodes.append(node_a)
    graph["end"] = Node("end", [])
    graph["end"].node_type = "BIG"
    return graph


def pretty_print_graph(graph: Dict[str, Node]):
    for node in graph:
        print(node, "->", ", ".join(graph[node].child_nodes))


"""
def find_routes(graph, node_a, node_b, curr_route, routes):
    print(routes)
    if node_a == "end":
        curr_route.append("end")
        routes.append(curr_route)
        return None
    for curr_node in graph[node_a].child_nodes:
        if curr_node == "end":
            curr_route.append("end")
            routes.append(curr_route)
            return None
        if graph[curr_node].visited and graph[curr_node].node_type == "SMALL":
            return None
        graph[curr_node].visited = True
        curr_route.append(curr_node)
        find_routes(graph, curr_node, node_b, curr_route, routes)
"""


def find_routes(graph, node_a, node_b, visited_nodes):
    visited_nodes = visited_nodes.copy()
    if graph[node_a].node_type == "SMALL":
        if node_a in visited_nodes:
            return []
        else:
            visited_nodes.append(node_a)

    if node_a == node_b:
        return [[node_a]]
    else:
        new_routes = []
        for child_node in graph[node_a].child_nodes:
            routes = find_routes(graph, child_node, node_b, visited_nodes)
            for route in routes:
                if len(route) == 0:
                    continue
                new_routes.append([node_a] + route)
        return new_routes


if __name__ == "__main__":
    with open("input", 'r') as fd:
        lines = fd.readlines()
        graph = parse_graph(lines)
        pretty_print_graph(graph)

        routes = find_routes(graph, "start", "end", [])
        print(routes)
        print("Found", len(routes), "routes.")
