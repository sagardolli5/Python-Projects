from turtle import Turtle

class Ball(Turtle):
    """Represents the ball in the Breakout game, handling movement and bouncing logic."""

    def __init__(self):
        """Initialize the ball with its appearance and starting velocity."""
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("#FFD93D")
        self.shapesize(1.5, 1.5)
        self.sety(-234)
        self.x = -10
        self.y = 10

    def ball_move(self):
        new_x = self.xcor() + self.x
        new_y = self.ycor() + self.y
        self.goto(new_x, new_y)

    def bounce_x(self):
        self.x *= -1

    def bounce_y(self):
        self.y *= -1

    def restart_game(self, pad_x, pad_y):
        new_y = pad_y + 30
        self.sety(180)
        self.goto(pad_x, new_y)
        self.y = abs(self.y)
