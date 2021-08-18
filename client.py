import pygame as pg
import draughts
import socket
import tcp
import threading

COLORS = [(255, 238, 194), (192, 178, 145)]
CIRCLE_COLOR = tuple([x * 6 // 7 for x in COLORS[1]])
SZ = 64
pl = 0

def screen_to_grid(pos):
    return (7 - pos[1] // SZ, pos[0] // SZ) if pl == 0 else (pos[1] // SZ, 7 - pos[0] // SZ)

def grid_to_screen(pos):
    return (pos[1] * SZ, (7 - pos[0]) * SZ) if pl == 0 else ((7 - pos[1]) * SZ, pos[0] * SZ)

def draw_sprite(screen, sprite, pos):
    screen.blit(sprite, grid_to_screen(pos))

def fill_tile(screen, pos):
    screen_pos = grid_to_screen(pos)
    pg.draw.rect(screen, COLORS[(pos[1] ^ (7 - pos[0])) & 1], pg.Rect(screen_pos, (SZ, SZ)))

def draw_tile(screen, pos):
    screen_pos = grid_to_screen(pos)
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(screen_pos, (SZ, SZ)), 1)

def draw_circle(screen, pos):
    screen_pos = grid_to_screen(pos)
    pg.draw.circle(screen, CIRCLE_COLOR, (screen_pos[0] + SZ // 2, screen_pos[1] + SZ // 2), 8)

class UpdateThread(threading.Thread):
    def __init__(self, client_socket, state):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.state = state
        self.moved = pg.mixer.Sound('sounds/moved.wav')

    def run(self):
        while True:
            msg = tcp.recv(self.client_socket)
            self.moved.play()
            row, col, nrow, ncol = [int(x) for x in msg.split()]
            self.state.play_move((row, col), (nrow, ncol))


if __name__=="__main__":
    pg.init()
    logo = pg.image.load("sprites/11.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("czech-draughts")
    screen = pg.display.set_mode((SZ * 8, SZ * 8))
    chess_sprites = [[None for _ in range(2)] for _ in range(2)]
    for i in range(2):
        for j in range(2):
            chess_sprites[i][j] = pg.image.load("sprites/" + str(i) + str(j) + ".png").convert_alpha()
    clock = pg.time.Clock()
    state = draughts.State()
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('45.79.93.163', 8081))
    pl = int(tcp.recv(client_socket))

    updater = UpdateThread(client_socket, state)
    updater.start()

    fcs = None
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                client_socket.close()
                exit(0)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    fcs = None
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = screen_to_grid(pg.mouse.get_pos())
                if state.pl == pl:
                    if fcs in state.moves() and pos in state.moves()[fcs]:
                        tcp.send(client_socket, ' '.join([str(x) for x in [fcs[0], fcs[1], pos[0], pos[1]]]))
                        state.play_move(fcs, pos)
                    fcs = pos if state.pl == pl else None
        for row in range(8):
            for col in range(8):
                pos = (row, col)
                fill_tile(screen, pos)
                if pos in state.last_move:
                    draw_tile(screen, pos)
                if state.color(pos) != draughts.NONE:
                    draw_sprite(screen, chess_sprites[state.color(pos)][state.rank(pos)], pos)
                elif fcs in state.moves() and pos in state.moves()[fcs]:
                    draw_circle(screen, pos)
        pg.display.update()
        clock.tick()