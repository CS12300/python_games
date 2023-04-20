from laserbeam import LaserBeam
from asteroid import Asteroid
from spaceship import Spaceship


class GameController:
    """
    Maintains the state of the game
    and manages interactions of game elements.
    """

    def __init__(self, SPACE, fadeout):
        """Initialize the game controller"""
        self.SPACE = SPACE
        self.fadeout = fadeout

        self.spaceship_hit = False
        self.asteroid_destroyed = False
        self.asteroids = [Asteroid(self.SPACE)]
        self.laser_beams = []
        self.spaceship = Spaceship(self.SPACE)

    def update(self):
        """Updates game state on every frame"""
        self.do_intersections()

        for asteroid in self.asteroids:
            asteroid.display()

        for l in range(len(self.laser_beams)):
            if self.laser_beams[l].lifespan > 0:
                self.laser_beams[l].display()

        self.spaceship.display()

        # Carries out necessary actions if game over
        if self.spaceship_hit:
            if self.fadeout <= 0:
                fill(1)
                textSize(30)
                text("YOU HIT AN ASTEROID",
                     self.SPACE['w']/2 - 165, self.SPACE['h']/2)
            else:
                self.fadeout -= 1

        if self.asteroid_destroyed:
            fill(1)
            textSize(30)
            text("YOU DESTROYED THE ASTEROIDS!!!",
                 self.SPACE['w']/2 - 250, self.SPACE['h']/2)

    def fire_laser(self, x, y, rot):
        """Add a laser beam to the game"""
        x_vel = sin(radians(rot))
        y_vel = -cos(radians(rot))
        self.laser_beams.append(
            LaserBeam(self.SPACE, x, y, x_vel, y_vel)
        )

    def handle_keypress(self, key, keycode=None):
        if (key == ' '):
            if self.spaceship.intact:
                self.spaceship.control(' ', self)
        if (keycode):
            if self.spaceship.intact:
                self.spaceship.control(keycode)

    def handle_keyup(self):
        if self.spaceship.intact:
            self.spaceship.control('keyup')

    def do_intersections(self):

        # between asteroids and laser beams
        if self.spaceship.intact:
            for l in range(len(self.laser_beams)):
                for i in range(len(self.asteroids)):
                    if (abs(self.laser_beams[l].x - self.asteroids[i].x)
                        < max(self.asteroids[i].radius, self.laser_beams[l].radius)
                        and
                        abs(self.laser_beams[l].y - self.asteroids[i].y)
                            < max(self.asteroids[i].radius, self.laser_beams[l].radius)):
                        end_game = self.blow_up_asteroid(i, l)
                        if end_game == True:
                            break

        # If the space ship still hasn't been blown up
        if self.spaceship.intact:
            # Check each asteroid for intersection
            for i in range(len(self.asteroids)):
                if (abs(self.spaceship.x - self.asteroids[i].x)
                    < max(self.asteroids[i].radius, self.spaceship.radius)
                    and
                    abs(self.spaceship.y - self.asteroids[i].y)
                        < max(self.asteroids[i].radius, self.spaceship.radius)):
                    # We've intersected an asteroid
                    self.spaceship.blow_up(self.fadeout)
                    self.spaceship_hit = True

    def blow_up_asteroid(self, i, j):

        if self.asteroids[i].asize == 'Large':
            del self.asteroids[i]
            self.asteroids.append(Asteroid(
                self.SPACE, 'Med', x_vel=-self.laser_beams[j].x_vel, y_vel=self.laser_beams[j].y_vel))
            self.asteroids.append(Asteroid(
                self.SPACE, 'Med', x_vel=self.laser_beams[j].x_vel, y_vel=-self.laser_beams[j].y_vel))
        elif self.asteroids[i].asize == 'Med':
            del self.asteroids[i]
            self.asteroids.append(Asteroid(
                self.SPACE, 'Small', x_vel=-self.laser_beams[j].x_vel, y_vel=self.laser_beams[j].y_vel))
            self.asteroids.append(Asteroid(
                self.SPACE, 'Small', x_vel=self.laser_beams[j].x_vel, y_vel=-self.laser_beams[j].y_vel))
            self.asteroids.append(Asteroid(self.SPACE, 'Small'))
        elif self.asteroids[i].asize == 'Small':
            del self.asteroids[i]
            if len(self.asteroids) == 0:
                self.asteroid_destroyed = True
            return True
        return False
