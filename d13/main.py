def parse_input(lines):
    dots = []
    folds = []
    dot_section = True
    for line in lines:
        if len(line.strip()) == 0:
            dot_section = False
            continue
        if dot_section:
            x, y = line.strip().split(',')
            dots.append((int(x), int(y)))
        else:
            axis, pos = line[11:].split('=')
            folds.append((axis, int(pos)))
    return dots, folds


def fold_dots(fold, dots):
    dots_after_folding = []
    if fold[0] == 'y':
        fold_pos = fold[1]
        for dot in dots:
            new_dot = None
            if dot[1] > fold_pos:
                new_dot = (dot[0], fold_pos - (dot[1] - fold_pos))
            else:
                new_dot = dot
            add_dot_if_not_present(dots_after_folding, new_dot)
    if fold[0] == 'x':
        fold_pos = fold[1]
        for dot in dots:
            new_dot = None
            if dot[0] > fold_pos:
                new_dot = (fold_pos - (dot[0] - fold_pos), dot[1])
            else:
                new_dot = dot
            add_dot_if_not_present(dots_after_folding, new_dot)
    return dots_after_folding


def add_dot_if_not_present(dots_after_folding, new_dot):
    for dot in dots_after_folding:
        if dot[0] == new_dot[0] and dot[1] == new_dot[1]:
            return None
    dots_after_folding.append(new_dot)


def pretty_print_code(dots):
    max_x = max(map(lambda d: d[0], dots))
    max_y = max(map(lambda d: d[1], dots))
    lines = [[' ' for i in range(max_x + 1)] for j in range(max_y + 1)]
    for dot in dots:
        lines[dot[1]][dot[0]] = '#'
    for line in lines:
        print("".join(line))


if __name__ == "__main__":
    with open('input', 'r') as fd:
        dots, folds = parse_input(fd.readlines())
        print(dots)
        for i_fold, fold in enumerate(folds):
            dots_after_folding = fold_dots(fold, dots)
            dots = dots_after_folding.copy()
            if i_fold == 0:
                print("After first fold, there are:", len(dots), "dots left.")
        pretty_print_code(dots)
