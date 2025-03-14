from __future__ import annotations
import pygame
import random
from settings import FRAMERATE, SCREEN_WIDTH, SCREEN_HEIGHT, RED_COIN_SCORE, GREEN_COIN_SCORE, GOLD_COIN_SCORE
from player import Player
from utils import distance

class Coin:
    def __init__(self, image_url: str, scale: int, coin_type: str, max_duration: int, can_teleport: bool):
        self.x = 0
        self.y = 0
        self.image_url = image_url
        self.image = pygame.image.load(image_url)
        self.rect = self.image.get_rect()
        self.coin_type = coin_type
        self.can_teleport = can_teleport
        self.duration = 0
        self.max_duration = max_duration
        self.score_given = False

        self.set_scale(scale)
    
    def set_random_screen_position(self, player: Player, coins: list[Coin], side_margin: int = 0) -> None:
        position_found: bool = False

        i: int = 0
        while not position_found:
            new_x: int = random.randint(self.rect.width/2 + side_margin, SCREEN_WIDTH - self.rect.width/2 - side_margin)
            new_y: int = random.randint(self.rect.height/2 + side_margin, SCREEN_HEIGHT - self.rect.height/2 - side_margin)
            new_rect: pygame.rect.Rect = pygame.rect.Rect((0, 0), (16, 16))
            new_rect.center = (new_x, new_y)

            dist: float = distance(player.rect, new_rect)

            collision: bool = False
            for coin in coins:
                coin_collision: bool = coin.rect.colliderect(new_rect)

                if coin_collision:
                    collision = True

            if dist > player.rect.width * 5 and not collision:
                position_found = True
                self.x = new_x
                self.y = new_y
                self.rect.center = (self.x, self.y)
                self.score_given = False
            
            i += 1
            if i > 1000:
                del self

                break

    def set_scale(self, scale: int) -> None:
        self.image = pygame.transform.scale_by(pygame.image.load(self.image_url), scale)
        self.rect = self.image.get_rect()
    
    def give_score(self, player: Player) -> None:
        if self.score_given:
            return
        
        self.score_given = True

        match self.coin_type:
            case "red":
                player.score += RED_COIN_SCORE
            case "green":
                player.score += GREEN_COIN_SCORE
            case "gold":
                player.score += GOLD_COIN_SCORE
                player.win = True
            case _:
                player.score += 1

    def player_collision(self, player: Player, coins: list[Coin]) -> bool:
        self.give_score(player)

        if self.can_teleport:
            self.set_random_screen_position(player, coins, 16)
            return False

        return True

    def render(self, screen: pygame.display) -> None:
        self.duration += 1/FRAMERATE
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

def handle_coins(coins: list[Coin], player: Player, screen: pygame.display) -> None:
    coins_to_remove: list[Coin] = []

    for coin in coins:
        if coin.rect.colliderect(player.rect):
            destroy: bool = coin.player_collision(player, coins)

            if not destroy:
                continue

            coins_to_remove.append(coin)
        
        if coin.duration >= coin.max_duration and coin.max_duration != -1:
            coins_to_remove.append(coin)

        coin.render(screen)
    
    for coin_to_remove in coins_to_remove:
        if coin_to_remove in coins:
            coins.remove(coin_to_remove)
            del coin_to_remove