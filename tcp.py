#fixed length for first message informing about length
MSG0_LEN = 6


def _send(socket, msg):
    sent = 0
    while sent < len(msg):
        sent += socket.send(msg[sent:])

def send(socket, msg):
    msg_enc = msg.encode()
    _send(socket, ((MSG0_LEN - len(str(len(msg_enc)))) * '0' + str(len(msg_enc))).encode())
    _send(socket, msg_enc)

def _recv(socket, msg_len):
    chunks = []
    recd = 0
    while recd < msg_len:
        chunks.append(socket.recv(msg_len - recd))
        recd += len(chunks[-1])
    return b''.join(chunks)

def recv(socket):
    return _recv(socket, int(_recv(socket, MSG0_LEN).decode())).decode()

