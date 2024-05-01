import pygame as pyg
pyg.init()

class Globals:
    # Default size of the application
    WIDTH, HEIGHT = (1920, 1080)
    # User's monitor size
    WINDOW_WIDTH, WINDOW_HEIGHT = (1920, 1080)
    # Actual window object that gets displayed to the user
    WINDOW = None
    # Image buffer that gets scaled to the user's monitor size, from the default size
    VID_BUFFER = pyg.surface.Surface((WIDTH, HEIGHT))

    # Max FPS of application
    FPS = 60
    # Pygame clock object for controlling the framerate
    clock = pyg.time.Clock()

    # Current position of mouse cursor
    mouse_position = [0, 0]
    saved_mposition = [0, 0]
    dragging_offset = [0, 0]
    saved_drag_card = None

    card_size = (150, 250)
    draw_pile = []
    discard_pile = []
    current_round = 3
    card_scale = 1.1

    num_players = 2
    player_turn = 0
    starting_player = 0
    player_hands = []
    went_out = False