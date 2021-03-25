import os
import pygame
from BasePlayer import Player
from random import randrange


class Sith(Player):
    '''
    Sith tries to maximize resource points for itself.
    '''

    group = pygame.sprite.Group()

    image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sith', 'sith.png')), [25, 25])


    def __init__(self, screen, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        Player.__init__(self, screen, row, col, row_velocity, col_velocity, sources)
        self.add(Sith.group)

        self.show_trajectory = False
        self.color = (255, 0, 0)

        # Configure pygame sprite
        self.screen = screen
        self.rect = self.image.get_rect()
