def main():
    with open("test_input", 'r') as fd:
        lines = [line.strip() for line in fd.readlines()]
    arr0 = eval(lines[0])
    dm = arr2depthmap(arr0)
    for i in range(1, len(lines)):
        dm1 = arr2depthmap(eval(lines[i]))
        dm = add(dm, dm1)
    t = depthmap2btree(dm)
    m = magnitude(t)
    print("Magnitude:", m)
    magnitudes = []
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i != j:
                dm1 = arr2depthmap(eval(lines[i]))
                dm2 = arr2depthmap(eval(lines[j]))
                dm = add(dm1, dm2)
                magnitudes.append(magnitude(depthmap2btree(dm)))
    print("Max :", max(magnitudes))


def magnitude(t):
    if t['val'] is not None:
        return t['val']
    return 3*magnitude(t['l']) + 2*magnitude(t['r'])


def arr2depthmap(a):
    if isinstance(a, int):
        return {'val': a, 'd': 0}
    l = []
    for i in range(len(a)):
        dm = arr2depthmap(a[i])
        if isinstance(dm, dict):
            dm['d'] += 1
            l.append(dm)
        else:
            for e in dm:
                e['d'] += 1
            l.extend(dm)
    return l


def find_first_regular_pair(dm):
    i = 0
    while i < len(dm) - 1:
        if dm[i]['d'] == dm[i + 1]['d']:
            return i
        i += 1
    return None


def find_end_of_snail_number_after_position(dm, i):
    j = i + 1
    while j < len(dm) - 1:
        if dm[j]['d'] <= dm[j + 1]['d']:
            return j
        j += 1
    return None


def build_tree(max_depth):
    if max_depth == 0:
        return {'val': None, 'children_full': False}
    t = {'l': build_tree(max_depth - 1), 'r': build_tree(max_depth - 1), 'val': None, 'children_full': False}
    if max_depth >= 1:
        t['l']['p'] = t
        t['r']['p'] = t
    return t


def notify_parent(node):
    if 'p' in node and node['p'] is not None \
            and node['p']['l']['children_full'] and node['p']['r']['children_full']:
        node['p']['children_full'] = True
        notify_parent(node['p'])


def find_next_free_node_at_depth_d(t, d):
    if t['children_full']:
        return None
    if d == 0:
        if t['val'] is None and not t['children_full']:
            return t
        else:
            return None
    else:
        node = find_next_free_node_at_depth_d(t['l'], d - 1)
        if node is None:
            node = find_next_free_node_at_depth_d(t['r'], d - 1)
            if node is None:
                return None
            else:
                return node
        else:
            return node


def depthmap2btree(dm):
    max_depth = max([e['d'] for e in dm])
    t = build_tree(max_depth)
    for i in range(len(dm)):
        d = dm[i]['d']
        node = find_next_free_node_at_depth_d(t, d)
        node['val'] = dm[i]['val']
        node['children_full'] = True
        notify_parent(node)
    return t


def print_tree(t, d=0):
    print(" " * 2 * d + "-- val:", t['val'], ", cf:", t['children_full'], ", d:", d)
    if 'l' in t and t['l'] is not None:
        print_tree(t['l'], d + 1)
    if 'r' in t and t['r'] is not None:
        print_tree(t['r'], d + 1)


def split(dm):
    copy = dm.copy()
    i = 0
    while i < len(dm):
        val = copy[i]['val']
        if val >= 10:
            copy[i]['val'] = val // 2
            copy[i]['d'] += 1
            copy.insert(i + 1, {'val': val - (val // 2), 'd': copy[i]['d']})
            return copy, True
        i += 1
    return copy, False


def explode(s):
    i_max = 0
    max_d = s[0]['d']
    for i, e in enumerate(s):
        if e['d'] > max_d:
            max_d = e['d']
            i_max = i

    i = i_max
    e = s[i]
    if e['d'] > 4:
        if i == 0:
            e['val'] = 0
            e['d'] -= 1
            s[i + 2]['val'] = s[i + 1]['val'] + s[i + 2]['val']
            del s[i + 1]
            return True
        elif i == len(s) - 2:
            s[i + 1]['val'] = 0
            s[i + 1]['d'] -= 1
            s[i - 1]['val'] = s[i - 1]['val'] + s[i]['val']
            del s[i]
            return True
        else:
            s[i - 1]['val'] = s[i - 1]['val'] + e['val']
            if i + 2 < len(s):
                s[i + 2]['val'] = s[i + 1]['val'] + s[i + 2]['val']
            s[i]['d'] -= 1
            s[i]['val'] = 0
            del s[i + 1]
            return True
    return False


def add(dm1, dm2) -> list:
    dm = dm1 + dm2
    for e in dm:
        e['d'] += 1
    dm = reduce(dm)
    return dm


def reduce(dm):
    has_exploded, has_split = True, True
    while has_exploded or has_split:
        has_exploded = explode(dm)
        if has_exploded:
            continue
        dm, has_split = split(dm)
    return dm


def pretty_print_t(t):
    s = ""
    if not 'l' in t:
        return str(t['val'])
    if t['l'] is not None:
        if t['l']['val'] is not None:
            s += "[" + str(t['l']['val'])
        else:
            s += "[" + pretty_print_t(t['l'])
    if t['r'] is not None:
        if t['r']['val'] is not None:
            s += ", " + str(t['r']['val'])
        else:
            s += ", " + str(pretty_print_t(t['r']))
    s += "]"
    return s


if __name__ == "__main__":
    main()
