from checker import Checkers


class Board:
    def __init__(self, square_size, square_num, dark_color, light_color):
        self.board = []
        self.size = square_size
        self.num = square_num
        self.dark_color = dark_color
        self.light_color = light_color


    def set_up(self):
        """Draw the board for the checker game"""
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                x, y = i * self.size, j * self.size
                fill(self.dark_color if (i + j) % 2 == 0 else self.light_color)
                # draw square
                square(x, y, self.size)
                
                
