import time
from board import Board
from player import Player
from ai import Ai

SIZE = 100


class GameController:
    def __init__(self, light, dark, user_color, ai_color):
        self.b = Board(100, 8, light, dark)
        self.board = self.b.board
        self.player = Player(self.board, user_color)
        self.ai = Ai(self.board, ai_color)
        self.ai_color = ai_color
        self.game_over = False
        self.player_turn = True
        self.has_jump = False
        self.PAUSE_TIME = 0.7
        self.last_move_time = 0.0
        self.game_over = False
        self.record = False

    def start_game(self):
        self.player.initialize()
        self.ai.initialize()

    def update(self):
        self.b.set_up()
        if self.has_jump and not self.player.jump_exist():
            self.has_jump = False
            self.player.valid_jump = None

        # if player side has a valid jump
        for c in self.board:
            if self.player.has_valid_jump(c):
                self.has_jump = True
                # self.player.only_jump(c)
                if c.is_dragged:
                    c.display_moving()
                else:
                    c.display()
            else:
                c.display()

        if not self.has_jump:
            self.b.set_up()
            for c in self.board:
                if self.player.has_valid_move(c):
                    c.has_valid_move = True
                    if c.is_dragged:
                        c.display_moving()
                    else:
                        c.display()
                else:
                    c.has_valid_move = False
                    c.display()

    def mouse_pressed(self):
        if self.player_turn:
            # if there is valid jump, others cannot be dragged
            if self.has_jump:
                for c in self.board:
                    if c.mouse_on() and self.player.has_valid_jump(c):

                        c.is_dragged = True
                        c.last_x, c.last_y = c.x, c.y
            else:
                for c in self.board:
                    if c.mouse_on() and self.player.has_valid_move(c):
                        c.is_dragged = True
                        c.last_x, c.last_y = c.x, c.y

    def mouse_released(self):
        if self.player_turn:
            for c in self.board:
                # only the checkers that has_valid_move or has_valid_jump can go through
                if c.is_dragged:
                    c.is_dragged = False
                    c.new_x, c.new_y = int(mouseX / SIZE), int(mouseY / SIZE)
                    self.player_move(c)

    def player_move(self, c):
        if self.has_jump:
            if c.is_king:
                for i, j in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                    if (c.x + i == c.new_x and c.y + j == c.new_y) and self.player.find_checker(c.new_x, c.new_y) == -1:
                        jumped_x, jumped_y = (
                            c.x + c.new_x) // 2, (c.y + c.new_y) // 2
                        jumped = self.player.find_checker(jumped_x, jumped_y)
                        if jumped != -1 and jumped.color != c.color:
                            c.move(c.new_x, c.new_y)
                            self.player.eat_checker(jumped)
                            self.has_jump = False
                            self.player_turn = False
                            self.last_move_time = time.time()
            else:
                for i, j in [(-2, -2), (2, -2)]:
                    if (c.x + i == c.new_x and c.y + j == c.new_y) and self.player.find_checker(c.new_x, c.new_y) == -1:
                        jumped_x, jumped_y = (
                            c.x + c.new_x) // 2, (c.y + c.new_y) // 2
                        jumped = self.player.find_checker(jumped_x, jumped_y)
                        if jumped != -1 and jumped.color != c.color:
                            c.move(c.new_x, c.new_y)
                            self.player.eat_checker(jumped)
                            self.has_jump = False
                            self.player_turn = False
                            self.last_move_time = time.time()
        else:    
            dx, dy = abs(c.new_x - c.last_x), abs(c.new_y - c.last_y)
            if dx == 1 and dy == 1:
                if c.is_king:
                    for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        if c.last_x + i == c.new_x and c.last_y + j == c.new_y and self.player.find_checker(c.new_x, c.new_y) == -1:
                            c.move(c.new_x, c.new_y)
                            self.last_move_time = time.time()
                            self.player_turn = False
                        
                for i, j in [(-1, -1), (1, -1)]:
                    if c.last_x + i == c.new_x and c.last_y + j == c.new_y and self.player.find_checker(c.new_x, c.new_y) == -1:
                        c.move(c.new_x, c.new_y)
                        self.last_move_time = time.time()
                        self.player_turn = False

    def ai_move(self):
        if not self.player_turn:
            for c in self.board:
                if self.ai.has_valid_jump(c):
                    self.ai.move(c, jump=True)
                    self.player_turn = True
                    return
            for c in self.board:
                if self.ai.has_valid_move(c):
                    self.ai.move(c)
                    self.player_turn = True
                    return

    def display_end_game(self):
        TEXT_SIZE = 120
        if self.game_over == "lose":
            message = "Red wins!"
        elif self.game_over == "win":
            message = "Black wins!"
        elif self.game_over == "draw":
            message = "Draw!"

        CENTER = self.b.size * self.b.size // 2
        OFFSET = 3
        textSize(TEXT_SIZE)
        textAlign(CENTER, CENTER)
        fill(0)
        text(message, CENTER+OFFSET, CENTER+OFFSET)
        fill(225)
        text(message, CENTER, CENTER)
        self.record_winner()

    def record_winner(self):
        if not self.record and self.game_over == "win":
            ranking = {}
            try:
                file = open("score.txt", "r+")
            except OSError as e:
                print("Cannot open score.txt")

            for line in file:
                if line == "\n":
                    continue
                line = line.split()
                name = line[0]
                score = int(line[1])
                ranking[name] = score

            winner = self.input("Enter name: ")
            ranking[winner] = ranking.get(winner, 0) + 1
            ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
            file.seek(0)
            
            for name, score in ranking:
                file.write(name + " " + str(score) + "\n")
        self.record = True
        

    def input(self, message=''):
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)
