# Vivian Zhang
# ICS 32A Project 2
# Socket Handling

import socket
from collections import namedtuple

CFConnection = namedtuple('CFConnection',['cf_socket','cf_input','cf_output'])

_SHOW_DEBUG_TRACE = False

class I32CFSPError(Exception):
    pass


def connect(host: str, port: int) -> CFConnection:
    game_socket = socket.socket()
    game_socket.connect((host, port))
    game_input = game_socket.makefile('r')
    game_output = game_socket.makefile('w')
    return CFConnection(game_socket, game_input, game_output)


def hello(connection: CFConnection, user: str) -> str:
    _write(connection, 'I32CFSP_HELLO ' + user)
    response = _read(connection)
    if response.startswith('WELCOME'):
        return response
    else:
        raise I32CFSPError()


def request_game(connection: CFConnection) -> str:
    _write(connection, 'AI_GAME')
    response = _read(connection)
    if response == 'READY':
        return response
    else:
        raise I32CFSPError()

def send_move(connection: CFConnection, dp: int, column: int) -> None:
    if dp == 0:
        line = 'DROP '
    else:
        line = 'POP '
    line = line + str(column+1)
    _write(connection, line)

def receive_move(connection: CFConnection) -> str:
    response = _read(connection)
    if response == 'OKAY':
        move = _read(connection)
        ready = _read(connection)
        return move
    elif response == 'INVALID':
        ready = _read(connection)
        return response
    elif response.startswith('WINNER'):
        return response
    else:
        raise I32CFSPError()

def _write(connection: CFConnection, line: str) -> None:
    connection.cf_output.write(line + '\r\n')
    connection.cf_output.flush()


def _read(connection: CFConnection) -> str:
    line = connection.cf_input.readline()[:-1]
    if _SHOW_DEBUG_TRACE:
        print(line)
    return line


def close(connection: CFConnection) -> None:
    connection.cf_input.close()
    connection.cf_output.close()
    connection.cf_socket.close()
