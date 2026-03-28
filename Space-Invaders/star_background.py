import random
import pygame

class StarBackground:

    def __init__(self):
        self.stars = []
        self.star_speed = 0.1
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            self.stars.append([x, y])


    def gen_star(self, screen):
        for star in self.stars:
            star[1] += self.star_speed
            if star[1] > 600:
                star[0] = random.randint(0, 800)
                star[1] = 0
            pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), 2)