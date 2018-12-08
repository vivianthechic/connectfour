# Vivian Zhang
# ICS 32A Project 2
# Shared Functions

import connectfour

def print_board(gs: connectfour.GameState):
    game_board = gs.board
    print('')
    for col in range(1, connectfour.BOARD_COLUMNS+1):
        print(' ', col, end = '')
    print('')
    for r in range(connectfour.BOARD_ROWS):
        print(' ', end = '')
        for c in range(connectfour.BOARD_COLUMNS):
            if(game_board[c][r] == connectfour.NONE):
                print(' . ', end = '')
            elif(game_board[c][r] == connectfour.RED):
                print(' R ', end = '')
            else:
                print(' Y ', end = '')
        print('')
    print('')


def move(gs: connectfour.GameState) -> [connectfour.GameState, int, int]:
    while True:
        drop_pop = _prompt_dp()
        column_num = _prompt_col()
        print()
        try:
            if drop_pop == 0:
                gs = connectfour.drop(gs, column_num)
                return [gs, drop_pop, column_num]
            elif drop_pop == 1:
                gs = connectfour.pop(gs, column_num)
                return [gs, drop_pop, column_num]
        except ValueError:
            print('Column number is invalid. Please try again.')
            print()
        except connectfour.GameOverError:
            print('The game is over.')
            print()
        except connectfour.InvalidMoveError:
            print('That is an invalid move. Please try again.')
            print()


def _prompt_dp() -> int:
    while True:
        try:
            user_input = int(input('Enter "0" to drop your disc or "1" to pop a disc: ').strip())
            if user_input == 0 or user_input == 1:
                return user_input
            else:
                print('Your input was invalid. Please try again.')
                print()
        except ValueError:
            print('Your input was invalid. Please try again.')
            print()


def _prompt_col() -> int:
    while True:
        user_input = input('Enter a number from 1-7 to select the corresponding column: ').strip()
        if(user_input.isdigit()):
            return int(user_input)-1
        else:
            print('Your input was invalid. Please try again.')
            print()

