NONE = -1
WHITE = 0
BLACK = 1
PAWN = 0
QUEEN = 1

QUEEN_DIRS = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
PAWN_DIRS = [
    [(1, -1), (1, 1)],
    [(-1, -1), (-1, 1)]
]

def in_bounds(pos):
    return pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8

def add_tuples(a, b):
    return tuple([x + y for x, y in zip(a, b)])

def sub_tuples(a, b):
    return tuple([x - y for x, y in zip(a, b)])

def div_tuple(a, b):
    return tuple([x // b for x in a])

class State:
    def __init__(self):
        self.board = [
            ['p', '.', 'p', '.', 'p', '.', 'p', '.'],
            ['.', 'p', '.', 'p', '.', 'p', '.', 'p'],
            ['p', '.', 'p', '.', 'p', '.', 'p', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'P', '.', 'P', '.', 'P', '.', 'P'],
            ['P', '.', 'P', '.', 'P', '.', 'P', '.'],
            ['.', 'P', '.', 'P', '.', 'P', '.', 'P'],
        ]
        self.pl = 0
        self.must_take = None
        self.last_move = (None, None)

    def color(self, pos):
        if self.board[pos[0]][pos[1]] == '.':
            return NONE
        return WHITE if self.board[pos[0]][pos[1]][0].islower() else BLACK

    def rank(self, pos):
        if self.board[pos[0]][pos[1]] == '.':
            return -1
        return PAWN if self.board[pos[0]][pos[1]][0].lower() == 'p' else QUEEN

    def jumped(self, pos):
        if len(self.board[pos[0]][pos[1]]) < 2:
            return False
        return self.board[pos[0]][pos[1]][1] == '#'

    def queen_takes(self):
        move_dict = dict()
        for row in range(8):
            for col in range(8):
                pos = (row, col)
                if self.must_take != None and pos != self.must_take:
                    continue
                if self.color(pos) == self.pl and self.rank(pos) == QUEEN:
                    for d in QUEEN_DIRS:
                        ipos = add_tuples(pos, d)
                        while in_bounds(ipos) and self.color(ipos) == NONE:
                            ipos = add_tuples(ipos, d)
                        if not in_bounds(ipos) or self.color(ipos) == self.pl or self.jumped(ipos):
                            continue
                        ipos = add_tuples(ipos, d)
                        while in_bounds(ipos) and self.color(ipos) == NONE:
                            if pos not in move_dict:
                                move_dict[pos] = []
                            move_dict[pos].append(ipos)
                            ipos = add_tuples(ipos, d)
        return move_dict

    def pawn_takes(self):
        move_dict = dict()
        for row in range(8):
            for col in range(8):
                pos = (row, col)
                if self.must_take != None and pos != self.must_take:
                    continue
                if self.color(pos) == self.pl and self.rank(pos) == PAWN:
                    for d in PAWN_DIRS[self.pl]:
                        ipos = add_tuples(pos, d)
                        if not in_bounds(ipos) or self.color(ipos) != self.pl ^ 1 or self.jumped(ipos):
                            continue
                        ipos = add_tuples(ipos, d)
                        if in_bounds(ipos) and self.color(ipos) == NONE:
                            if pos not in move_dict:
                                move_dict[pos] = []
                            move_dict[pos].append(ipos)
        return move_dict

    # returns dict[pos] = [ pos ]
    def moves(self):
        move_dict = self.queen_takes()
        if len(move_dict) > 0:
            return move_dict
        move_dict = self.pawn_takes()
        if len(move_dict) > 0:
            return move_dict
        move_dict = dict()
        if self.must_take != None:
            return move_dict
        for row in range(8):
            for col in range(8):
                pos = (row, col)
                if self.color(pos) == self.pl:
                    if self.rank(pos) == PAWN:
                        for d in PAWN_DIRS[self.pl]:
                            ipos = add_tuples(pos, d)
                            if in_bounds(ipos) and self.color(ipos) == NONE:
                                if pos not in move_dict:
                                    move_dict[pos] = []
                                move_dict[pos].append(ipos)
                    else:
                        for d in QUEEN_DIRS:
                            ipos = add_tuples(pos, d)
                            while in_bounds(ipos) and self.color(ipos) == NONE:
                                if pos not in move_dict:
                                    move_dict[pos] = []
                                move_dict[pos].append(ipos)
                                ipos = add_tuples(ipos, d)
        return move_dict

    
    def play_move(self, pos, npos):
        d = sub_tuples(npos, pos)
        d = div_tuple(d, abs(d[0]))
        ipos = add_tuples(pos, d)
        taken = None
        while ipos != npos:
            if self.color(ipos) == self.pl ^ 1:
                taken = ipos
            ipos = add_tuples(ipos, d)
        self.board[pos[0]][pos[1]], self.board[npos[0]][npos[1]] = self.board[npos[0]][npos[1]], self.board[pos[0]][pos[1]]
        self.last_move = (pos, npos)
        if taken != None:
            self.board[taken[0]][taken[1]] += '#'
            self.must_take = npos
            take_dict = self.moves()
            if len(take_dict) == 0:
                self.next_turn()
        else:
            self.next_turn()

    def next_turn(self):
        for row in range(8):
            for col in range(8):
                if len(self.board[row][col]) > 1:
                    self.board[row][col] = '.'
                if self.board[row][col] == 'p' and row == 7:
                    self.board[row][col] = 'q'
                if self.board[row][col] == 'P' and row == 0:
                    self.board[row][col] = 'Q'
        self.must_take = None
        self.pl ^= 1