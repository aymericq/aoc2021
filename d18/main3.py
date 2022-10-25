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


# def depthmap2arr(dm, d=1) -> list:
#     dmax = max([e['d'] for e in dm])
#     if d == dmax:
#         return [dm[0]['val'], dm[1]['val']]
#     if dm[0]['d'] == d:
#         # Cas d'un nombre simple à la racine
#         if dm[1]['d'] == d:
#             return [dm[0]['val'], dm[1]['val']]
#         else:
#             return [dm[0]['val'], depthmap2arr(dm[1:], d=d + 1)]
#     elif dm[-1]['d'] == d:
#         return [depthmap2arr(dm[0:-1], d=d + 1), dm[-1]['val']]
#     else:
#         i = find_first_regular_pair(dm)
#         j = find_end_of_snail_number_after_position(dm, i)
#         return [depthmap2arr(dm[0:j], d=d + 1), depthmap2arr(dm[j:], d=d + 1)]


# def depthmap2arr(dm):
#     i = find_first_regular_pair(dm)
#     if i - 1 > 0 and dm[i - 1]['d'] == dm[i]['d'] - 1:
#         arr = [dm[i - 1]['val'], [dm[i]['val'], dm[i + 1]['val']]]
#         # remonter le fil vers la gauche
#         j = i - 2
#         while j >= 0:
#             arr = [dm[j]['val'], arr]
#             j -= 1
#         return arr
#     elif i + 2 < len(dm) - 1 and dm[i + 2]['d'] == dm[i]['d'] - 1:
#         arr = [[dm[i]['val'], dm[i + 1]['val']], dm[i + 2]['val']]
#         while j := find_first_regular_pair(dm[i + 3:]) is not None:
#             j += i + 3
#             pass
#         # Remonter le fil vers la droite
#         j = i + 3
#         while j < len(dm):
#             arr = [arr, dm[j]['val']]
#             j += 1
#         return arr
#     else:
#         arr = [[dm[i], dm[i + 1]], [dm[i + 2], dm[i + 3]]]

# def depthmap2arr(dm):
#     d = dm[0]['d']
#     s = "[" * dm[0]['d'] + str(dm[0]['val'])
#     i = 1
#     while i < len(dm):
#         if dm[i]['d'] > d:
#             s += "," + "[" * (dm[i]['d'] - d) + str(dm[i]['val'])
#         elif dm[i]['d'] == d:
#             s += "," + str(dm[i]['val']) + "]"
#         d = dm[i]['d']
#         i += 1
#     return s

def build_tree(max_depth):
    if max_depth == 0:
        return {'val': None}
    t = {'l': build_tree(max_depth - 1), 'r': build_tree(max_depth - 1), 'val': None}
    if max_depth >= 2:
        t['l']['p'] = t
        t['r']['p'] = t
    return t


def find_next_free_node_at_depth_d(t, d):
    if d == 1:
        if t['l']['val'] is None:
            return t['l']
        elif t['r']['val'] is None:
            return t['r']
        else:
            return None
    else:
        node = find_next_free_node_at_depth_d(t['l'], d-1)
        if node is None:
            node = find_next_free_node_at_depth_d(t['r'], d - 1)
            if node is None:
                return None
            else:
                return node
        else:
            return node

def depthmap2arr(dm):
    max_depth = max([e['d'] for e in dm])
    t = build_tree(max_depth)
    for i in range(len(dm)):
        d = dm[i]['d']
        node = find_next_free_node_at_depth_d(t, d)
        node['val'] = dm[i]['val']
    return t
        #notify_parents(node)





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



if __name__ == "__main__":
    with open("test_input", 'r') as fd:
        lines = [line.strip() for line in fd.readlines()]
    arr0 = eval(lines[0])
    dm = arr2depthmap(arr0)
    for i in range(len(lines)):
        dm1 = arr2depthmap(eval(lines[i]))
        dm = add(dm, dm1)
    print(dm)
    print(depthmap2arr(dm))
