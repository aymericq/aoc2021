import json
from typing import List, Union


class SnailNumber:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        if isinstance(self.val, int):
            return str(self.val)
        else:
            return "["+",".join([str(subval) for subval in self.val]) + "]"


def replace_with_snail_number(number: Union[int, List]) -> SnailNumber:
    if isinstance(number, int):
        return SnailNumber(number)
    else:
        sub_numbers = []
        for subnumber in number:
            sub_numbers.append(replace_with_snail_number(subnumber))
        return SnailNumber(sub_numbers)


def parse_input(lines: List[str]) -> List[SnailNumber]:
    numbers = []
    for line in lines:
        numbers.append(json.loads(line.strip()))
    s_numbers = []
    for line in numbers:
        s_numbers.append(replace_with_snail_number(line))
    return s_numbers


def explode(number: SnailNumber, depth=0, left_num=None, right_num=None) -> SnailNumber:
    if depth == 0:
        for i_sub, sub_number in enumerate(number.val):
            result = explode(sub_number, depth=1)
            if result is not None:
                number.val[i_sub].val = result.val
                return number
        return None
    else:
        if depth == 3:
            if isinstance(number.val, int):
                return None
            else:
                first_number_is_int = isinstance(number.val[0].val, int)
                if first_number_is_int:
                    l_num = number.val[0].val + number.val[1].val[0].val
                    r_num = number.val[1].val[1].val + right_num.val if right_num is not None else 0
                    new_number = [SnailNumber(l_num), SnailNumber(r_num)]
                else:
                    l_num = left_num.val + number.val[0].val[0].val if left_num is not None else 0
                    r_num = number.val[0].val[1].val + number.val[1].val
                    new_number = [SnailNumber(l_num), SnailNumber(r_num)]
                # print("new number is", new_number)
                return SnailNumber(new_number)
        else:
            number_is_list = isinstance(number.val, List)
            if number_is_list:
                for i_sub, sub_number in enumerate(number.val):
                    result = explode(sub_number, depth=depth + 1)
                    if result is not None:
                        number.val[i_sub].val = result.val
                        return number
            else:
                return None


"""
def explode(number: SnailNumber, depth=0) -> SnailNumber:
    print("Exploding number", number)
    if depth == 3:
        print("At depth 3:", number)
        if isinstance(number, List):
            if isinstance(number[0], int):
                if isinstance(number[1], int):
                    return False, []
                else:
                    new_number = [number[0] + number[1][0], 0]
                    print("new_number", new_number)
                    return True, new_number
            else:
                new_number = [0, number[0][1] + number[1]]
                print("new_number", new_number)
                return True, new_number
        else:
            return False, []
    elif isinstance(number, List):
        for i_sub, subnumber in enumerate(number):
            has_exploded, new_number = explode(subnumber, depth + 1)
            if has_exploded:
                number[i_sub] = new_number
                if depth == 0:
                    return number
                else:
                    return True, number
    else:
        return False, number
"""


def reduce_s_number(number: SnailNumber) -> SnailNumber:
    if can_be_exploded:
        number = explode(number)
        number = reduce_s_number(number)
    if can_be_split:
        number = split(number)
        number = reduce_s_number(number)
    return number


def add_s_numbers(number_a: SnailNumber, number_b: SnailNumber) -> SnailNumber:
    number_before_reduction = number_a + number_b
    return reduce_s_number(number_before_reduction)


def main():
    with open("test_input", 'r') as fd:
        lines = parse_input(fd.readlines())
        print(str(lines))
        s = explode(lines[0])
        print("after explosion:", str(s))


if __name__ == "__main__":
    main()
