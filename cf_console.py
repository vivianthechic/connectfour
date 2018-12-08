# Vivian Zhang
# ICS 32A Project 2
# Console Version

import connectfour
import cf_functions

def _run_interface():
    game_state = connectfour.new_game()
    while True:
        cf_functions.print_board(game_state)
        gs_dp_col = cf_functions.move(game_state)
        game_state = gs_dp_col[0]
        win = connectfour.winner(game_state)
        if win == connectfour.RED:
            print('Player R has won the game.')
            break
        elif win == connectfour.YELLOW:
            print('Player Y has won the game.')
            break

if __name__ == '__main__':
    _run_interface()
