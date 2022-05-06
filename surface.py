import pygame


class Surface:
    def __init__(self, x, y, width, length, color):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.color = color
        self.surf = pygame.Surface((self.width, self.length), pygame.SRCALPHA)
        self.surf.fill(color)

    def draw(self, screen):
        screen.blit(self.surf, (self.x, self.y))
