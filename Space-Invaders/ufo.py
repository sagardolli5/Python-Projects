import random
import pygame

class Ufo:

    def __init__(self):
        # ── UFO POSITION ─────────────────────────────
        self.ufo_position = []
        self.initial_x, self.initial_y = 105, 60
        self.drop_amount = 20
        for i in range(12):
            self.ufo_position.append([self.initial_x, self.initial_y])
            self.initial_x += 105
            if (i + 1) % 6 == 0:
                self.initial_x = 105
                self.initial_y += 80


        self.ufo_speed, self.laser_speed = 0.5, 2
        self.laser_beam = None

        # ── UFO IMAGE ──────────────────────────────────────────────────
        self.ufo_img = pygame.image.load("img/ufo.png")
        self.ufo_img = pygame.transform.scale(self.ufo_img, (60, 60))


    def fire_laser(self):
        # randomly pick a UFO to shoot from
        shooter = random.choice(self.ufo_position)
        self.laser_beam = {
            "ufo_x": shooter[0] + 30,
            "ufo_y1": shooter[1] + 60,
            "ufo_y2": shooter[1] + 75
        }

    def move(self):
        if not self.ufo_position:  # ← skip if a list is empty
            return

        # move all UFOs horizontally
        for ufo in self.ufo_position:
            ufo[0] += self.ufo_speed

        # go left + drop down
        if self.ufo_position[0][0] < 0:
            self.ufo_speed = 0.1
            for ufo in self.ufo_position:
                ufo[1] += 10
        #go right
        if self.ufo_position[-1][0] > 740:
            self.ufo_speed = -0.5

    def update_laser(self, screen):
        if self.laser_beam is None:
            self.fire_laser()

        if self.laser_beam is not None:
            self.laser_beam["ufo_y1"] += self.laser_speed
            self.laser_beam["ufo_y2"] += self.laser_speed

            pygame.draw.line(screen, (32, 255, 32), (self.laser_beam["ufo_x"], self.laser_beam["ufo_y1"]),
                             (self.laser_beam["ufo_x"], self.laser_beam["ufo_y2"]), 3)

            # Remove laser if off-screen
            if self.laser_beam is not None and self.laser_beam["ufo_y2"] > 600:
                self.laser_beam = None

    def draw(self, screen):
        for ufo in self.ufo_position:
            screen.blit(self.ufo_img, (ufo[0], ufo[1]))

    def check_bullet_collision(self, bullet):
        for ufo in self.ufo_position:
            if ufo[0] < bullet["x"] < ufo[0] + 60 and ufo[1] < bullet["y2"] < ufo[1] + 60:
                self.ufo_position.remove(ufo)  # destroy UFO
                return True  # tell player bullet is gone
        return False

    def check_laser_collision(self, player):
        if self.laser_beam is not None:
            if (player.x < self.laser_beam["ufo_x"] < player.x + 60 and
                    player.y < self.laser_beam["ufo_y1"] < player.y + 60):
                self.laser_beam = None  # destroy laser
                return True  # tell player they got hit
        return False