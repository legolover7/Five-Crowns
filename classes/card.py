import pygame as pyg

from classes.display import Colors, Fonts
from classes.globals import Globals
import modules.collider as collider


class Card:
    def __init__(self, value: str, color, size: tuple):
        self.value = value
        self.color = color
        self.width, self.height = size
        self.selected = False
        self.dragging = False
        self.maybe_drag = False

    def draw(self, window, x, y):
        self.x, self.y = x, y
        scaled = self.check_mcollision(False)
        scaled = True if self.selected else scaled
        
        # Calculate hovered card's size and position
        width, height = self.width * (Globals.card_scale if scaled else 1), self.height * (Globals.card_scale if scaled else 1)
        diff_w, diff_h = width - self.width, height - self.height
        x -= diff_w/2
        y -= diff_h/2

        border_color = Colors.aqua if self.selected else Colors.white
        pyg.draw.rect(window, border_color, (x, y, width, height), border_radius=8)
        pyg.draw.rect(window, Colors.gray, (x+2, y+2, width-4, height-4), border_radius=8)

        text_width, text_height = Fonts.font_20.size(self.value)
        window.blit(Fonts.font_20.render(self.value, True, self.color), (x + 6, y + 6))
        window.blit(pyg.transform.rotate(Fonts.font_20.render(self.value, True, self.color), 180), (x + width - text_width - 6, y + height - text_height - 6))

    def check_mcollision(self, maybe_drag):
        if maybe_drag and not self.maybe_drag and collider.collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height)):
            Globals.dragging_offset = [Globals.mouse_position[0] - self.x, Globals.mouse_position[1] - self.y]
            Globals.saved_mposition[0], Globals.saved_mposition[1] = Globals.mouse_position[0], Globals.mouse_position[1]
            Globals.saved_drag_card = self
            Globals.maybe_drag = True
            return True
        return collider.collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))