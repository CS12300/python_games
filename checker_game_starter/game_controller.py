from board import Board


class GameController:
    def __init__(self, light, dark, user_color, ai_color):
        self.b = Board(100, 8, light, dark, user_color, ai_color)
        self.members = [[0 for x in range(8)]]

    def draw(self):
        self.b.set_up()
        for row in self.b.board:
            for elem in row:
                if elem != 0:
                    if self.b.has_valid_move(elem):
                        elem.has_valid_move = True
                        if elem.is_dragged:
                            elem.display_moving()
                        else:
                            elem.display()
                    else:
                        elem.has_valid_move = False
                        elem.display()

    def mouse_pressed(self):
        self.b.mouse_pressed()

    def mouse_release(self):
        self.b.mouse_release()
