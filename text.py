import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Text:
    def __init__(self, font: pygame.font.Font, content: str, color: tuple[int, int, int], x: int, y: int):
        self.font = font
        self.content = content
        self.color = color
        self.surface = self.font.render(self.content, True, self.color)
        self.rect = self.surface.get_rect()
        self.x = x
        self.y = y
        self.dynamic_position = False
        self.anchor_corner = ""
        self.anchor_margin = 0

        self.rect.center = (self.x, self.y)
    
    def update_content(self, new_content: str) -> None:
        self.surface = self.font.render(new_content, True, self.color)
        self.rect = self.surface.get_rect()

        if self.dynamic_position:
            self.calc_dynamic_corner_position()

    def enable_dynamic_corner_position(self, corner: str, margin: int) -> None:
        """
        corner: top-left; top-right; bottom-left; bottom-right
        """
        self.dynamic_position = True
        self.anchor_corner = corner
        self.anchor_margin = margin

        self.calc_dynamic_corner_position()

    def calc_dynamic_corner_position(self) -> None:
        match self.anchor_corner:
            case "top-left":
                self.x, self.y = self.rect.width/2 + self.anchor_margin, self.rect.height/2 + self.anchor_margin
            case "top-right":
                self.x, self.y = SCREEN_WIDTH - self.rect.width/2 - self.anchor_margin, self.rect.height/2 + self.anchor_margin
            case "bottom-left":
                self.x, self.y = self.rect.width/2 + self.anchor_margin, SCREEN_HEIGHT - self.rect.height/2 - self.anchor_margin
            case "bottom-right":
                self.x, self.y = SCREEN_WIDTH - self.rect.width/2 - self.anchor_margin, SCREEN_HEIGHT - self.rect.height/2 - self.anchor_margin
            case _:
                self.x, self.y = 0, 0
        
        self.rect.center = (self.x, self.y)

    def render(self, screen: pygame.display) -> None:
        screen.blit(self.surface, self.rect)

def handle_texts(texts: list[Text], screen: pygame.display) -> None:
    for text in texts:
        text.render(screen)