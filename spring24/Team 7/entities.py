import random

from collision import *
from shapes import *
from textures import *

####################################
########### CONSTANTS ###############

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 650
RIBBON_HEIGHT = 40


class Player:
    FRAME_UPDATE_INTERVAL = 20
    EMPOWERED_DURATION = 500  # 500 frames * 20ms = 10 seconds
    TIME_SINCE_GHOST = 50  # 1 second

    def __init__(self, x: int, y: int, size: int, speed: int):
        """Initialize a new player."""
        self.x_pos = x
        self.y_pos = y
        self.prev_x = x
        self.prev_y = y
        self.length = size
        self.speed = speed
        self.rect = Rectangle(x, y, size, size)
        self.direction = "Moving Right"
        self.requested_direction = self.direction
        self.texture_ids = [1, 2]
        self.frame_counter = 0
        self.can_move = False
        self.empowered = False
        self.empowered_timer = 0
        self.eaten_ghost = False
        self.eaten_ghost_timer = 0

    def get_texture_ids(self) -> list:
        """Return the texture IDs for the player."""

        if self.direction == "Moving Right":
            return [1, 2]
        if self.direction == "Moving Left":
            return [3, 4]
        if self.direction == "Moving Up":
            return [5, 6]
        if self.direction == "Moving Down":
            return [7, 8]

    def clone(self) -> "Player":
        """Create a copy of the player."""
        return Player(self.x_pos, self.y_pos, self.length, self.speed)

    def teleport(self, x: int, y: int):
        """Move the player to a new position instantly."""
        self.x_pos = x
        self.y_pos = y
        self.rect = Rectangle(x, y, self.length, self.length)

    def end_frame(self):
        """Update the player's state at the end of a frame."""
        self.frame_counter += 1
        if self.frame_counter >= self.FRAME_UPDATE_INTERVAL:
            self.prev_x = self.x_pos
            self.prev_y = self.y_pos
            self.frame_counter = 0

        if self.empowered:
            self.empowered_timer += 1
            if self.empowered_timer >= self.EMPOWERED_DURATION:
                self.empowered = False
                self.empowered_timer = 0

        # Feature : freeze after eating a ghost
        # if self.eaten_ghost:

        #     if self.eaten_ghost_timer >= self.TIME_SINCE_GHOST:
        #         self.eaten_ghost = False
        #         self.eaten_ghost_timer = 0
        #         self.can_move = True
        #     else:
        #         self.can_move = False

        #     self.eaten_ghost_timer += 1

    @property
    def is_moving(self) -> bool:
        """Check if the player is moving."""
        return self.x_pos != self.prev_x or self.y_pos != self.prev_y


class Fruit:
    def __init__(self, x, y, size, type):
        self.x_pos = x
        self.y_pos = y
        self.size = size
        self.type = type
        self.rect = Rectangle(x, y, size, size)


class Wall:
    def __init__(self, x, y, length, width):
        self.rect = Rectangle(x, y, length, width)
        self.color = (1, 1, 1)

    def draw(self):
        glColor(self.color)
        self.rect.draw()
        glColor(1, 1, 1)
