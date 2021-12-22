def pretty_print_target(x_bounds, y_bounds, traj=None):
    min_x, max_x = min(x_bounds), max(x_bounds)
    min_y, max_y = min(y_bounds), max(y_bounds)

    lines = []
    # Target on the right
    lines.append(list('x' + '.' * (max_x - min_x) + '.' * min_x))
    for i_line in range(-1, min_y - 1, -1):
        if i_line in range(min_y, max_y + 1):
            lines.append(list('.' * min_x + '-' * (max_x - min_x + 1)))
        else:
            lines.append(list('.' * min_x + '.' * (max_x - min_x + 1)))

    if traj is not None:
        for pos in traj:
            y, x = -pos[1], pos[0]
            if 0 <= y < -min_y and x < max_x:
                lines[y][x] = 'O'
    for line in lines:
        print("".join(line))


def compute_traj(v_x, v_y, n_step):
    traj = []
    pos = [0, 0]
    for i_step in range(n_step):
        pos[0] += v_x
        pos[1] += v_y
        traj.append(pos.copy())
        v_x -= 1
        v_x = v_x if v_x >= 0 else 0
        v_y -= 1
    return traj


def touches_target(traj, x_bounds, y_bounds):
    for pos in traj:
        if x_bounds[0] <= pos[0] <= x_bounds[1] and y_bounds[0] <= pos[1] <= y_bounds[1]:
            return True
    return False


def main():
    with open('input', 'r') as fd:
        xbounds_str, ybounds_str = fd.readline().strip().strip("target area: ").split(', ')
        x_bounds = [int(bound) for bound in xbounds_str[2:].split("..")]
        y_bounds = [int(bound) for bound in ybounds_str[2:].split("..")]

        print("x bounds:", x_bounds)
        print("y bounds:", y_bounds)

        count = 0
        for v_x in range(0, max(x_bounds)+1):
            for v_y in range(min(y_bounds), 200):
                traj = compute_traj(v_x, v_y, 1000)
                touches_target_for_velo = touches_target(traj, x_bounds, y_bounds)
                if touches_target_for_velo:
                    count += 1
        print(count, "initial values touched target")

        traj = compute_traj(v_x, 95, 1000)
        print("max_y", max(map(lambda pos: pos[1], traj)))
        print("Touches target? ->", touches_target_for_velo)


if __name__ == "__main__":
    main()
