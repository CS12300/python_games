from game_behavior import GameBehavior
from checker import Checkers

SIZE = 8


class Ai(GameBehavior):
    def __init__(self, board, color):
        GameBehavior.__init__(self, board, color)
        self.valid_move = []
        self.valid_jump = None
        self.jump = []
        self.before_jump = None

    def initialize(self):
        """initialize the board with checkers"""
        for x in range(SIZE):
            for y in range(SIZE):
                if y < 3 and (x % 2 == 0 and y % 2 != 0 or x % 2 != 0 and y % 2 == 0):
                    self.add_checker(Checkers(x, y, 100, self.color))

    def has_valid_move(self, checker):
        if checker.color == self.color:
            for i, j in [(1, 1), (-1, 1)]:
                new_x, new_y = checker.x + i, checker.y + j
                if 0 <= new_x < SIZE and 0 <= new_y < SIZE:
                    if self.find_checker(new_x, new_y) == -1:
                        checker.has_valid_move = True
                        self.valid_move.append(new_x)
                        self.valid_move.append(new_y)
                        return True
        checker.has_valid_move = False
        return False

    def has_valid_jump(self, c):
        if c.color == self.color:
            for i, j in [(2, 2), (-2, 2)]:
                new_x, new_y = c.x + i, c.y + j
                if 0 <= new_x < SIZE and 0 <= new_y < SIZE and self.find_checker(new_x, new_y) == -1:
                    jumped_x, jumped_y = (c.x + new_x) // 2, (c.y + new_y) // 2
                    jumped = self.find_checker(jumped_x, jumped_y)
                    if jumped != -1 and jumped.color != c.color:
                        self.valid_jump = jumped
                        c.has_valid_jump = True
                        self.jump.append(new_x)
                        self.jump.append(new_y)
                        self.before_jump = c
                        return True
        c.has_valid_jump = False
        self.before_jump = None
        return False


    def move(self, checker, jump=False):
        if jump and self.jump_exist():
            checker.move(self.jump[0], self.jump[1])
            self.eat_checker(self.valid_jump)
            self.valid_jump = None
            self.jump = []
            self.before_jump = None
        else:
            checker.move(self.valid_move[0], self.valid_move[1])
            self.valid_move = []

    def jump_exist(self):
        for c in self.board:
            if c == self.before_jump:
                return True
        return False