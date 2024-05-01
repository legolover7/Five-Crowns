# Import statements
import pygame as pyg
import random
import sys
import os

# Custom modules
from classes.buttons import Button
from classes.card import Card
from classes.display import Colors, Fonts
from classes.globals import Globals
from classes.hand import Hand, SavedSets
import modules.draw as draw
import modules.collider as collider

# Get/set the number of players
stop = False
args = sys.argv[1:]
if len(args) > 0:
    try:
        Globals.num_players = min(7, int(args[0]))
        if Globals.num_players < 2:
            Globals.num_players = 2
    except:
        Globals.num_players = 2

# Initialize window
pyg.init()
info_object = pyg.display.Info()
Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
Globals.WINDOW = pyg.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))
pyg.display.set_caption("Texting App")
os.system("cls")

def Main():
    reset()
    discarded = False
    drew = False

    # Set up players' hands
    hands = []
    saved_sets = []
    player_details = []

    for i in range(Globals.num_players):
        cards = []
        for _ in range(Globals.current_round):
            cards.append(draw_card())
        hands += [Hand(cards, (300, 700))]
        saved_sets += [{"sets": [], "num_saved": 0}]
        player_details += [{"player_id": i, "scores": []}]

    hands[0].cards = [Card("4", Colors.green, Globals.card_size), Card("4", Colors.green, Globals.card_size), Card("4", Colors.green, Globals.card_size)]
    
    check_button = Button((Globals.WIDTH/2-150, Globals.HEIGHT-100, 300, 90), Colors.aqua, "Check Selected", Fonts.font_20, Colors.black)
    pass_play_button = Button((Globals.WIDTH/2-150, Globals.HEIGHT/2+50, 300, 90), Colors.green, "Next Player", Fonts.font_20, Colors.black)

    while True:
        current_hand = hands[Globals.player_turn]
        current_sets = saved_sets[Globals.player_turn]["sets"]

        if Globals.went_out and discarded:
            check_button.text = "Play Hand"
            check_button.color = Colors.green if hands[Globals.player_turn].calc_score() == 0 else Colors.yellow

        # Get events
        for event in pyg.event.get():
            Globals.mouse_position[0] = pyg.mouse.get_pos()[0] * (Globals.WIDTH / Globals.WINDOW_WIDTH)
            Globals.mouse_position[1] = pyg.mouse.get_pos()[1] * (Globals.HEIGHT / Globals.WINDOW_HEIGHT)

            if abs(Globals.mouse_position[0] - Globals.saved_mposition[0]) > 5 and Globals.saved_drag_card != None:
                Globals.saved_drag_card.dragging = True

            mods = pyg.key.get_mods()
            shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL
            
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            elif event.type == pyg.KEYDOWN:
                key = event.key

                # Kill key
                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()

                elif key == pyg.K_F5:
                    reset()

                elif key == pyg.K_ESCAPE:
                    for card in hands.cards:
                        card.selected = False

            elif event.type == pyg.MOUSEBUTTONDOWN:
                # Check if the selected cards are alright
                if check_button.check_mcollision():
                    if check_button.text == "Check Selected" and check_selected(current_hand):
                        # Cards were a valid hand, add it to a new set
                        selected_cards = []
                        # Copy cards from hand
                        for card in current_hand.cards:
                            if card.selected:
                                selected_cards += [card]
                                saved_sets[Globals.player_turn]["num_saved"] += 1

                        # Delete from hand
                        for card in selected_cards:
                            current_hand.cards.remove(card)
                            card.width *= .75
                            card.height *= .75
                            card.selected = False

                        # Create a new saved set and add it
                        saved_sets[Globals.player_turn]["sets"] += [SavedSets(selected_cards, (40, 10 + (Globals.card_size[1] * .85) * len(saved_sets[Globals.player_turn]["sets"])), 500)]

                        # Change check selected button to play hand button
                        if saved_sets[Globals.player_turn]["num_saved"] == Globals.current_round:
                            check_button.color = Colors.green
                            check_button.text = "Go Out!"

                    # Player went out
                    elif check_button.text == "Go Out!":
                        if len(hands[Globals.player_turn].cards) != 0:
                            Globals.discard_pile.append(hands[Globals.player_turn].cards.pop())

                        player_details[Globals.player_turn]["scores"] += [0]
                        Globals.went_out = True
                        Globals.player_turn += 1
                        Globals.player_turn %= Globals.num_players
                        check_button.text = "Check Selected"
                        check_button.color = Colors.aqua
                        drew = False
                        discarded = False

                    # Player was forced to play their hand (after discarding)
                    elif check_button.text == "Play Hand" and len(hands[Globals.player_turn].cards) <= Globals.current_round:
                        player_details[Globals.player_turn]["scores"] += [hands[Globals.player_turn].calc_score()]
                        Globals.player_turn += 1
                        Globals.player_turn %= Globals.num_players
                        drew = False
                        # Was the last player to have to play
                        if len(player_details[Globals.player_turn]["scores"]) == Globals.current_round - 2:
                            reset()
                            Globals.current_round += 1
                            Globals.player_turn = Globals.starting_player
                            Globals.starting_player += 1
                            Globals.starting_player %= Globals.num_players
                            Globals.went_out = 0
                            check_button.text = "Check Selected"
                            check_button.color = Colors.aqua
                            discarded = False
                            hands = []

                            for i in range(Globals.num_players):
                                cards = []
                                for _ in range(Globals.current_round):
                                    cards.append(draw_card())
                                hands += [Hand(cards, (300, 700))]
                                saved_sets[i] = {"sets": [], "num_saved": 0}
                            
                # Checks for players passing turns
                elif pass_play_button.text == "Next Player" and discarded and pass_play_button.check_mcollision():
                    Globals.player_turn += 1
                    Globals.player_turn %= Globals.num_players
                    check_button.text = "Check Selected"
                    check_button.color = Colors.aqua
                    discarded = False
                    drew = False
                else:
                    # Check player card collisions
                    for card in current_hand.cards:
                        if not ctrl and not (Globals.discard_pile[-1].check_mcollision(False) and len(current_hand.cards) + saved_sets[Globals.player_turn]["num_saved"] > Globals.current_round):
                            card.selected = False
                        if card.check_mcollision(True):
                            if event.button == 1:
                                card.selected = not card.selected
                            elif event.button == 3:
                                current_hand.cards.remove(card)

                    # Check saved sets return button
                    index = -1
                    for set in current_sets:
                        if set.check_mcollision():
                            index = current_sets.index(set)
                            for card in set.cards:
                                current_hand.cards += [card]
                                card.width /= .75
                                card.height /= .75
                                saved_sets[Globals.player_turn]["num_saved"] -= 1
                    
                    if index != -1: 
                        current_sets.pop(index)
                        check_button.color = Colors.aqua
                        check_button.text = "Check Selected"

                    # Draw a new card
                    if collider.collides_point(Globals.mouse_position, (Globals.WIDTH/2 + 25, (Globals.HEIGHT/2 - Globals.card_size[1]) - 100, Globals.card_size[0], Globals.card_size[1])) and len(current_hand.cards) <= Globals.current_round and not drew and check_button.text == "Check Selected":
                        card = draw_card() 
                        if card is not None:
                            current_hand.cards.append(card)

                        drew = True

                    # Discard current card
                    elif Globals.discard_pile[-1].check_mcollision(False) and not discarded:
                        if drew == False:
                            current_hand.cards.append(Globals.discard_pile.pop())
                            drew = True
                        else:
                            num_selected_cards = 0
                            
                            for card in current_hand.cards:
                                if card.selected:
                                    num_selected_cards += 1
                                    selected_index = current_hand.cards.index(card)

                            if num_selected_cards == 1:
                                Globals.discard_pile.append(current_hand.cards[selected_index])
                                Globals.discard_pile[-1].selected = False
                                current_hand.cards.pop(selected_index)
                                discarded = True

            elif event.type == pyg.MOUSEBUTTONUP:
                if Globals.saved_drag_card != None:
                    # Reset dragging stuff
                    for card in current_hand.cards:
                        card.maybe_drag = False
                    Globals.saved_drag_card.dragging = False
                    Globals.saved_drag_card = None
                    Globals.saved_mposition = [0, 0]
                    Globals.dragging_offset = [0, 0]

        draw.draw(current_hand, check_button, pass_play_button, current_sets, discarded, player_details)
        Globals.clock.tick(Globals.FPS)

def reset():
    # Setup draw pile
    values = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    current_cards = []
    for color in Colors.card_colors:
        for value in values:
            current_cards.append({"value": value, "color": color})
            current_cards.append({"value": value, "color": color})

    while len(current_cards):
        card = random.choice(current_cards)
        current_cards.remove(card)
        Globals.draw_pile.append(card)

    Globals.discard_pile.append(Card("Empty", Colors.white, Globals.card_size))
    Globals.discard_pile.append(draw_card())

def check_selected(hand):
    selected_list = []
    map = {"J": 11, "Q": 12, "K": 13}

    # Get the currently seleceted cards
    for card in hand.cards:
        if card.selected:
            selected_list += [card]

    print("Selected cards: ", end="")
    for card in selected_list:
        print(card.value, end=" ")
    print("\n")

    if len(selected_list) < 3: 
        print("Not enough cards to check, returning False")
        return False

    # First, check if they're all the same
    card_value = 0
    smallest_value = 1000
    occurences = {}

    are_same = True
    print("Checking if they're all the same")
    for card in selected_list:
        # Save the smallest value for the next check, as well as the number of occurances
        try:
            current_value = map[card.value]
        except KeyError:
            current_value = int(card.value)

        print("Looking at value:", current_value)
        if current_value in occurences:
            occurences[current_value] += 1
        else:
            occurences[current_value] = 1

        if current_value < smallest_value and current_value != Globals.current_round:
            smallest_value = current_value

        # Do the checking of equal values
        if current_value == Globals.current_round:
            continue
        if card_value == 0:
            print("Saving value:", current_value)
            card_value = current_value
            continue
        
        print("Checking", current_value, "vs", card_value)
        if current_value != card_value:
            are_same = False

    if are_same: 
        print("All the same, returning True")
        return True
    print("Cards are not the same\n")
    
    # Then, check if it's a straight
    # Store the number of occurences of each card
    popped_smallest = False
    print("Checking if it's a straight")
    card_color = ""
    for card in selected_list:
        # Check if they're all the same color
        if card_color == "":
            card_color = card.color
        else:
            if card.color != card_color:
                print("Colors didn't match, returning False")
                return False
            
        if card_value == smallest_value and not popped_smallest:
            selected_list.remove(card)
            popped_smallest = True


    print("Building straight from value", smallest_value)
    # Try to build a straight, starting at the saved smallest value
    current_value = smallest_value
    for _ in range(len(selected_list)):
        # Check if the card itself exists somewhere
        print("Checking for a", current_value)
        if current_value in occurences:
            occurences[current_value] -= 1
            if occurences[current_value] == 0:
                occurences.pop(current_value)
            current_value += 1
            continue

        # Check wildcards
        print("Didn't find it, checking for a wildcard")
        if Globals.current_round in occurences:
            occurences[Globals.current_round] -= 1
            if occurences[Globals.current_round] == 0:
                occurences.pop(Globals.current_round)
            current_value += 1

        else:
            print("Couldn't build a straight, returning False")
            return False
        
    print("A valid straight was found, returning True")
    return True

def draw_card():
    try:
        card = Globals.draw_pile[0]
    except IndexError:
        return
    Globals.draw_pile.remove(card)
    return Card(card["value"], card["color"], Globals.card_size)

if __name__ == "__main__":
    Main()