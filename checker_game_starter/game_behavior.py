class GameBehavior:

    def __init__(self, board, color):
        self.board = board
        self.color = color

    def add_checker(self, checker):
        self.board.append(checker)

    def eat_checker(self, checker):
        for c in self.board:
            if c == checker:
                self.board.remove(c)
                return

    def find_checker(self, x, y):
        for c in self.board:
            if c.x == x and c.y == y:
                return c
        return -1

    # let all others has no valid move
    def only_jump(self, checker):
        for c in self.board:
            if c != checker and c.color == checker.color:
                c.has_valid_move = False

