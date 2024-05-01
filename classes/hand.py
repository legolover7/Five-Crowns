import pygame as pyg

from classes.card import Card
from classes.display import Colors
from classes.globals import Globals

import modules.collider as collider

class Hand:
    def __init__(self, cards, pos, width=0):
        self.cards = cards
        self.x, self.y = pos
        self.width = width

    def draw(self, window):
        hand_width = (Globals.WIDTH - self.x * 2 if self.width == 0 else self.width)

        # Draw hand rect
        hand_border = Colors.green if len(self.cards) > Globals.current_round else Colors.white
        try:
            height = self.cards[0].height
        except IndexError:
            height = Globals.card_size[1]

        pyg.draw.rect(window, hand_border, (self.x - 10, self.y - 10, hand_width + 20, height + 20), border_radius=8)
        pyg.draw.rect(window, Colors.dark_gray, (self.x - 8, self.y - 8, hand_width + 16, height + 16), border_radius=8)

        if len(self.cards) == 0: return

        # Draw cards
        card_offset_total = hand_width - (len(self.cards) * self.cards[0].width)
        card_offset_single = card_offset_total / (len(self.cards) + 1)
        drag_pos = 0

        for i in range(len(self.cards)):
            x_pos = self.x + card_offset_single * (i + 1) + self.cards[0].width * i
            if self.cards[i].dragging:
                x_pos = Globals.mouse_position[0] - Globals.dragging_offset[0]
                drag_pos = x_pos

            self.cards[i].draw(window, x_pos, self.y)

        # Reorder cards for dragging
        if Globals.saved_drag_card != None and abs(Globals.mouse_position[0] - Globals.saved_mposition[0]) > 5:
            for i in range(len(self.cards)):
                x_pos = self.x + card_offset_single * (i + 1) + self.cards[0].width * i
                if drag_pos < x_pos + card_offset_single / 2:
                    self.cards.remove(Globals.saved_drag_card)
                    self.cards.insert(i, Globals.saved_drag_card)
                    break

    def calc_score(self):
        """Calculates the score based on the contents of the hand"""
        map = {"J": 11, "Q": 12, "K": 13}
        score = 0

        for card in self.cards:
            try:
                current_value = map[card.value]
            except KeyError:
                current_value = int(card.value)

            if current_value == Globals.current_round:
                score += 20
            else:
                score += current_value

        return score

class SavedSets:
    def __init__(self, cards, pos, width):
        self.cards = cards
        self.x, self.y = pos
        self.width = width

    def draw(self, window):
        hand_width = (Globals.WIDTH - self.x * 2 if self.width == 0 else self.width)

        # Draw hand rect
        try:
            height = self.cards[0].height
        except IndexError:
            height = Globals.card_size[1]

        self.height = height

        pyg.draw.rect(window, Colors.white, (self.x - 10, self.y - 10, hand_width + 20, height + 20), border_radius=8)
        pyg.draw.rect(window, Colors.dark_gray, (self.x - 8, self.y - 8, hand_width + 16, height + 16), border_radius=8)

        if not self.check_mcollision():
            pyg.draw.rect(window, Colors.dark_green, (self.x + self.width + 22, self.y + self.height/2 - 18, 40, 40), border_radius=5)
        pyg.draw.rect(window, Colors.dark_green if self.check_mcollision() else Colors.green, (self.x + self.width + 20, self.y + self.height/2 - 20, 40, 40), border_radius=5)
        pyg.draw.line(window, Colors.black, (self.x + self.width + 39, self.y + self.height/2 - 10), (self.x + self.width + 39, self.y + self.height/2 + 10), 2)
        pyg.draw.line(window, Colors.black, (self.x + self.width + 39, self.y + self.height/2 + 10), (self.x + self.width + 29, self.y + self.height/2), 2)
        pyg.draw.line(window, Colors.black, (self.x + self.width + 39, self.y + self.height/2 + 10), (self.x + self.width + 49, self.y + self.height/2), 2)

        # Draw cards
        card_offset_total = hand_width - (len(self.cards) * self.cards[0].width)
        card_offset_single = card_offset_total / (len(self.cards) + 1)

        for i in range(len(self.cards)):
            x_pos = self.x + card_offset_single * (i + 1) + self.cards[0].width * i
            self.cards[i].draw(window, x_pos, self.y)

    def check_mcollision(self):
        """Checks the collision of the green button"""
        return collider.collides_point(Globals.mouse_position, (self.x + self.width + 20, self.y + self.height/2 - 20, 40, 40))