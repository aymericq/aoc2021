import numpy as np


def find_match(beacons1, beacons2, T, R):
    thresh = 12
    for transformation in T:
        for rotation in R:
            for i in range(beacons2.shape[1]):
                beacon_offset = beacons2[:, i].reshape((3, 1))
                for j in range(beacons1.shape[1]):
                    n_match = 0
                    candidate = (transformation @ (rotation @ beacons1))
                    offset = beacon_offset - candidate[:, j].reshape((3, 1))
                    candidate_with_offset = candidate + offset
                    for k in range(beacons2.shape[1]):
                        if k == i:
                            n_match += 1
                        else:
                            comp = np.sum(np.abs(candidate_with_offset - beacons2[:, k].reshape((3, 1))), axis=0) == 0
                            if comp.any():
                                n_match += 1
                    if n_match >= thresh:
                        return n_match, (candidate[:, j], beacons2[:, i]), (transformation, rotation), candidate
                    del candidate
                    del candidate_with_offset


def connected_to_0(j, connections):
    dist = {}
    prev = {}
    for vertex in connections:
        dist[vertex] = np.inf
        prev[vertex] = None
    dist[j] = 0

    q = set(connections.keys())
    while len(q) != 0:
        u = min([(v, dist[v]) for v in q], key=lambda e: e[1])[0]
        q.discard(u)

        for v in [v['p'] for v in connections[u] if v['p'] in q]:
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    if 0 not in dist or dist[0] == np.inf:
        return None
    return prev


def connect(i, j, connections, transf):
    if j not in connections:
        connections[j] = [{'p': i, 'transf': transf}]
    else:
        connections[j].append({'p': i, 'transf': transf})


def transform_beacon_coords(i, beacons_i, connections):
    pos_in_graph = i
    transformed_beacons_i = beacons_i.copy()
    while pos_in_graph in connections:
        transformation, rotation, relative_pos = connections[pos_in_graph]['transf']
        transformed_beacons_i = transformation @ rotation @ transformed_beacons_i + relative_pos
        if 'p' in connections[pos_in_graph]:
            pos_in_graph = connections[pos_in_graph]['p']
    return transformed_beacons_i


def main():
    beacons_array = read_input()
    connections = {}
    for i in range(len(beacons_array)):
        for j in range(i + 1, len(beacons_array)):
            if connected_to_0(i, connections) is not None and connected_to_0(j, connections) is not None:
                continue
            beacons1 = beacons_array[i]
            beacons2 = beacons_array[j]
            res = find_match(beacons2, beacons1, T, R)
            if res is not None:
                n_match, matching_beacons, (transformation, rotation), candidate = res
                relative_pos = (matching_beacons[1] - matching_beacons[0]).reshape((3, 1))
                connect(i, j, connections, lambda b: transformation @ rotation @ b + relative_pos)
                connect(j, i, connections,
                        lambda b: np.invert(rotation) @ np.invert(transformation) @ (b - relative_pos))
                print("Match : ", i, j)

    print(connected_to_0(2, connections))
    # transformed_beacon_coords = [beacons_array[0]]
    # for i in range(1, len(beacons_array)):
    #     transformed_beacon_coords.append(transform_beacon_coords(i, beacons_array[i], connections))
    #
    # beacons = []
    # for i in range(len(transformed_beacon_coords)):
    #     beacons_i = transformed_beacon_coords[i]
    #     for j in range(beacons_i.shape[1]):
    #         if tuple(beacons_i[:, j]) not in beacons:
    #             beacons.append(tuple(beacons_i[:, j]))
    #     print(len(beacons))
    # print(beacons)


def read_input():
    with open('test_input', 'r') as fd:
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


def rotate(scanner):
    rotated_scanner = []
    for i in range(len(scanner)):
        rotated_scanner.append([scanner[i][0], scanner[i][1], scanner[i][2]])
        rotated_scanner.append([scanner[i][0], scanner[i][2], -scanner[i][1]])
        rotated_scanner.append([scanner[i][0], -scanner[i][1], -scanner[i][2]])
        rotated_scanner.append([scanner[i][0], -scanner[i][2], scanner[i][1]])


if __name__ == "__main__":
    main()
