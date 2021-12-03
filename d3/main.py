def find_gamma_eps(l):
    counts = [0]*len(l[0])
    for line in l:
        for i, c in enumerate(line):
            counts[i] += int(c.strip())
    gamma = ['1' if c >= len(l) // 2 else '0' for c in counts]
    eps = ['0' if c == '1' else '1' for c in gamma]
    return ("".join(gamma), "".join(eps))

def filter_on_char(l, i_char, char):
    return [line for line in l if line[i_char] == char]

def find_most_used_digit_at_pos(l, i_char):
    s = 0
    for i in range(len(l)):
        if l[i][i_char] == '1':
            s += 1
    return '1' if s >= len(l)/2 else '0'

def binary2dec(val):
    return sum([2**i for i in range(len(val)-1, -1, -1) if val[len(val)-1-i] == '1'])

with open('input', 'r') as fd:
    lines = [line.strip() for line in fd.readlines()]
    gamma, eps = find_gamma_eps(lines)
    print("gamma", gamma, ", eps", eps)
    gamma_val = sum([2**i for i in range(len(gamma)-1, -1, -1) if gamma[len(eps)-1-i] == '1'])
    eps_val = sum([2**i for i in range(len(eps)-1, -1, -1) if eps[len(eps)-1-i] == '1'])
    print("gamma val:", gamma_val, "eps_val:", eps_val)
    print("res:", gamma_val*eps_val)

    trunc_list_gamma = lines
    trunc_list_eps = lines
    for i in range(len(gamma)):
        char_gamma = find_most_used_digit_at_pos(trunc_list_gamma, i)
        char_eps = '0' if find_most_used_digit_at_pos(trunc_list_eps, i) == '1' else '1'
        trunc_list_gamma = filter_on_char(trunc_list_gamma, i, char_gamma)
        trunc_list_eps = filter_on_char(trunc_list_eps, i, char_eps)
        if len(trunc_list_gamma) == 1:
            print("O2 rating", trunc_list_gamma[0])
            o2 = trunc_list_gamma[0]
        if len(trunc_list_eps) == 1:
            print("CO2 rating", trunc_list_eps[0])
            co2 = trunc_list_eps[0]

    o2_val = binary2dec(o2)
    co2_val = binary2dec(co2)
    print("O2 val:", o2_val, ", CO2 val:", co2_val)
    print("Result:", o2_val*co2_val)