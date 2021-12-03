def forward(amount, aim, pos):
    pos[0] += amount
    pos[1] += aim*amount
    return aim

def down(amount, aim, pos):
    aim += amount
    return aim

def up(amount, aim, pos):
    aim -= amount
    return aim

with open('input', 'r') as fd:
    decoder = {'forward': forward, 'down': down, 'up': up}
    pos = [0,0]
    aim = 0
    instructions = fd.readlines()
    for instruction in instructions:
        fct_name, amnt_str = instruction.split(' ')
        fct = decoder[fct_name]
        amnt = int(amnt_str)
        aim = fct(amnt, aim, pos)

    print("Pos:", pos, ", mult:", pos[0]*pos[1])