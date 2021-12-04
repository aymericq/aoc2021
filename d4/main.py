def load_boards(lines):
    boards = []
    curr_board = []
    for line in lines:
        if len(line.strip()) == 0:
            boards.append(curr_board)
            curr_board = []
        else:
            line = [line[i:i+2].strip() for i in range(0, 13, 3)]
            curr_board.append(line)
    boards.append(curr_board)
    return boards

def mark_board_and_check_victory(marked_boards, i_board, x_board, y_board):
    marked_boards[i_board][x_board][y_board] = 1
    winner_board_x = True
    for x_check in range(5):
        if marked_boards[i_board][x_check][y_board] == 0:
            winner_board_x = False
            break
    winner_board_y = True
    for y_check in range(5):
        if marked_boards[i_board][x_board][y_check] == 0:
            winner_board_y = False
            break
    return winner_board_x or winner_board_y

def prepare_marked_boards(n_boards):
    marked_boards = []
    for i_board in range(n_boards):
        lines = []
        for y_board in range(5):
            line = []
            for x_board in range(5):
                line.append(0)
            lines.append(line)
        marked_boards.append(lines)
    return marked_boards

def mark_boards_and_check_victory(boards, marked_boards, number):
    winning_boards = []
    for i_board, board in enumerate(boards):
        for x_board in range(5):
            for y_board in range(5):
                if board[x_board][y_board] == number:
                    winner_board = mark_board_and_check_victory(marked_boards, i_board, x_board, y_board)
                    if winner_board:
                        winning_boards.append(i_board)
    return winning_boards

def pretty_print_board(board):
    line_to_print = ""
    for line in board:
        line_to_print = ""
        for n in line:
            n = str(n)
            if len(n) == 1:
                line_to_print += " " + n
            else:
                line_to_print += n
            line_to_print += " "
        print(line_to_print)

def sum_of_unmarked_numbers(board, marked_board):
    s = 0
    for i in range(5):
        for j in range(5):
            if marked_board[i][j] == 0:
                s += int(board[i][j])
    return s

with open('input', 'r') as fd:
    draw = fd.readline().strip().split(',')
    fd.readline()
    boards = load_boards(fd.readlines())

    print("Board 1 is:")
    pretty_print_board(boards[1])
    print("~~~~~")
    n_boards = len(boards)
    marked_boards = prepare_marked_boards(n_boards)

    winning_boards = []

    for i_number, number in enumerate(draw):
        winning_boards_at_turn_i = mark_boards_and_check_victory(boards, marked_boards, number)
        new_winning_boards = []
        for winning_board_i in winning_boards_at_turn_i:
            if winning_board_i not in winning_boards:
                new_winning_boards.append(winning_board_i)
        if len(new_winning_boards) != 0:
            for i_board in new_winning_boards:
                print("Number", number, "was drawn.")
                print("At turn", i_number, ", Board", i_board, "wins !")
                print("~ ~ ~ ~ ~ ~ ~ ~")
                pretty_print_board(marked_boards[i_board])
                print("~ ~ ~ ~ ~ ~ ~ ~")
                s = sum_of_unmarked_numbers(boards[i_board], marked_boards[i_board])
                print("Sum of unmarked numbers is:", s)
                print("Score is:", s*int(number))
            winning_boards.extend(new_winning_boards)