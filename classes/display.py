import pygame as pyg
pyg.font.init()

class Colors:
    black = (25, 25, 25)
    dark_gray = (50, 50, 50)
    gray = (70, 70, 70)
    light_gray = (90, 90, 90)
    lighter_gray = (120, 120, 120)
    white = (255, 255, 255)

    green = (0, 200, 0)
    dark_green = (0, 160, 0)
    aqua = (0, 255, 255)
    blue = (0, 0, 200)
    light_blue = (0, 0, 238)
    red = (200, 0, 0)
    yellow = (255, 255, 0)
    purple = (200, 0, 200)
    tan = (210, 180, 140)

    card_colors = [red, green, yellow, blue, purple]

class Fonts:
    font_20 = pyg.font.SysFont("consolas", 20)
    font_22 = pyg.font.SysFont("consolas", 22)
    font_35 = pyg.font.SysFont("consolas", 35)