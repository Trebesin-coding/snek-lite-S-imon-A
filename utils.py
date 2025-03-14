import pygame
import math

def distance(rect_0: pygame.rect.Rect, rect_1: pygame.rect.Rect) -> float:
    position_0: tuple[int, int] = rect_0.center
    position_1: tuple[int, int] = rect_1.center

    x_distance: int = abs(position_0[0] - position_1[0])
    y_distance: int = abs(position_0[1] - position_1[1])

    distance: float = math.sqrt(math.pow(x_distance, 2) + math.pow(y_distance, 2))

    return distance

def abbreviate_number(number: int) -> str:
    reverse_number_string: str = str(number)[::-1]
    abbr_string: str = ""

    i: int = 0
    for l in reverse_number_string:
        abbr_string += l

        if i >= 2:
            i = -1
            abbr_string += "," 

        i += 1
    
    final_string: str = abbr_string[::-1]

    if final_string[0] == ",":
        final_string = final_string[1:]

    return final_string