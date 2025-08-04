import random


def get_number():
    numbers = [i for i in range(16)]

    def draw_number():
        nonlocal numbers

        if len(numbers) > 0:
            index = random.randint(0, len(numbers)-1)

            drawed_number = numbers[index]
            numbers.pop(index)
            return drawed_number
    return draw_number


def print_board(board):
    for row in board:
        print('\t'.join('' if item == 0 else f"[{item}]" for item in row))
    print('\n'+'-'*30)


def update_board(board, action):
    def find_index_empty() -> tuple[int, int]:
        for row in range(len(board)-1):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    return col, row
        else:
            return -1, -1

    def move_up():
        x, y = find_index_empty()
        if y < len(board)-1:
            board[y][x], board[y+1][x] = board[y+1][x], board[y][x]

    def move_down():
        x, y = find_index_empty()
        if y > 0:
            board[y][x], board[y-1][x] = board[y-1][x], board[y][x]

    def move_left():
        x, y = find_index_empty()
        if x < len(board[y])-1:
            board[y][x], board[y][x+1] = board[y][x+1], board[y][x]

    def move_right():
        x, y = find_index_empty()
        if x > 0:
            board[y][x], board[y][x-1] = board[y][x-1], board[y][x]

    if action == "w":
        move_up()
    elif action == "s":
        move_down()
    elif action == "a":
        move_left()
    elif action == "d":
        move_right()
    return


def play_15_puzzle():
    draw_number = get_number()

    board_solved = [[(i+4*j) for i in range(4)] for j in range(4)]
    play_board = [[draw_number() for _ in range(4)] for _ in range(4)]

    print("Slide tiles (numbers) to match this configuration:")
    print_board(board_solved)

    while True:
        print_board(play_board)
        print('\tW\nA\t\tD\n\tS\nq - Quit\n')
        user_input = input().lower()
        print(user_input)

        if user_input in ['q']:
            break
        if user_input in ['w', 's', 'a', 'd']:
            update_board(play_board, user_input)

        if play_board == board_solved:
            print("You win!")
            break
