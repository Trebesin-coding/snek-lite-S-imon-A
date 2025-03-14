import pygame
from settings import FRAMERATE, SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_SPEED

class Player:
    def __init__(self, spawn_x: int, spawn_y: int, scale: int):
        self.x = spawn_x
        self.y = spawn_y
        self.vel_x = 0
        self.vel_y = 0
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.score = 0
        self.win = False

        self.set_scale(scale)

    def set_scale(self, scale: int) -> None:
        self.image = pygame.transform.scale_by(pygame.image.load("images/player.png"), scale)
        self.rect = self.image.get_rect()

    def update_position(self) -> None:
        self.x += self.vel_x * SNAKE_SPEED * (60 / FRAMERATE)
        self.y += self.vel_y * SNAKE_SPEED * (60 / FRAMERATE)

    def check_position(self) -> None:
        if self.x < self.rect.width/2:
            self.x = SCREEN_WIDTH - self.rect.width/2
        elif self.x > SCREEN_WIDTH - self.rect.width/2:
            self.x = self.rect.width/2

        if self.y < self.rect.height/2:
            self.y = SCREEN_HEIGHT - self.rect.height/2
        elif self.y > SCREEN_HEIGHT - self.rect.height/2:
            self.y = self.rect.height/2

    def render(self, screen: pygame.display) -> None:
        if not self.win:
            self.update_position()
            self.check_position()

        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)