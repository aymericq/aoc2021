def histogram(string):
    hist = {}
    for c in string:
        if c in hist:
            hist[c] += 1
        else:
            hist[c] = 1
    return hist


def find_min_max_hist(hist):
    k_min, mini = None, list(hist.values())[0]
    k_max, maxi = None, list(hist.values())[0]
    for key in hist:
        if hist[key] < mini:
            k_min = key
            mini = hist[key]
        if hist[key] > maxi:
            k_max = key
            maxi = hist[key]
    return mini, maxi


if __name__ == "__main__":
    with open('input', 'r') as fd:
        lines = fd.readlines()
        starting_state = lines[0].strip()
        insertion_rules = [line.strip().split(" -> ") for line in lines[2:]]
        matchers = [rule[0] for rule in insertion_rules]
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
        hist = histogram(starting_state)
        mini, maxi = find_min_max_hist(hist)
        print(maxi - mini)

