from typing import List


def histogram(string):
    hist = {}
    for c in string:
        if c in hist:
            hist[c] += 1
        else:
            hist[c] = 1
    return hist


def find_min_max_hist(hist):
    mini = min(hist.values())
    maxi = max(hist.values())
    return mini, maxi


def populate_pairs_from_template(starting_state):
    pairs = {}
    for i in range(len(starting_state) - 1):
        if starting_state[i: i + 2] in pairs:
            pairs[starting_state[i: i + 2]] += 1
        else:
            pairs[starting_state[i: i + 2]] = 1
    return pairs


def hist_from_pairs(pairs, template):
    hist = {}
    keys = list(pairs.keys())
    for key in keys:
        if key[0] in hist:
            hist[key[0]] += pairs[key]
        else:
            hist[key[0]] = pairs[key]

    hist[template[-1]] += 1
    return hist


def compute_pairs_v2(pairs, matchers, insertion_rules):
    for i in range(10):
        new_pairs = {}
        for pair in pairs:
            nb_new_pairs = pairs[pair]
            try:
                index = matchers.index(pair)
                new_pair_left = pair[0] + insertion_rules[index][1]
                new_pair_right = insertion_rules[index][1] + pair[1]
                if new_pair_left in new_pairs:
                    new_pairs[new_pair_left] += nb_new_pairs
                else:
                    new_pairs[new_pair_left] = nb_new_pairs
                if new_pair_right in new_pairs:
                    new_pairs[new_pair_right] += nb_new_pairs
                else:
                    new_pairs[new_pair_right] = nb_new_pairs
            except ValueError:
                if pair in new_pairs:
                    new_pairs[pair] += nb_new_pairs
                else:
                    new_pairs[pair] = nb_new_pairs
        pairs = new_pairs.copy()
    return pairs


def compute_pairs_v3(pairs: List, matchers, insertion_rules):
    new_pairs = {}
    for i_matcher, matcher in enumerate(matchers):
        if matcher in pairs:
            nb_pairs = pairs[matcher]
            new_pair = matcher[0] + insertion_rules[i_matcher][1]
            if new_pair in new_pairs:
                new_pairs[new_pair] += nb_pairs
            else:
                new_pairs[new_pair] = nb_pairs

            new_pair = insertion_rules[i_matcher][1] + matcher[1]
            if new_pair in new_pairs:
                new_pairs[new_pair] += nb_pairs
            else:
                new_pairs[new_pair] = nb_pairs
    return new_pairs


def main(lines):
    starting_state = lines[0].strip()
    insertion_rules = [line.strip().split(" -> ") for line in lines[2:]]
    matchers = [rule[0] for rule in insertion_rules]

    pairs = populate_pairs_from_template(starting_state)
    print(pairs)
    for i_step in range(40):
        pairs = compute_pairs_v3(pairs, matchers, insertion_rules)

    print(pairs)

    hist = hist_from_pairs(pairs, starting_state)
    print(hist)

    """
    MAX_STEPS = 10
    for i_step in range(MAX_STEPS):
        new_str = ""
        for i in range(len(starting_state) - 1):
            try:
                index = matchers.index(starting_state[i:i+2])
                new_str += starting_state[i] + insertion_rules[index][1]
            except ValueError:
                new_str += starting_state[i]
        new_str += starting_state[-1]
        starting_state = new_str
    """
    # hist = histogram(final_str)
    mini, maxi = find_min_max_hist(hist)
    print(maxi - mini)
    assert maxi - mini == 2265039461737 # 2265039461738 - 1 for a reason....


if __name__ == "__main__":
    with open('test_input', 'r') as fd:
        lines = fd.readlines()
        main(lines)
