import pygame as pg
import draughts

COLORS = [(255, 238, 194), (192, 178, 145)]
CIRCLE_COLOR = tuple([x * 6 // 7 for x in COLORS[1]])
SZ = 64

def screen_to_grid(pos):
    return (7 - pos[1] // SZ, pos[0] // SZ)

def grid_to_screen(pos):
    return (pos[1] * SZ, (7 - pos[0]) * SZ)

def draw_sprite(screen, sprite, pos):
    screen.blit(sprite, grid_to_screen(pos))

def draw_tile(screen, pos):
    screen_pos = grid_to_screen(pos)
    pg.draw.rect(screen, COLORS[(pos[1] ^ (7 - pos[0])) & 1], pg.Rect(screen_pos, (SZ, SZ)))

def draw_circle(screen, pos):
    screen_pos = grid_to_screen(pos)
    pg.draw.circle(screen, CIRCLE_COLOR, (screen_pos[0] + SZ // 2, screen_pos[1] + SZ // 2), 8)

if __name__=="__main__":
    pg.init()
    logo = pg.image.load("sprites/11.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("czech-draughts")
    screen = pg.display.set_mode((SZ * 8, SZ * 8))
    running = True
    chess_sprites = [[None for _ in range(2)] for _ in range(2)]
    for i in range(2):
        for j in range(2):
            chess_sprites[i][j] = pg.image.load("sprites/" + str(i) + str(j) + ".png").convert_alpha()
    clock = pg.time.Clock()
    state = draughts.State()
    moves = state.moves()
    focused = None
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    focused = None
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = screen_to_grid(pg.mouse.get_pos())
                if focused in moves and pos in moves[focused]:
                    state.play_move(focused, pos)
                    moves = state.moves()
                focused = pos
        for i in range(8):
            for j in range(8):
                draw_tile(screen, (i, j))
        for i in range(8):
            for j in range(8):
                if state.color((i, j)) != draughts.NONE:
                    draw_sprite(screen, chess_sprites[state.color((i, j))][state.rank((i, j))], (i, j))
                elif focused in moves and (i, j) in moves[focused]:
                    draw_circle(screen, (i, j))
        pg.display.update()
        clock.tick()
        