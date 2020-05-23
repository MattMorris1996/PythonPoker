import pygame
from Poker import *
import math


class UICard:
    def __init__(self, width, img_path):
        self.width = width
        self.img_path = "./Playing Cards/PNG-cards-1.3/" + img_path + ".png"
        self.card_image = pygame.image.load(self.img_path)

        rect = self.card_image.get_rect()
        aspect_ratio = rect.height / rect.width
        self.height = int(self.width * aspect_ratio)

        # resize
        self.card_image = pygame.transform.smoothscale(self.card_image, (self.width, self.height))

    def card_display(self, pos_x, pos_y, surface):
        dest_rect = pygame.Rect(pos_x - self.width // 2, pos_y - self.height // 2, self.width, self.height)
        surface.blit(self.card_image, (dest_rect.x, dest_rect.y))


class UIText:
    def __init__(self, text):
        self.text = text
        self.font = "freesansbold.ttf"
        self.font_size = 15

        self.text_font = pygame.font.Font("freesansbold.ttf", self.font_size)
        self.text_surface = self.text_font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()

    def display(self, pos_x, pos_y, surface):
        self.text_rect.center = (pos_x, pos_y)
        surface.blit(self.text_surface, self.text_rect)


class UIPlayer:
    def __init__(self, width, player_obj):
        self.player_name = str(player_obj.number)
        self.chips = str(player_obj.chips)

        self.player_name = UIText(self.player_name)
        self.player_chips = UIText(str(player_obj.chips) + "C")
        self.card_img_1 = UICard(100, player_obj.hand[0].image_path())
        self.card_img_2 = UICard(100, player_obj.hand[1].image_path())

        self.bounding_surface = pygame.Surface((230, 300))
        self.bounding_surface.fill((100, 150, 200))

        self.player_name.display(115, 20, self.bounding_surface)
        self.player_chips.display(115, 50, self.bounding_surface)
        self.card_img_1.card_display(60, 150, self.bounding_surface)
        self.card_img_2.card_display(170, 150, self.bounding_surface)

        aspect_ratio = self.bounding_surface.get_rect().height / self.bounding_surface.get_rect().width
        print(aspect_ratio)
        height = int(aspect_ratio * width)
        self.bounding_surface = pygame.transform.smoothscale(self.bounding_surface, (width, height))

    def get_surface(self):
        return self.bounding_surface


class UIPoker:
    def __init__(self, poker_obj, surface):
        self.players = poker_obj.players
        self.flop = poker_obj.flop
        self.surface_rect = surface.get_rect()
        self.n_players = len(self.players)
        self.table_radius = 200
        self.player_ui_elements = []
        for i in range(self.n_players):
            player = self.players[i]
            self.player_ui_elements.append(UIPlayer(100, player))

    def display(self):
        radians = math.pi / 180
        sep_angle = 360 / self.n_players
        width = self.surface_rect.width
        height = self.surface_rect.height

        ui_player_rect = self.player_ui_elements[0].get_surface().get_rect()
        ui_player_width = ui_player_rect.width
        ui_player_height = ui_player_rect.height

        for i in range(self.n_players):
            x = int(self.table_radius * math.cos(sep_angle * i * radians))
            y = int(self.table_radius * math.sin(sep_angle * i * radians))
            screen.blit(self.player_ui_elements[i].get_surface(),
                        (x + width // 2 - ui_player_width // 2, y + height // 2 - ui_player_height // 2))

    def flop_display(self):
        flop_images = []
        for card in self.flop:
            flop_images.append(UICard(100, card.image_path()))


if __name__ == '__main__':
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([700, 700])

    running = True
    origin_x = 350
    origin_y = 350

    PLAYERS = 8
    BUY_IN = 1000

    game = Poker(PLAYERS, BUY_IN)
    game.deal()
    game.print_hands()
    game.print_flop()
    game.score_hands()

    poker_ui = UIPoker(game, screen)

    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((50, 155, 50))
        poker_ui.display()
        # Draw a solid blue circle in the center

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
