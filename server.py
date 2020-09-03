import draughts
import random
import socket
import tcp

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('192.168.0.136', 55822))
server_socket.listen(2)
print('Server started')

client_socket = [None] * 2
for i in range(2):
    (client_socket[i], _) = server_socket.accept()
    print('Connection accepted')
for i in range(2):
    tcp.send(client_socket[i], str(i))

state = draughts.State()
moves = state.moves()
while len(moves) > 0:
    msg = tcp.recv(client_socket[state.pl])
    tcp.send(client_socket[state.pl ^ 1], msg)
    row, col, nrow, ncol = [int(x) for x in msg.split()]
    state.play_move((row, col), (nrow, ncol))
    moves = state.moves()