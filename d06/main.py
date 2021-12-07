def load_initial_state(initial_state_input):
    initial_state_input = initial_state_input.strip()
    values = [int(val) for val in initial_state_input.split(',')]
    hist = {val: 0 for val in range(9)}
    for val in values:
        hist[val] += 1
    return hist


def process_one_iteration(histogram):
    new_hist = {val: 0 for val in range(9)}
    for key, val in zip(histogram.keys(), histogram.values()):
        if key > 0:
            new_hist[key-1] = val
    new_hist[8] = histogram[0]
    new_hist[6] += histogram[0]
    return new_hist

with open('input', 'r') as fd:
    histogram = load_initial_state(fd.readline())
    print("Initial state is:", histogram)
    for i_iter in range(1, 256+1):
        histogram = process_one_iteration(histogram)
        print("After it", i_iter, ", state is:", histogram)
        print("After it", i_iter, "there are", sum(histogram.values()), "individuals")
