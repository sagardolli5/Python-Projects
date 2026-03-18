from turtle import Turtle

MOVE_DISTANCE = 10

class Paddle(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(1, 5)
        self.sety(-260)

    def move_left(self):
        if self.xcor() >= -235:
            self.backward(MOVE_DISTANCE)


    def move_right(self):
        if self.xcor() <= 220:
            self.forward(MOVE_DISTANCE)