import pygame
import random
from sys import exit
from settings import FRAMERATE, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN_COIN_INTERVAL, GREEN_COIN_DURATION, GOLD_COIN_MIN_INTERVAL, GOLD_COIN_MAX_INTERVAL, GOLD_COIN_DURATION
from player import Player
from coin import Coin, handle_coins
from text import Text, handle_texts
from utils import abbreviate_number

player: Player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 3)

def key_down_event(event: pygame.event.Event) -> None:
    global player

    match event.key:
        case pygame.K_a | pygame.K_LEFT:
            if player.vel_x != 1:
                player.vel_x, player.vel_y = -1, 0
        case pygame.K_d | pygame.K_RIGHT:
            if player.vel_x != -1:
                player.vel_x, player.vel_y = 1, 0
        case pygame.K_w | pygame.K_UP:
            if player.vel_y != 1:
                player.vel_x, player.vel_y = 0, -1
        case pygame.K_s | pygame.K_DOWN:
            if player.vel_y != -1:
                player.vel_x, player.vel_y = 0, 1

def handle_events() -> None:
    events: list[pygame.event.Event] = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            key_down_event(event)

def main() -> None:
    global player

    pygame.init()
    pygame.display.set_caption("SnekLite")

    screen: pygame.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True
    coins: list[Coin] = []
    texts: list[Text] = []

    red_coin: Coin = Coin("images/coin_red.png", 2, "red", -1, True)
    red_coin.set_random_screen_position(player, coins, 16)
    coins.append(red_coin)
    green_coin_timer: int = 0
    gold_coin_timer: int = 0
    gold_coin_time: int = random.randint(GOLD_COIN_MIN_INTERVAL, GOLD_COIN_MAX_INTERVAL)

    score_text: Text = Text(pygame.font.SysFont("arial", 20), "SCORE: 0", (255, 255, 255), 0, 0)
    score_text.enable_dynamic_corner_position("top-right", 25)
    texts.append(score_text)
    win_text: Text = Text(pygame.font.SysFont("arial", 60), "Victory!", (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    while running:
        handle_events()

        screen.fill((47, 47, 47))

        player.render(screen)
        handle_coins(coins, player, screen)
        handle_texts(texts, screen)
        
        if player.win:
            win_text.render(screen)

        pygame.display.flip()

        if not player.win:
            green_coin_timer += 1/FRAMERATE
            gold_coin_timer += 1/FRAMERATE

            if green_coin_timer >= GREEN_COIN_INTERVAL:
                green_coin_timer = 0
            
                green_coin: Coin = Coin("images/coin_green.png", 2, "green", GREEN_COIN_DURATION, False)
                green_coin.set_random_screen_position(player, coins, 16)
                coins.append(green_coin)
        
            if gold_coin_timer >= gold_coin_time and gold_coin_timer < 100:
                gold_coin_timer = 100

                gold_coin: Coin = Coin("images/coin_gold.png", 2, "gold", GOLD_COIN_DURATION, False)
                gold_coin.set_random_screen_position(player, coins, 16)
                coins.append(gold_coin)
        
        score_text.update_content(f'SCORE: {abbreviate_number(player.score)}')

        clock.tick(FRAMERATE)

if __name__ == "__main__":
    main()