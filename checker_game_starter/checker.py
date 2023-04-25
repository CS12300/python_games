

class Checkers:

    def __init__(self, x, y, square_size, color):
        self.size = square_size
        self.is_king = False
        self.x = x
        self.y = y
        self.color = color
        self.last_x = 0
        self.last_y = 0
        self.new_x = 0
        self.new_y = 0
        self.is_dragged = False
        self.has_valid_move = False
        self.has_valid_jump = False
        self.valid_move = []

    def display(self):
        """Display the checker on the board"""
        strokeWeight(2)
        if self.mouse_on() and self.has_valid_jump:
            strokeWeight(4)
        elif self.mouse_on() and not self.has_valid_jump and self.has_valid_move:
            strokeWeight(4)
        fill(self.color)
        ellipse(self.x * self.size + self.size // 2, self.y * self.size +
                self.size // 2, self.size * 0.8, self.size * 0.8)
        strokeWeight(2)
        noFill()
        stroke(255)
        ellipse(self.x * self.size + self.size // 2, self.y * self.size +
                self.size // 2, self.size * 0.6, self.size * 0.6)
        strokeWeight(0)

        if self.is_king:
            self.be_king(self.x * self.size + self.size // 2, self.y * self.size +
                         self.size // 2)

    def display_moving(self):
        """ Display the checker while mouse is moving"""
        strokeWeight(4)
        fill(self.color)
        ellipse(mouseX, mouseY, self.size * 0.8, self.size * 0.8)
        strokeWeight(2)
        noFill()
        stroke(255)
        ellipse(mouseX, mouseY, self.size * 0.6, self.size * 0.6)
        strokeWeight(0)

        # if self.is_king:
        #     self.be_king(mouseX, mouseY)

    def mouse_on(self):
        """Check if mouse is on the checker"""
        
        x = mouseX - self.x * self.size - self.size // 2
        y = mouseY - self.y * self.size - self.size // 2
        return sqrt(x ** 2 + y ** 2) < self.size * 0.5

    def be_king(self, x, y):
        """Draw a crown on top of the checker"""
        img = loadImage("crown.png")
        imageMode(CENTER)
        image(img, x, y, self.size * 0.5, self.size * 0.5)

    def move(self, x, y):
        """Move the checker to the passed in coordinates"""
        self.x = x
        self.y = y
        self.is_dragged = False