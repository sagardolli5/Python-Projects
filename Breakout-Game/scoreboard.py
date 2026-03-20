from turtle import Turtle

class ScoreBoard:
    """Manages and displays the player's score and remaining lives on screen."""
    def __init__(self):
        """Initialize score and life counters, and set up their display turtles."""
        self.score = 0
        self.life = 3
        self.user_score = Turtle()
        self.user_score.color("white")
        self.user_score.penup()
        self.user_score.hideturtle()
        self.user_score.goto(-150, 250)

        self.user_life = Turtle()
        self.user_life.color("white")
        self.user_life.penup()
        self.user_life.hideturtle()
        self.user_life.goto(150, 250)

        self.update_life()
        self.update_score()

    def update_score(self):
        self.user_score.clear()
        self.user_score.write(f"Score: {self.score}", align="center", font=("Arial", 20, "normal"))

    def update_life(self):
        self.user_life.clear()
        self.user_life.write(f"Life: {self.life}", align="center", font=("Arial", 20, "normal"))

    def increase_score(self):
        self.score += 1
        self.update_score()

    def decrease_score(self):
        self.life -= 1
        self.score -= 1
        self.update_score()
        self.update_life()

    def game_complete(self):
        self.user_life.hideturtle()
        self.user_score.goto(0, 0)
        self.user_score.write(f"You Won!", align="center", font=("Courier", 24, "normal"))

    def game_over(self):
        self.user_life.hideturtle()
        self.user_score.goto(0, 0)
        self.user_score.write(f"Game Over!", align="center", font=("Courier", 24, "normal"))