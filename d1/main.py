with open('input', 'r') as fd:
    depths = [int(line.strip()) for line in fd.readlines()]
    increases = [1 for i in range(len(depths) - 1) if depths[i+1] - depths[i] > 0]
    print("Increases:", len(increases))
    
with open('input', 'r') as fd:
    depths = [int(line.strip()) for line in fd.readlines()]
    increases = [1 for i in range(len(depths) - 3) if depths[i+3] - depths[i] > 0]
    print("Increases with sliding window:", len(increases))
