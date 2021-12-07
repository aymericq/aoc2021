import numpy as np
import matplotlib.pyplot as plt

def read_input(str_input):
    return [int(pos) for pos in str_input.strip().split(',')]

with open('input', 'r') as fd:
    h_pos = np.array(read_input(fd.readline()))
    h_pos.shape = (1, len(h_pos))
    h_pos_rep = np.tile(h_pos, (np.max(h_pos), 1))
    m = np.arange(0, np.max(h_pos))
    m.shape = (m.shape[0], 1)
    diffs = np.abs(h_pos - m)
    fuel_cons = np.sum(np.multiply(diffs, diffs+1)/2, 1)
    print(fuel_cons)
    print("Best h_pos is:", np.argmin(fuel_cons))
    print("Fuel cons is:", np.min(fuel_cons))
    plt.plot(fuel_cons) # For my own curiosity
    plt.show()