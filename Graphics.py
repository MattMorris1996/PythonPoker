# Simple pygame program

# Import and initialize the pygame library
import pygame
from Poker import *
import math
import random
from os import listdir
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([700, 700])

cards_paths = listdir("./Playing Cards/PNG-cards-1.3/")
path_length = len(cards_paths)

class CardGraphic:
    def __init__(self, x, y, img_path, angle):
        ratio = 726/500
        self.width = 55
        self.length = int(self.width*ratio)
        self.angle = angle
        self.img_path = "./Playing Cards/PNG-cards-1.3/" + img_path +".png"
        self.display_rect = pygame.Rect(x-self.width//2, y-self.length//2, self.width, self.length)
        self.highlight_rect = pygame.Rect(x-5 - self.width // 2, y-5 - self.length // 2, self.width+10, self.length+10)
        self.highlight = False

        self.image_blit = pygame.image.load(self.img_path)
        self.image_blit = pygame.transform.smoothscale(self.image_blit, (self.display_rect.width, self.display_rect.height))

    def display(self, surface):
        if self.highlight:
            pygame.draw.rect(surface, (221, 230, 69), self.highlight_rect)

        surface.blit(self.image_blit, (self.display_rect.x, self.display_rect.y))

    def mouse_over(self, mouse_x, mouse_y):
        hit_horizontal = (self.display_rect.x <= mouse_x <= self.display_rect.x + self.display_rect.width)
        hit_vertical = (self.display_rect.y <= mouse_y <= self.display_rect.y + self.display_rect.height)
        if hit_horizontal and hit_vertical:
            self.highlight = True
        else:
            self.highlight = False


def text_objects(text, font):
    text_surface = font.render(text, True, (0,0,0))
    return text_surface, text_surface.get_rect()

class TextInput:
    def __init__(self, pos_x, pos_y, width, height):

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.selected = True
        self.highlight = False

        self.display_rect = pygame.Rect(pos_x - width // 2, pos_y - height // 2, width, height)

        self.pulse_start = pygame.time.get_ticks()
        self.pulse_duration = 900
        self.pulse = True
        self.text = "200"

    def display(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.display_rect)

        button_text = pygame.font.Font("freesansbold.ttf", self.display_rect.height)
        text_surf, text_rect = text_objects(self.text, button_text)
        text_rect.center = (self.pos_x, self.pos_y)
        surface.blit(text_surf, text_rect)

        pulse_rect = pygame.Rect(text_rect.x + text_rect.width + 1, text_rect.y, 1, text_rect.height)

        if self.selected:
            if pygame.time.get_ticks() - self.pulse_start >= self.pulse_duration:
                self.pulse_start = pygame.time.get_ticks()
                self.pulse = not self.pulse

        if self.pulse:
            pygame.draw.rect(surface, (0, 0, 0), pulse_rect)

    def mouse_over(self, mouse_x, mouse_y):
        hit_horizontal = (self.display_rect.x <= mouse_x <= self.display_rect.x + self.display_rect.width)
        hit_vertical = (self.display_rect.y <= mouse_y <= self.display_rect.y + self.display_rect.height)
        if hit_horizontal and hit_vertical:
            self.highlight = True
        else:
            self.highlight = False

    def picked(self, click_down, text):
        if click_down and self.highlight:
            self.selected = True
            self.text += text
        else:
            self.selected = True


class Button:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.display_rect = pygame.Rect(pos_x - width // 2, pos_y - height // 2, width, height)
        self.highlight = False
        self.text = "Fold"

    def display(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.display_rect)
        button_text = pygame.font.Font("freesansbold.ttf", 10)
        text_surf, text_rect = text_objects(self.text, button_text)
        text_rect.center = (self.pos_x, self.pos_y)
        surface.blit(text_surf, text_rect)

    def mouse_over(self, mouse_x, mouse_y):
        hit_horizontal = (self.display_rect.x <= mouse_x <= self.display_rect.x + self.display_rect.width)
        hit_vertical = (self.display_rect.y <= mouse_y <= self.display_rect.y + self.display_rect.height)
        if hit_horizontal and hit_vertical:
            self.highlight = True
        else:
            self.highlight = False

# Run until the user asks to quit
if __name__ == '__main__':
    running = True
    radius = 270
    cards = []
    origin_x = 350
    origin_y = 350

    PLAYERS = 7
    BUY_IN = 1000

    game = Poker(PLAYERS, BUY_IN)
    game.deal()
    game.print_hands()
    game.print_flop()
    game.score_hands()

    flop_paths = []
    for card in game.flop:
        flop_paths.append(card.image_path())

    player_card_paths = []
    for player in game.players:
        hand_paths = []
        for card in player.hand:
            hand_paths.append(card.image_path())
        player_card_paths.append(hand_paths)

    sep_angle = 360 // PLAYERS

    for i in range(PLAYERS):
        radians = math.pi / 180
        x = int(radius * math.cos(sep_angle*i*radians))
        y = int(radius * math.sin(sep_angle*i*radians))
        cards.append(CardGraphic(origin_x + x -55//2, origin_y + y, player_card_paths[i][0], sep_angle*i))
        cards.append(CardGraphic(origin_x + x + 55-55//2 + 5, origin_y +y, player_card_paths[i][1], sep_angle*i))

    start_button = TextInput(origin_x, origin_y + 70, 55, 20)

    start = int(origin_x - 2*55)
    for i in range(5):
        cards.append(CardGraphic(start + 60*i, origin_y, flop_paths[i], 0))

    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((50, 155, 50))

        # Draw a solid blue circle in the center

        #render flop
        mouse = pygame.mouse.get_pos()
        for card in cards:
            card.mouse_over(mouse[0], mouse[1])
            card.display(screen)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()