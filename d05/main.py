import numpy as np

def load_lines(input):
    lines = []
    max_x = 0
    max_y = 0
    for line in input:
        z1, z2 = [z.strip() for z in line.split('->')]
        x1, y1 = [int(n) for n in z1.split(',')]
        x2, y2 = [int(n) for n in z2.split(',')]
        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)
        lines.append([(x1, y1), (x2, y2)])
    return lines, max_x, max_y

def increase_count_diagonal(map_currents, line):
    z1, z2 = line
    x1, y1 = z1
    x2, y2 = z2
    for i in range(abs(x1 - x2) + 1):
        dir_x = 1 if x1 < x2 else -1
        dir_y = 1 if y1 < y2 else -1
        map_currents[y1+i*dir_y, x1+i*dir_x] += 1


with open('input', 'r') as fd:
    lines, max_x, max_y = load_lines(fd.readlines())
    map_currents = np.zeros((max_y+1, max_x+1))
    for line in lines:
        if line[0][0] == line[1][0]:
            if line[0][1] < line[1][1]:
                map_currents[line[0][1]:line[1][1]+1, line[0][0]] += 1
            else:
                map_currents[line[1][1]:line[0][1]+1, line[0][0]] += 1
        elif line[0][1] == line[1][1]:
            if line[0][0] < line[1][0]:
                map_currents[line[0][1], line[0][0]:line[1][0]+1] += 1
            else:
                map_currents[line[0][1], line[1][0]:line[0][0]+1] += 1
        else:
            increase_count_diagonal(map_currents, line)

    map_currents[map_currents<2] = 0
    map_currents[map_currents>=2] = 1
    print("Result:", np.count_nonzero(map_currents))
