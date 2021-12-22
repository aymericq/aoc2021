class Packet:
    def __init__(self, version, type_id, length, subpackets=None, value=None):
        self.version = version
        self.type_id = type_id
        self.length = length
        self.subpackets = subpackets
        self.value = value


def pad_bin(bin_str):
    return '0' * (4 - len(bin_str)) + bin_str


def add_version_number(packet):
    if packet.subpackets is not None:
        s = packet.version
        for subpacket in packet.subpackets:
            s += add_version_number(subpacket)
        return s
    else:
        return packet.version


def evaluate(packet: Packet) -> float:
    if packet.type_id == 0:
        return sum(evaluate(subpacket) for subpacket in packet.subpackets)
    if packet.type_id == 1:
        acc = 1
        for subpacket in packet.subpackets:
            acc *= evaluate(subpacket)
        return acc
    if packet.type_id == 2:
        return min(evaluate(subpacket) for subpacket in packet.subpackets)
    if packet.type_id == 3:
        return max(evaluate(subpacket) for subpacket in packet.subpackets)
    if packet.type_id == 4:
        return packet.value
    if packet.type_id == 5:
        return 1 if evaluate(packet.subpackets[0]) > evaluate(packet.subpackets[1]) else 0
    if packet.type_id == 6:
        return 1 if evaluate(packet.subpackets[0]) < evaluate(packet.subpackets[1]) else 0
    if packet.type_id == 7:
        return 1 if evaluate(packet.subpackets[0]) == evaluate(packet.subpackets[1]) else 0


def parse_packet(binary_input):
    print("~~~~~~~~ NEW PACKET ~~~~~~~~")
    version = int(binary_input[:3], base=2)
    type_id = int(binary_input[3:6], base=2)
    print("Version:", version, ", type id:", type_id)
    if type_id == 4:
        # Literal packet
        return parse_litteral_packet(binary_input, type_id, version)
    else:
        # Operator packet(s)
        return parse_operator_packet(binary_input, type_id, version)


def parse_operator_packet(binary_input, type_id, version) -> Packet:
    cursor = 6
    if binary_input[cursor] == '0':
        # Next 15 bits indicate total length
        cursor += 1
        length_of_subpackets = int(binary_input[cursor:cursor + 15], base=2)
        cursor += 15
        print("Length of subpackets is:", length_of_subpackets)
        offset = 0
        packets = []
        while offset < length_of_subpackets:
            new_packet = parse_packet(binary_input[cursor + offset:])
            packets.append(new_packet)
            offset += new_packet.length
            print("Offset is at:", offset)
        cursor += offset
        return Packet(version, type_id, cursor, subpackets=packets)
    else:
        # Next 11 bits indicate number of packets
        cursor += 1
        nb_of_subpackets = int(binary_input[cursor:cursor + 11], base=2)
        cursor += 11
        print("# of subpackets is:", nb_of_subpackets)
        packets = []
        for i_packet in range(nb_of_subpackets):
            new_packet = parse_packet(binary_input[cursor:])
            packets.append(new_packet)
            offset = new_packet.length
            cursor += offset
        return Packet(version, type_id, cursor, subpackets=packets)


def parse_litteral_packet(binary_input, type_id, version) -> Packet:
    print("Packet is a literal")
    cursor = 6
    literal = ""
    while binary_input[cursor] == "1":
        curr_group = binary_input[cursor: cursor + 5]
        literal += curr_group[1:]
        cursor += 5
    curr_group = binary_input[cursor: cursor + 5]
    literal += curr_group[1:]
    cursor += 5
    print("Literal bin val is:", literal)
    value = int(literal, base=2)
    print("Literal val is:", int(literal, base=2))
    return Packet(version, type_id, cursor, value=value)


def main():
    with open('input', 'r') as fd:
        binary_input = "".join([pad_bin(bin(int(char, base=16))[2:]) for char in fd.readline().strip()])
        print(binary_input)
        packet = parse_packet(binary_input)
        s = 0
        s += add_version_number(packet)
        print("Sum of versions is:", s)
        value = evaluate(packet)
        print("Packet evaluates to:", value)


if __name__ == "__main__":
    main()
