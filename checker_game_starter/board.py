from checker import Checkers


class Board:
    def __init__(self, square_size, square_num, dark_color, light_color, user_color, ai_color):
        self.board = [[0] * square_num for _ in range(square_num)]
        self.size = square_size
        self.num = square_num
        self.dark_color = dark_color
        self.light_color = light_color
        self.user_color = user_color
        self.ai_color = ai_color
        self.initialize()

    def set_up(self):
        """Draw the board for the checker game"""
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                x, y = i * self.size, j * self.size
                fill(self.dark_color if (i + j) % 2 == 0 else self.light_color)
                # draw square
                square(x, y, self.size)

    def initialize(self):
        """initialize the board with checkers"""
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if y < 3 and (x % 2 == 0 and y % 2 != 0 or x % 2 != 0 and y % 2 == 0):
                    self.board[x][y] = Checkers(x, y, 100, self.ai_color)
                if y >= 5 and (x % 2 == 0 and y % 2 != 0 or x % 2 != 0 and y % 2 == 0):
                    self.board[x][y] = Checkers(x, y, 100, self.user_color)

    def mouse_pressed(self):
        """Handle mouse pressed event"""
        for row in self.board:
            for checker in row:
                if checker != 0 and checker.mouse_on() and checker.has_valid_move:
                    # start dragging the checker
                    # remember the original position of the checker
                    checker.last_x, checker.last_y = checker.x, checker.y
                    checker.is_dragged = True

    def mouse_release(self):
        """Handle mouse released event"""
        # calculate the new position where mouse released
        for row in self.board:
            for checker in row:
                if checker != 0 and checker.is_dragged:
                    checker.is_dragged = False
                    checker.new_x, checker.new_y = int(
                        mouseX / self.size), int(mouseY / self.size)
                    # check if new position is valid for current checker
                    if 0 <= checker.new_x < len(self.board) and 0 <= checker.new_y < len(self.board):
                        self.move(checker)

    def move(self, checker):
        """Move the checker"""
        # move 1 step
        dx, dy = abs(checker.new_x -
                     checker.last_x), abs(checker.new_y - checker.last_y)
        if dx == 1 and dy == 1:
            if checker.is_king:
                pass
            elif checker.color == self.user_color:
                for i, j in [(-1, -1), (1, -1)]:
                    if checker.last_x + i == checker.new_x and checker.last_y + j == checker.new_y and self.board[checker.new_x][checker.new_y] == 0:
                        checker.move(checker.new_x, checker.new_y)
                        self.update_board(checker)
            elif checker.color == self.ai_color:
                for i, j in [(-1, 1), (1, 1)]:
                    if checker.last_x + i == checker.new_x and checker.last_y + j == checker.new_y and self.board[checker.new_x][checker.new_y] == 0:
                        checker.move(checker.new_x, checker.new_y)
                        self.update_board(checker)
        elif dx == 2 and dy == 2:
            if self.check_jump(checker, checker.new_x, checker.new_y):
                checker.move(checker.new_x, checker.new_y)
                return self.update_board(checker, jump=True)

    def update_board(self, checker, jump=False):
        if jump:
            jumped_x, jumped_y = (
                checker.last_x + checker.new_x) // 2, (checker.last_y + checker.new_y) // 2
            self.board[jumped_x][jumped_y] = 0
        self.board[checker.last_x][checker.last_y] = 0
        self.board[checker.x][checker.y] = checker

    def check_jump(self, checker, new_x, new_y):
        # check boundaries
        if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board):
            if self.board[new_x][new_y] == 0:
                jumped_x = (checker.x + new_x) // 2
                jumped_y = (checker.y + new_y) // 2
                if self.board[jumped_x][jumped_y] != 0 and self.board[jumped_x][jumped_y].color != checker.color:
                    return True
        return False

    def has_valid_move(self, checker):
        """Check before mouse_released if the selected checkers have valid moves"""
        if checker.is_king:
            for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                new_x = checker.x + i
                new_y = checker.y + j
                if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board):
                    if self.board[new_x][new_y] == 0:
                        return True
                    elif self.board[new_x][new_y] != 0:
                        self.check_jump(checker, new_x + i, new_y + j)
                        return True
        elif checker.color == self.user_color:
            for i, j in [(-1, -1), (1, -1)]:
                new_x, new_y = checker.x + i, checker.y + j
                if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board):
                    if self.board[new_x][new_y] == 0:
                        return True
                    elif self.check_jump(checker, new_x + i, new_y + j):
                        return True
        elif checker.color == self.ai_color:
            print("HI")
            for i, j in [(1, 1), (-1, 1)]:
                print("x, y = ", checker.x, checker.y)
                print("i, j =", i, j)
                new_x = checker.x + i
                new_y = checker.y + j
                print("new_x, new_y = ", new_x, new_y)
                if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board):
                    if self.board[new_x][new_y] == 0:
                        return True
                    elif self.check_jump(checker, new_x + i, new_y + j):
                        return True
        return False
