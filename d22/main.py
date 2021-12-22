import numpy as np


def parse_instuctions(lines):
    instructions = []
    for line in lines:
        mode, range_as_str = line.strip().split(" ")
        mode = 1 if mode == "on" else 0
        range_x, range_y, range_z = range_as_str.split(",")
        range_x = [int(n) for n in range_x[2:].split("..")]
        range_y = [int(n) for n in range_y[2:].split("..")]
        range_z = [int(n) for n in range_z[2:].split("..")]
        instructions.append((mode, range_x, range_y, range_z))
    return instructions


def process_instructions(instructions):
    on_cubes = np.zeros((101, 101, 101))
    for i_inst, inst in enumerate(instructions):
        mode, range_x, range_y, range_z = inst

        adjusted_range_x = max(-50, range_x[0]) + 50, min(50, range_x[1]) + 51
        adjusted_range_y = max(-50, range_y[0]) + 50, min(50, range_y[1]) + 51
        adjusted_range_z = max(-50, range_z[0]) + 50, min(50, range_z[1]) + 51
        on_cubes[
                adjusted_range_x[0]:adjusted_range_x[1],
                adjusted_range_y[0]:adjusted_range_y[1],
                adjusted_range_z[0]:adjusted_range_z[1]
        ] = mode
    return on_cubes


def main():
    with open("input", 'r') as fd:
        instructions = parse_instuctions(fd.readlines())
        print(instructions)
        on_cubes = process_instructions(instructions)
        print(np.count_nonzero(on_cubes))


if __name__ == "__main__":
    main()
