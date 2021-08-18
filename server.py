import draughts
import random
import socket
import tcp

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 8081))
server_socket.listen(2)
print('Server started')

client_socket = [None] * 2
order = random.sample([0, 1], 2)
for i in range(2):
    (client_socket[order[i]], _) = server_socket.accept()
    tcp.send(client_socket[order[i]], str(order[i]))
    print('Connection accepted')

state = draughts.State()
moves = state.moves()
while len(moves) > 0:
    msg = tcp.recv(client_socket[state.pl])
    tcp.send(client_socket[state.pl ^ 1], msg)
    row, col, nrow, ncol = [int(x) for x in msg.split()]
    state.play_move((row, col), (nrow, ncol))
    moves = state.moves()