import pygame
from star_background import StarBackground
from player import Player
from ufo import Ufo

pygame.init()
screen = pygame.display.set_mode((800, 600))

star_background = StarBackground()
player = Player()
ufo = Ufo()

def restart():
    global game_over, player, ufo
    player = Player()
    ufo = Ufo()
    game_over = False

font = pygame.font.SysFont("ocraextended", 40)
score = 0
game_over = False
running = True
while running:
    # ── BACKGROUND ───────────────────────────────────────────────────────────
    screen.fill((19, 36, 64))

    # ── TITLE TEXT ───────────────────────────────────────────────────────────
    if not game_over:
        text = font.render(f"Space Invaders  |  Score: {score}", True, (32, 255, 32))
        screen.blit(text, (220, 20))

    # ── STARS ────────────────────────────────────────────────────────────────
    star_background.gen_star(screen)

    # ── DIVIDER LINE ─────────────────────────────────────────────────────────
    pygame.draw.line(screen, (32, 255, 32), (100, 520), (700, 520), 3)

    # ── PLAYER MOVEMENT AND BULLET FIRING ───────────────────────────────────────────────────────────────
    keys = pygame.key.get_pressed()
    player.handle_input(keys, screen)
    player.update_bullet(screen)
    player.draw(screen)

    if player.bullet_fired and player.bullet:
        if ufo.check_bullet_collision(player.bullet):
            player.bullet = None
            player.bullet_fired = False
            score += 10

    # ── MOVE UFOs ────────────────────────────────────────────────────────────
    ufo.move()
    ufo.update_laser(screen)
    ufo.draw(screen)

    if ufo.check_laser_collision(player):
        player.player_life -= 1
        ufo.laser_beam = None # force reset so it can't hit the same frame
        if player.player_life <= -1:
            game_over = True

    if game_over:
        game_over_text = font.render(f"Game Over! | Score: {score}", True, (32, 255, 32))
        x = 800 // 2 - game_over_text.get_width() // 2
        y = 600 // 2 - game_over_text.get_height() // 2
        screen.blit(game_over_text, (x, y))

        # restart text below it
        restart_text = font.render("Press R to Play Again", True, (255, 255, 255))
        rx = 800 // 2 - restart_text.get_width() // 2
        screen.blit(restart_text, (rx, y + 60))

    # ── regenerate UFOs when all destroyed ───────────────────────────────────
    if len(ufo.ufo_position) == 0:
        ufo.ufo_position = []
        initial_x, initial_y = 105, 60
        for i in range(12):
            ufo.ufo_position.append([initial_x, initial_y])
            initial_x += 105
            if (i + 1) % 6 == 0:
                initial_x = 105
                initial_y += 80

        ufo.ufo_speed += 0.3  # faster left/right
        ufo.drop_amount += 5  # faster drop down

    # ── EVENTS ───────────────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart()

    # ── UPDATE SCREEN ────────────────────────────────────────────────────────
    pygame.display.update()