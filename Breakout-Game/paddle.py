from turtle import Turtle

MOVE_DISTANCE = 15

class Paddle(Turtle):
    """Represents the player-controlled paddle at the bottom of the screen."""
    def __init__(self):
        """Initialize the paddle with its appearance and fixed vertical position."""
        super().__init__()
        self.penup()
        self.shape("square")
        self.color("#FFFFFF")
        self.shapesize(1, 5)
        self.sety(-260)

    def move_left(self):
        if self.xcor() >= -235:
            self.backward(MOVE_DISTANCE)


    def move_right(self):
        if self.xcor() <= 220:
            self.forward(MOVE_DISTANCE)