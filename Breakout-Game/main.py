import time
from turtle import Screen
from paddle import Paddle
from bricks import Bricks
from ball import Ball
from scoreboard import ScoreBoard

# ─── Game State ───────────────────────────────────────────────────────────────
is_game_on = True

# ─── Screen Setup ─────────────────────────────────────────────────────────────
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("#1A1A2E")
screen.tracer(0)

# ─── Game Object Initialization ───────────────────────────────────────────────
paddle = Paddle()
bricks = Bricks()
ball = Ball()
score_board = ScoreBoard()

bricks.create_bricks() # Generate the brick layout on screen

# ─── Keyboard Bindings ────────────────────────────────────────────────────────
screen.onkey(paddle.move_left,"Left")
screen.onkey(paddle.move_right,"Right")
screen.listen()

# ─── Main Game Loop ───────────────────────────────────────────────────────────
while is_game_on:
    time.sleep(0.1) # Control game speed
    screen.update()
    ball.ball_move()

    # ── Wall Collision (Left & Right) ─────────────────────────────────────────
    if ball.xcor() > 260 or ball.xcor() < -270:
        ball.bounce_x()

    # ── Wall Collision (Top & Bottom) ─────────────────────────────────────────
    if ball.ycor() > 275:
        ball.bounce_y()
    elif ball.ycor() < -320:
        score_board.decrease_score()
        paddle_x_cor = paddle.xcor()
        paddle_y_cor = paddle.ycor()
        ball.restart_game(paddle_x_cor, paddle_y_cor)
        score_board.update_score()

    # ── Paddle Collision ──────────────────────────────────────────────────────
    if ball.distance(paddle) < 40 and ball.ycor() > -240 and ball.y < 0:
        ball.y = abs(ball.y)

        # change a horizontal direction based on hit side
        if ball.xcor() < paddle.xcor():  # hit left side
            ball.x = -abs(ball.x)  # go left
        elif ball.xcor() > paddle.xcor():  # hit right side
            ball.x = abs(ball.x)  # go right

    # ── Brick Collision & End Conditions ──────────────────────────────────────
    if not bricks.all_bricks and score_board.life > 0:
        score_board.game_complete()
    elif score_board.life == 0:
        bricks.remove_all_bricks()
        score_board.game_over()
    else:
        for brick in bricks.all_bricks:
            if ball.distance(brick) < 45:
                score_board.increase_score()
                ball.bounce_y()
                brick.hideturtle()
                bricks.all_bricks.remove(brick)
                score_board.update_score()
                break

# ─── Keep Window Open ─────────────────────────────────────────────────────────
screen.mainloop()