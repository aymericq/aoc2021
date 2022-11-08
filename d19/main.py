import gc

import numpy as np


def find_match(beacons1, beacons2, T, R):
    thresh = 12
    for transformation in T:
        for rotation in R:
            for i_beacons2 in range(beacons2.shape[1]):
                beacon_offset = beacons2[:, i_beacons2].reshape((3, 1))
                for j_beacons1 in range(beacons1.shape[1]):
                    n_match = 0
                    candidate = (transformation @ (rotation @ beacons1))
                    offset = beacon_offset - candidate[:, j_beacons1].reshape((3, 1))
                    candidate_with_offset = candidate + offset
                    for k in range(beacons2.shape[1]):
                        if k == i_beacons2:
                            n_match += 1
                        else:
                            comparison = np.sum(
                                np.abs(candidate_with_offset - beacons2[:, k].reshape((3, 1))),
                                axis=0) == 0
                            if comparison.any():
                                n_match += 1
                    if n_match >= thresh:
                        return n_match, \
                               (candidate[:, j_beacons1], beacons2[:, i_beacons2]), \
                               (transformation, rotation), \
                               candidate


def find_path_to_target(source, target, connections):
    # Dijkstra from Wikipedia
    dist = {}
    prev = {}
    for vertex in connections:
        dist[vertex] = np.inf
        prev[vertex] = None
    dist[source] = 0

    q = set(connections.keys())
    while len(q) != 0:
        u = min([(v, dist[v]) for v in q], key=lambda e: e[1])[0]
        q.discard(u)

        for v in [v['p'] for v in connections[u] if v['p'] in q]:
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    if target not in dist or dist[target] == np.inf:
        return None
    s = []
    u = target
    if u in prev or u == source:
        while u is not None:
            s.insert(0, u)
            u = None if u not in prev else prev[u]
    return s


def connect(i, j, connections, transf, args):
    if j not in connections:
        connections[j] = [{'p': i, 'transf': transf, 'args': args}]
    else:
        connections[j].append({'p': i, 'transf': transf, 'args': args})


def transform_beacon_coords(i, beacons_i, connections):
    path = find_path_to_target(i, 0, connections)
    transformed_beacons_i = beacons_i.copy()
    for i_pos_in_graph in range(len(path) - 1):
        pos_in_graph = path[i_pos_in_graph]
        p = path[i_pos_in_graph+1]
        connection = [conn for conn in connections[pos_in_graph] if conn['p'] == p][0]
        transf, (t, r, rp) = connection['transf'], connection['args']
        transformed_beacons_i = transf(t, r, rp, transformed_beacons_i)
    return transformed_beacons_i


def main():
    beacons_array = read_input()
    connections = find_scanners_relative_transformations(beacons_array)

    transformed_beacon_coords = compute_beacons_coord_in_same_space(beacons_array, connections)

    beacons = compute_unique_beacon_coords(transformed_beacon_coords)
    print("There are", len(beacons), "beacons.")

    max_manhattan_distance = find_farthest_scanners(connections, len(beacons_array))
    print("The fursthest 2 scanners are", max_manhattan_distance, "units apart.")


def find_farthest_scanners(connections, n_scanner):
    transformed_scanner_coords = [np.array([[0], [0], [0]])]
    for i in range(1, n_scanner):
        transformed_scanner_coords.append(transform_beacon_coords(i, np.zeros((3, 1)), connections))
    max_dist = 0
    for i in range(len(transformed_scanner_coords)):
        for j in range(i+1, len(transformed_scanner_coords)):
            dist = np.sum(np.abs(transformed_scanner_coords[i] - transformed_scanner_coords[j]))
            if dist > max_dist:
                max_dist = dist
    return max_dist


def compute_unique_beacon_coords(transformed_beacon_coords):
    beacons = []
    for i in range(len(transformed_beacon_coords)):
        beacons_i = transformed_beacon_coords[i]
        for j in range(beacons_i.shape[1]):
            if tuple(beacons_i[:, j]) not in beacons:
                beacons.append(tuple(beacons_i[:, j]))
    return beacons


def compute_beacons_coord_in_same_space(beacons_array, connections):
    transformed_beacon_coords = [beacons_array[0]]
    for i in range(1, len(beacons_array)):
        transformed_beacon_coords.append(transform_beacon_coords(i, beacons_array[i], connections))
    return transformed_beacon_coords


def find_scanners_relative_transformations(beacons_array):
    connections = {}
    for i in range(len(beacons_array)):
        for j in range(i + 1, len(beacons_array)):
            if find_path_to_target(i, 0, connections) is not None and find_path_to_target(j, 0, connections) is not None:
                continue
            beacons1 = beacons_array[i]
            beacons2 = beacons_array[j]
            res = find_match(beacons2, beacons1, T, R)
            if res is not None:
                n_match, matching_beacons, (transformation, rotation), candidate = res
                relative_pos = (matching_beacons[1] - matching_beacons[0]).reshape((3, 1))
                connect(i, j, connections, lambda t, r, rp, b: (t @ r @ b) + rp,
                        (transformation, rotation, relative_pos))
                connect(j, i, connections,
                        lambda t, r, rp, b: (np.linalg.inv(r) @ np.linalg.inv(t) @ (b - rp)).astype(np.int64),
                        (transformation, rotation, relative_pos))
                print("Match : ", i, j)
        gc.collect()
    return connections


def read_input():
    with open('test_input2', 'r') as fd:
        lines = [line.strip() for line in fd.readlines()]
        beacons = []
        beacon_arrays = []
        for i, line in enumerate(lines):
            if i == 0:
                continue
            if len(line) == 0:
                del line
            elif line[:12] == "--- scanner ":
                beacon_arrays.append(np.array(beacons).T)
                beacons = []
            else:
                beacons.append([int(coord) for coord in line.split(',')])
        beacon_arrays.append(np.array(beacons).T)
    return beacon_arrays


Rr1 = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])
Rr2 = np.array([
    [0, 1, 0],
    [-1, 0, 0],
    [0, 0, 1]
])
Rr3 = np.array([
    [-1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
])
Rr4 = np.array([
    [0, -1, 0],
    [1, 0, 0],
    [0, 0, 1]
])

Rx1 = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])
Rx2 = np.array([
    [1, 0, 0],
    [0, 0, 1],
    [0, -1, 0],
])
Rx3 = np.array([
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, -1],
])
Rx4 = np.array([
    [1, 0, 0],
    [0, 0, -1],
    [0, 1, 0],
])
Ry1 = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [-1, 0, 0],
])
Ry2 = np.array([
    [0, 0, -1],
    [0, 1, 0],
    [1, 0, 0],
])
R = [Rr1, Rr2, Rr3, Rr4]
T = [Rx1, Rx2, Rx3, Rx4, Ry1, Ry2]

if __name__ == "__main__":
    main()
