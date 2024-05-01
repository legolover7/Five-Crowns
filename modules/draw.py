import pygame as pyg
pyg.init()
pyg.font.init()

from classes.card import Card
from classes.display import Colors, Fonts
from classes.globals import Globals
import modules.collider as collider
import modules.score_drawer as sd

def draw(hand, check_button, pass_play_button, saved_sets, discarded, player_details):
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    VID_BUFFER.fill(Colors.black)

    if not discarded or Globals.went_out:
        hand.draw(VID_BUFFER)

    for set in saved_sets:
        set.draw(VID_BUFFER)

    draw_piles(VID_BUFFER)

    draw_info(VID_BUFFER, hand)

    if discarded and not Globals.went_out:
        pass_play_button.draw()
    else:
        check_button.draw()

    sd.draw_score(VID_BUFFER, (Globals.WIDTH-400, 20), (380, 500), player_details)

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 

def draw_info(window, hand):
    
    text_width, text_height = Fonts.font_35.size("Player " + str(Globals.player_turn + 1) + "'s turn")
    window.blit(Fonts.font_35.render("Player " + str(Globals.player_turn + 1) + "'s turn", True, Colors.aqua), (Globals.WIDTH/2 - text_width/2, 75))

    text_width, text_height = Fonts.font_22.size("Current round: " + str(Globals.current_round))
    window.blit(Fonts.font_22.render("Current round: " + str(Globals.current_round), True, Colors.white), (Globals.WIDTH/2 - text_width/2, Globals.HEIGHT/2 + 75 - text_height/2))

    text_width, text_height = Fonts.font_22.size("Size of your hand: " + str(len(hand.cards)))
    window.blit(Fonts.font_22.render("Size of your hand: " + str(len(hand.cards)), True, Colors.white), (Globals.WIDTH/2 - text_width/2, Globals.HEIGHT/2 + 100 - text_height/2))
    text_width, text_height = Fonts.font_22.size("Hand's current score: " + str(hand.calc_score()))
    window.blit(Fonts.font_22.render("Hand's current score: " + str(hand.calc_score()), True, Colors.white), (Globals.WIDTH/2 - text_width/2, Globals.HEIGHT/2 + 125 - text_height/2))

def draw_piles(window):
    pile_y = (Globals.HEIGHT/2 - Globals.card_size[1]) - 100
    discard_x = Globals.WIDTH/2 - Globals.card_size[0] - 25
    draw_x = Globals.WIDTH/2 + 25

    # Display discard pile
    if len(Globals.discard_pile) > 0:
        Globals.discard_pile[-1].draw(window, discard_x, pile_y)
    else:
        scale_draw = collider.collides_point(Globals.mouse_position, (discard_x, pile_y, Globals.card_size[0], Globals.card_size[1]))
        card_width, card_height = Globals.card_size
        if scale_draw:
            card_width *= Globals.card_scale
            card_height *= Globals.card_scale
            discard_x -= (card_width - Globals.card_size[0]) / 2
            pile_y -= (card_height - Globals.card_size[1]) / 2
        pyg.draw.rect(window, Colors.white, (discard_x, pile_y, card_width, card_height), border_radius=8)
        pyg.draw.rect(window, Colors.gray, (discard_x + 2, pile_y + 2, card_width - 4, card_height - 4), border_radius=8)
        if scale_draw:
            text_width, text_height = Fonts.font_22.size("Discard")
            window.blit(Fonts.font_22.render("Discard", True, Colors.white), (draw_x + (card_width - text_width)/2, pile_y + (card_height - text_height)/2))
        else:
            text_width, text_height = Fonts.font_20.size("Discard")
            window.blit(Fonts.font_20.render("Discard", True, Colors.white), (draw_x + (card_width - text_width)/2, pile_y + (card_height - text_height)/2))
    
    # Display draw pile
    pile_y = (Globals.HEIGHT/2 - Globals.card_size[1]) - 100
    scale_draw = collider.collides_point(Globals.mouse_position, (draw_x, pile_y, Globals.card_size[0], Globals.card_size[1]))
    card_width, card_height = Globals.card_size
    if scale_draw:
        card_width *= Globals.card_scale
        card_height *= Globals.card_scale
        draw_x -= (card_width - Globals.card_size[0]) / 2
        pile_y -= (card_height - Globals.card_size[1]) / 2

    pyg.draw.rect(window, Colors.white, (draw_x, pile_y, card_width, card_height), border_radius=8)
    pyg.draw.rect(window, Colors.gray, (draw_x + 2, pile_y + 2, card_width - 4, card_height - 4), border_radius=8)

    if scale_draw:
        text_width, text_height = Fonts.font_22.size("Draw")
        window.blit(Fonts.font_22.render("Draw", True, Colors.white), (draw_x + (card_width - text_width)/2, pile_y + (card_height - text_height)/2))
    else:
        text_width, text_height = Fonts.font_20.size("Draw")
        window.blit(Fonts.font_20.render("Draw", True, Colors.white), (draw_x + (card_width - text_width)/2, pile_y + (card_height - text_height)/2))