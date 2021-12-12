from typing import List

import numpy as np


def load_map(lines: List[str]) -> np.ndarray:
    energy_map = []
    for line in lines:
        energy_map.append([int(char) for char in line.strip()])
    return np.array(energy_map).astype(np.int8)


def count_adjacent_flashes(energy_map, i, j):
    flashes = 0
    for x, y in [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]:
        if i + x < 10 and i + x >= 0 and j + y < 10 and j + y >= 0 and energy_map[i + x, j + y] == -1:
            flashes += 1
    return flashes


def take_one_step(energy_map: np.ndarray) -> int:
    energy_map += 1
    resume = True
    while resume:
        energy_map[energy_map >= 10] = -1
        current_flashing_pos = []
        for i in range(10):
            for j in range(10):
                if energy_map[i, j] < 0:
                    continue
                adjacent_flashes = count_adjacent_flashes(energy_map, i, j)
                energy_map[i, j] += adjacent_flashes
                if energy_map[i, j] >= 10:
                    current_flashing_pos.append((i, j))
        energy_map[energy_map == -1] = -2
        for pos in current_flashing_pos:
            energy_map[pos[0], pos[1]] = -1
        resume = np.count_nonzero(energy_map == -1) > 0
    energy_map[energy_map == -2] = 0
    return np.count_nonzero(energy_map == 0)


if __name__ == "__main__":
    with open('input', 'r') as fd:
        energy_map = load_map(fd.readlines())
        MAX_STEP = 500
        total_nb_flashes = 0
        for n_step in range(1, MAX_STEP+1):
            flashes = take_one_step(energy_map)
            print("After", n_step, "steps, there has been", flashes, "flashes.")
            total_nb_flashes += flashes
            if n_step == 100:
                print("~~~~~~~~~~~")
                print("After", MAX_STEP, "steps, there has been a total of", total_nb_flashes, "flashes.")
            if np.count_nonzero(energy_map == 0) == 100:
                print("At step", n_step, ", all octopuses have synchronized \\o/")
                break
