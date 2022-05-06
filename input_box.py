import pygame
import os

class InputBox:
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32)) -> None:
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color(0, 0, 255)
        self.color_active = pygame.Color(255, 0, 0)
        self.color = self.color_inactive
        self.active = False
        self.text = "10"
        self.done = False
        self.font = pygame.font.Font("font/times.ttf", 60)

    def dealEvent(self, event: pygame.event.Event, screen):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(self.boxBody.collidepoint(event.pos)):
                self.active = not self.active
                # if not self.active and len(self.text) == 0:
                #     self.text = "10"
                #     self.draw(screen)
            else:
                self.active = False
                if len(self.text) == 0 or int(self.text) == 0:
                    self.text = "10"
                    self.draw(screen)
            self.color = self.color_active if(
                self.active) else self.color_inactive
        if(event.type == pygame.KEYDOWN):
            if(self.active):
                if(event.key == pygame.K_RETURN):
                    print(self.text)
                    # self.text=''
                elif(event.key == pygame.K_BACKSPACE):
                    self.text = self.text[:-1]
                elif len(self.text) <= 3 and event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        txtSurface = self.font.render(
            self.text, True, self.color)
        # width = max(250, txtSurface.get_width()+10)
        width = 130
        self.boxBody.w = width
        screen.blit(txtSurface, (self.boxBody.x+5, self.boxBody.y+5))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)