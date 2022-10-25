from typing import Union


def main():
    with open("test_input", 'r') as fd:
        lines = fd.readlines()


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


# def depthmap2arr(dm, d=1) -> list:
#     i = 0
#     arr = []
#     while i < len(dm):
#         if dm[i]['d'] > d:
#             j = 0
#             while i + j < len(dm):
#                 if dm[i + j]['d'] <= d:
#                     break
#                 j += 1
#             new_arr = depthmap2arr(dm[i:i + j], d + 1)
#             arr.append(new_arr)
#             i += j
#         else:
#             arr.append(dm[i]['val'])
#             i += 1
#     return arr

def find_first_regular_pair(dm):
    i = 0
    while i < len(dm) - 1:
        if dm[i]['d'] == dm[i+1]['d']:
            return i
        i += 1
    return None


def find_end_of_snail_number_after_position(dm, i):
    j = i + 1
    while j < len(dm) - 1:
        if dm[j]['d'] <= dm[j+1]['d']:
            return j
        j += 1
    return None



def depthmap2arr(dm, d=1) -> list:
    dmax = max([e['d'] for e in dm])
    if d == dmax:
        return [dm[0]['val'], dm[1]['val']]
    if dm[0]['d'] == d:
        # Cas d'un nombre simple à la racine
        if dm[1]['d'] == d:
            return [dm[0]['val'], dm[1]['val']]
        else:
            return [dm[0]['val'], depthmap2arr(dm[1:], d=d+1)]
    elif dm[-1]['d'] == d:
        return [depthmap2arr(dm[0:-1], d=d+1), dm[-1]['val']]
    else:
        i = find_first_regular_pair(dm)
        j = find_end_of_snail_number_after_position(dm, i)
        return [depthmap2arr(dm[0:j], d=d+1), depthmap2arr(dm[j:], d=d+1)]




def reduce(s):
    i_max = 0
    max_d = s[0]['d']
    for i, e in enumerate(s):
        if e['d'] > max_d:
            max_d = e['d']
            i_max = i

    i = i_max
    e = s[i]
    if e['d'] >= 4:
        if i == 0:
            e['val'] = 0
            e['d'] -= 1
            s[i + 2]['val'] = s[i + 1]['val'] + s[i + 2]['val']
            del s[i + 1]
            return
        elif i == len(s) - 2:
            s[i + 1]['val'] = 0
            s[i + 1]['d'] -= 1
            s[i - 1]['val'] = s[i - 1]['val'] + s[i]['val']
            del s[i]
            return
        else:
            s[i - 1]['val'] = s[i - 1]['val'] + e['val']
            if i + 2 < len(s):
                s[i + 2]['val'] = s[i + 1]['val'] + s[i + 2]['val']
            s[i]['d'] -= 1
            s[i]['val'] = 0
            del s[i + 1]


def add(s1: Union[list, int], s2: Union[list, int]) -> list:
    s = [s1, s2]
    dm = arr2depthmap(s)
    reduce(dm)
    return dm


if __name__ == "__main__":
    A = [1, [2], [3, [[4]]]]
    B = [8, 9]
    print('non-reduced sum:', [A, B])
    s = add(A, B)
    print("s:", s)

    s = [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    print('non-reduced:', s)
    s = arr2depthmap(s)
    reduce(s)
    print(s)

    arr = depthmap2arr(s)
    print(arr)
