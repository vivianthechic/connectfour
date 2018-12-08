# Vivian Zhang
# ICS 32A Project 2
# Networked Version

import connectfour
import cf_functions
import cf_sockethandling


def _get_host() -> str:
    while True:
        h = input('Enter a hostname or an IP address: ').strip()
        if h == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return h

    
def _get_port() -> int:
    while True:
        try:
            p = int(input('Enter a port: ').strip())
            if p < 0 or p > 65535:
                print('Ports must be an integer between 0 and 65535')
            else:
                return p
        except ValueError:
            print('Ports must be an integer between 0 and 65535')


def _get_user() -> str:
    while True:
        name = input('Enter your username (no white spaces): ')
        if len(name) == 0:
            print('Your input was blank. Please try again.')
        else:
            no_spaces = True
            for i in name:
                if i == ' ':
                    no_spaces = False
            if no_spaces:
                return name
            else:
                print('Your username contains white spaces. Please try again.')


def _move_for_server(s_move: str, gs: connectfour.GameState) -> connectfour.GameState:
    col = int(s_move[-1])-1
    if s_move.startswith('DROP'):
        gs = connectfour.drop(gs, col)
        return gs
    else:
        gs = connectfour.pop(gs, col)
        return gs


def _run_interface():
    host = _get_host()
    port = _get_port()
    username = _get_user()
    try:
        connection = cf_sockethandling.connect(host, port)
        try:
            welcome = cf_sockethandling.hello(connection, username)
            print()
            print(welcome)
            ready = cf_sockethandling.request_game(connection)
            game_state = connectfour.new_game()
            while True:
                cf_functions.print_board(game_state)
                gs_dp_col = cf_functions.move(game_state)
                game_state = gs_dp_col[0]
                cf_sockethandling.send_move(connection, gs_dp_col[1], gs_dp_col[2])
                win = connectfour.winner(game_state)
                if win == connectfour.RED:
                    print('Player R has won')
                server_move = cf_sockethandling.receive_move(connection)
                if server_move == 'INVALID':
                    print('Move is invalid.')
                elif server_move.startswith('WINNER'):
                    break
                else:
                    print('Y\'s move: ' + server_move)
                    print()
                    game_state = _move_for_server(server_move, game_state)
                    win = connectfour.winner(game_state)
                    if win == connectfour.YELLOW:
                        print('Player Y has won')
                        break
        except cf_sockethandling.I32CFSPError:
            print('Input does not conform to protocol.')
        finally:
            cf_sockethandling.close(connection)
    except ConnectionRefusedError:
        print('Connection was unsuccessful.')


if __name__ == '__main__':
    _run_interface()
