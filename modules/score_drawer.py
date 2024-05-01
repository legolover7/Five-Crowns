import pygame as pyg

from classes.display import Colors, Fonts
from classes.globals import Globals

def draw_score(window, position, size, details):
    x, y = position
    width, height = size

    # Background
    pyg.draw.rect(window, Colors.tan, (x, y, width, height), border_radius=8)
    window.blit(Fonts.font_20.render("Scorecard", True, Colors.black), (x + 4, y + 4))

    # Draw outlines/rounds
    vertical_position = y + 100
    spacing = 4
    margin = 40
    for i in range(3, 14):
        text_width, text_height = Fonts.font_20.size("AA")
        window.blit(Fonts.font_20.render((" " if i < 10 else "") + str(i), True, Colors.black), (x + margin, vertical_position))
        pyg.draw.rect(window, Colors.black, (x + 4, vertical_position + text_height, width-8, 2))
        pyg.draw.rect(window, Colors.black, (x + 4, vertical_position - spacing, width-8, 2))
        
        vertical_position += text_height + (text_height if (i - 2) % 3 == 0 else 0) + spacing

    # Side bars
    pyg.draw.rect(window, Colors.black, (x + margin + 5 + text_width, y + 75 - spacing, 2, vertical_position - y - 50))
    pyg.draw.rect(window, Colors.black, (x + 4, y + 75 - spacing, 2, vertical_position - y - 50))
    # Text
    text_width = Fonts.font_20.size("Round")[0]
    window.blit(Fonts.font_20.render("Round", True, Colors.black), (x + 8, y + 75))
    window.blit(Fonts.font_20.render("Total", True, Colors.black), (x + 8, y + vertical_position - 20))
    # Top/bottom bars
    pyg.draw.rect(window, Colors.black, (x + 4, y + 75 - spacing, width - 8, 2))
    pyg.draw.rect(window, Colors.black, (x + 4, y + vertical_position, width - 8, 2))

    horizontal_position = x + 30 + text_width


    # Loop through players and their scores
    for k in range(len(details)):
        player = details[k]
        window.blit(Fonts.font_20.render("P" + str(k + 1), True, Colors.black), (horizontal_position, y + 75))
        
        horizontal_position += Fonts.font_20.size("P")[0]

        vertical_position = y + 100
        for j in range(len(player["scores"])):
            text_width, text_height = Fonts.font_20.size("A")
            score = str(player["scores"][j])
            margin = -(text_width * (len(score) - 1))

            color = Colors.black if score != "0" else Colors.dark_green
            window.blit(Fonts.font_20.render(score, True, color), (horizontal_position + margin, vertical_position))

            vertical_position += text_height + spacing
        pyg.draw.rect(window, Colors.black, (horizontal_position + 15, y + 71, 2, 375))

        # Highlight current player
        if k == Globals.player_turn:
            pyg.draw.rect(window, Colors.dark_green, (horizontal_position - 29, y + 96, 47, 2))
            pyg.draw.rect(window, Colors.dark_green, (horizontal_position - 28, y + 71, 46, 2))
            pyg.draw.rect(window, Colors.dark_green, (horizontal_position - 29, y + 71, 2, 25))
            pyg.draw.rect(window, Colors.dark_green, (horizontal_position + 15, y + 71, 2, 25))

        horizontal_position += Fonts.font_20.size("P1 ")[0]
        