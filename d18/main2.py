from typing import Tuple


def main():
    with open("test_input", 'r') as fd:
        lines = fd.readlines()


def find_depth(s, d=4):
    if d == 0:
        return []
    if isinstance(s, list):
        for i in range(len(s)):
            path = find_depth(s[i], d - 1)
            if path is not None:
                return [i] + path


def find_left(s, path):
    pair = s.copy()
    for i in range(len(path)):
        pair = pair[path[i]]

    for i in range(len(path)-1, -1, -1):
        if path[i] - 1 >= 0:
            path[-1] = i-1


    return pair


def explode(s):
    path = find_depth(s)
    if path is not None:
        l = find_left(s, path)


def split(s):
    pass


def reduce(s) -> Tuple[bool, object]:
    has_exploded, s = explode(s)
    if not has_exploded:
        has_split, s = split(s)
    if not has_split:
        return False, s
    else:
        return reduce(s)


def add(sn1, sn2):
    s = [sn1, sn2]
    return reduce(s)


if __name__ == "__main__":
    A = [1, [2, 3, [4, [5, 6]], []]]
    path = find_depth(A)[:-1]
    print("path is:", path)
    print(find_left(A, path))
