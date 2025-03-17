import random

from collision import is_colliding_walls
from shapes import Rectangle


class Ghost:
    ghost_textures = {"yellow": [0, 1], "red": [2, 3], "blue": [4, 5], "pink": [6, 7]}
    MOVE_TO_TARGET = 1
    MOVE_TO_START = -1
    direction_stack = []

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        speed: int,
        ghost_color: str,
        nearby_blocks: list,
    ):
        self.x_pos = x
        self.y_pos = y
        self.length = size
        self.speed = speed
        self.nearby_blocks = nearby_blocks
        self.rect = Rectangle(x, y, size, size)
        self.state = self.MOVE_TO_TARGET
        self.direction = random.choice(self.nearby_blocks)
        self.texture_ids = self.ghost_textures[ghost_color]

    def clone(self) -> "Ghost":
        """Create a copy of the ghost."""
        return Ghost(
            self.x_pos,
            self.y_pos,
            self.length,
            self.speed,
            self.start,
            self.target,
            self.ghost_color,
        )

    def teleport(self, x: int, y: int):
        """Move the ghost to a new position instantly."""
        self.x_pos = x
        self.y_pos = y
        self.rect = Rectangle(x, y, self.length, self.length)

    def change_direction(self):
        direction = random.choice(self.nearby_blocks)

        while len(self.direction_stack) > 2 and direction == self.direction_stack[-2]:
            direction = random.choice(self.nearby_blocks)

        self.direction_stack.append(direction)

        self.direction = direction

    def move_to_block(self, block, walls):
        """Move the ghost to a specific block."""
        new_x = self.x_pos
        new_y = self.y_pos

        if self.x_pos < block[0]:
            new_x += self.speed
        elif self.x_pos > block[0]:
            new_x -= self.speed

        if self.y_pos < block[1]:
            new_y += self.speed
        elif self.y_pos > block[1]:
            new_y -= self.speed

        if is_colliding_walls(self, walls):
            self.change_direction()
            return

        else:
            self.teleport(new_x, new_y)

            if block == (new_x, new_y):
                self.change_direction()

    def move_randomly(self, walls):
        position = (self.x_pos, self.y_pos)

        if not (self.x_pos == self.direction[0] or self.y_pos == self.direction[1]):
            self.change_direction()
            return

        self.move_to_block(self.direction, walls)
