from game_controller import GameController


SIZE = {'w': 800, 'h': 800}
LIGHT = color(219, 192, 158)
DARK = color (108, 70, 26)
USER = color(0)
AI = color(234, 51, 35)
gc = GameController(LIGHT, DARK, USER, AI)

def setup():
    size(SIZE['w'], SIZE['h'])

def draw():
    gc.draw()

def mousePressed():
    gc.mouse_pressed()

def mouseReleased():
    gc.mouse_release()

