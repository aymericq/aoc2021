import numpy as np


def load_height_map():
    y_size = len(lines)
    x_size = len(lines[0].strip())
    height_map = 9 * np.ones((y_size + 2, x_size + 2))
    for i_line, line in enumerate(lines):
        height_map[i_line + 1, 1:-1] = [int(char) for char in line.strip()]
    return y_size, x_size, height_map


def compute_lowest_points_and_risk():
    sum_of_risks = 0
    lowest_points = []
    for x in range(1, x_size + 1):
        for y in range(1, y_size + 1):
            if (height_map[y, x] < height_map[y - 1, x]
                    and height_map[y, x] < height_map[y + 1, x]
                    and height_map[y, x] < height_map[y, x - 1]
                    and height_map[y, x] < height_map[y, x + 1]):
                sum_of_risks += height_map[y, x] + 1
                lowest_points.append((y, x))
    return sum_of_risks, lowest_points


def augment_enveloppe(basin_lowest, height_map, points_in_basin, curr_enveloppe):
    new_enveloppe = []
    for y_offset, x_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        basin_lowest_y, basin_lowest_x = basin_lowest
        if (not height_map[basin_lowest_y + y_offset, basin_lowest_x + x_offset] == 9 and height_map[
            basin_lowest_y + y_offset, basin_lowest_x + x_offset] >= height_map[basin_lowest_y, basin_lowest_x]):
            is_curr_pos_already_in_basin = len(
                list(filter(lambda pos: pos[0] == basin_lowest_y + y_offset and pos[1] == basin_lowest_x + x_offset,
                            points_in_basin))) == 1
            is_curr_pos_already_in_curr_enveloppe = len(
                list(filter(lambda pos: pos[0] == basin_lowest_y + y_offset and pos[1] == basin_lowest_x + x_offset,
                            curr_enveloppe))) == 1
            if not is_curr_pos_already_in_basin and not is_curr_pos_already_in_curr_enveloppe:
                new_enveloppe.append((basin_lowest_y + y_offset, basin_lowest_x + x_offset))
    return new_enveloppe


def compute_basins_size(height_map, lowest_points):
    basin_sizes = []
    for basin_lowest in lowest_points:
        points_in_basin = []
        new_enveloppe = [basin_lowest]
        while (len(new_enveloppe) > 0):
            curr_pos = new_enveloppe.pop()
            points_in_basin.append(curr_pos)
            new_enveloppe.extend(augment_enveloppe(curr_pos, height_map, points_in_basin, new_enveloppe))
        basin_sizes.append(len(points_in_basin))
    return basin_sizes

if __name__ == "__main__":
    with open('input', 'r') as fd:
        lines = fd.readlines()
        y_size, x_size, height_map = load_height_map()

        sum_of_risks, lowest_points = compute_lowest_points_and_risk()
        print("sum of risks is", sum_of_risks)
        basin_sizes = sorted(compute_basins_size(height_map, lowest_points), reverse=True)
        product = basin_sizes[0]*basin_sizes[1]*basin_sizes[2]
        print("Product of 3 biggest basins is", product)
