from game_controller import GameController
import time

SIZE = {'w': 800, 'h': 800}
LIGHT = color(219, 192, 158)
DARK = color(108, 70, 26)
USER = color(0)
AI = color(234, 51, 35)
gc = GameController(LIGHT, DARK, USER, AI)
AI_TIME_DELAY = 0.7

def setup():
    size(SIZE['w'], SIZE['h'])
    gc.start_game()

def draw():
    gc.update()
    if time.time() >= gc.last_move_time + AI_TIME_DELAY:
        gc.ai_move()

def mousePressed():
    gc.mouse_pressed()

def mouseReleased():
    gc.mouse_released()
