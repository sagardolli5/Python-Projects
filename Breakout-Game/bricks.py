from turtle import Turtle
import random
COLORS = ["#FF4757", "#FF6B35", "#FFD93D", "#6BCB77", "#4D96FF", "#C77DFF"]

BRICK_UNIT = 20  # 1 turtle unit = 20px
GAP = 5

class Bricks:
    """Manages the creation, tracking, and removal of all bricks in the game."""

    def __init__(self):
        """Initialize the brick manager with an empty brick list and a starting Y position."""
        self.all_bricks = []
        self.all_coordinates = []
        self.y_cor = 220

    def create_bricks(self):
        """
        Recursively generate rows of randomly sized bricks across the screen.

        Each brick is assigned a random width (1–5 units) and color. Bricks are
        placed left to right until the row is full, then the method recurses to
        fill the next row downward — stopping when y_cor reaches 0 (screen centers).
        """

        left_edge = -290
        stop_point = 260

        while left_edge < stop_point:
            stretch_len = random.randint(1, 5)
            brick_width = stretch_len * BRICK_UNIT

            center_x = left_edge + brick_width / 2  # place from a center

            brick = Turtle("square")
            brick.color(random.choice(COLORS))
            brick.penup()
            brick.shapesize(stretch_wid=1, stretch_len=stretch_len)
            brick.setpos(center_x, self.y_cor)
            self.all_bricks.append(brick)

            left_edge += brick_width + GAP  # move to the next brick's left edge

        if self.y_cor > 0:
            self.y_cor -= 30
            self.create_bricks()

    def remove_all_bricks(self):
        for brick in self.all_bricks:
            brick.hideturtle()
        self.all_bricks.clear()