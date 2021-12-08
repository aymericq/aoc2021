def parse_input(puzzle_input):
    digits_str, code_str = [e.strip() for e in puzzle_input.strip().split('|')]
    digits_array = [e.strip() for e in digits_str.split(' ')]
    code_str = [e.strip() for e in code_str.split(' ')]
    return digits_array, code_str

def compute_intersection(digit1, digit2):
    set1 = set(digit1)
    set2 = set(digit2)
    return set1.symmetric_difference(set2)


def compute_code(puzzle):
    mixed_signals, ciphered_code = puzzle
    candidates = mixed_signals.copy()
    decoder = {}
    decoder[1] = [digit for digit in candidates if len(digit) == 2][0]
    del candidates[candidates.index(decoder[1])]
    decoder[7] = [digit for digit in candidates if len(digit) == 3][0]
    del candidates[candidates.index(decoder[7])]
    decoder[4] = [digit for digit in candidates if len(digit) == 4][0]
    del candidates[candidates.index(decoder[4])]
    decoder[8] = [digit for digit in candidates if len(digit) == 7][0]
    del candidates[candidates.index(decoder[8])]

    intersection_4_8 = compute_intersection(decoder[4], decoder[8])
    two_six_zero = [digit for digit in candidates if intersection_4_8.issubset(set(digit))]
    decoder[2] = [digit for digit in two_six_zero if len(digit) == 5][0]
    del candidates[candidates.index(decoder[2])]

    six_zero = [digit for digit in two_six_zero if len(digit) == 6]

    intersection_4_7 = compute_intersection(decoder[4], decoder[7])
    nine_five_six = [digit for digit in candidates if intersection_4_7.issubset(set(digit))]

    six = set(six_zero).intersection(nine_five_six).pop()
    decoder[6] = six
    del candidates[candidates.index(decoder[6])]

    zero = set(six_zero).symmetric_difference([six]).pop()
    decoder[0] = zero
    del candidates[candidates.index(decoder[0])]

    nine_five = set(nine_five_six).difference([six])
    decoder[9] = [digit for digit in nine_five if len(digit) == 6][0]
    del candidates[candidates.index(decoder[9])]

    decoder[5] = [digit for digit in nine_five if len(digit) == 5][0]
    del candidates[candidates.index(decoder[5])]

    decoder[3] = candidates[0]
    reverse_decoder = {"".join(sorted(decoder[value])): str(value) for value in decoder.keys()}

    return "".join([reverse_decoder["".join(sorted(digit))] for digit in ciphered_code])


if __name__ == "__main__":
    with open('input', 'r') as fd:
        tuples_of_mixed_signal_and_codes = [parse_input(line) for line in fd.readlines()]
        codes = [entry[1] for entry in tuples_of_mixed_signal_and_codes]
        count_of_decipherable_digit_per_code = map(lambda code: sum([1 for digit in code if len(digit) in [2, 3, 4, 7]]), codes)
        print("There are", sum(count_of_decipherable_digit_per_code), "decipherable digits for the first part.")

        sum_of_codes = 0
        for puzzle in tuples_of_mixed_signal_and_codes:
            code = int(compute_code(puzzle))
            sum_of_codes += code
        print("Sum of codes:", sum_of_codes)
