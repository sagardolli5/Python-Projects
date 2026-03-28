import pygame

class Player:

    def __init__(self):
        self.player_speed, self.player_life, self.bullet_speed = 0.5, 2, 2
        self.bullet, self.bullet_fired = None, False
        # ── CURRENT POSITION ─────────────────────────────────────────────────────────
        self.x, self.y = 350, 450
        # ── PLAYER IMAGE ─────────────────────────────────────────────────────
        self.player_img = pygame.image.load("img/plane.png")
        self.player_img = pygame.transform.scale(self.player_img, (60, 60))
        # ── REMAINING PLAYER IMAGE POSITION ─────────────────────────────────────────────────────
        self.life_positions = [(100, 525), (170, 525), (240, 525)]

    def fire_bullet(self):
        if not self.bullet_fired:
            self.bullet = {
                "x": self.x + 30,
                "y1": self.y - 25,
                "y2": self.y - 5
            }
            self.bullet_fired = True

    def move_left(self):
        if self.x >= 90:
            self.x -= self.player_speed

    def move_right(self):
        if self.x <= 650:
            self.x += self.player_speed

    def update_bullet(self, screen):
        if self.bullet_fired and self.bullet:
            self.bullet["y1"] -= self.bullet_speed
            self.bullet["y2"] -= self.bullet_speed

            pygame.draw.line(screen, (32, 255, 32), (self.bullet["x"], self.bullet["y1"]),
                             (self.bullet["x"], self.bullet["y2"]), 3)

            if self.bullet["y2"] < 0:   # off screen, reset
                self.bullet = None
                self.bullet_fired = False

    def draw(self, screen):
        if self.player_life >= 0:
            screen.blit(self.player_img, (self.x, self.y))
        # life icons
        for i, pos in enumerate(self.life_positions):
            if i < self.player_life:
                screen.blit(self.player_img, pos)

    def handle_input(self, keys, screen):
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        if keys[pygame.K_SPACE]:
            self.fire_bullet()

