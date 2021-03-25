import os
import pygame
from BasePlayer import Player
from random import randrange

class Jedi(Player):
    '''
    Jedis try ONLY try to maximize average resources points to Jedi collectively.
    Upon impact with Jedi, Jedis will split their resource points evenly.
    Upon impact with Sith, Sith steals resource points from Jedi and reallocs
    the gained resources to its own resources.
    '''

    group = pygame.sprite.Group()
    image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'jedi', 'jedi.png')), [25, 25])

    def __init__(self, screen, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        Player.__init__(self, screen, row, col, row_velocity, col_velocity, sources)
        self.add([Jedi.group])

        self.color = (0, 0, 255)

        # Jedis have the "right" things for the "right" reasons
        self.lust_resources = randrange(100)
        self.gluttony_resources = randrange(100)
        self.greed_resources = randrange(100)
        self.sloth_resources = randrange(100)
        self.wrath_resources = randrange(100)
        self.envy_resources = randrange(100)
        self.pride_resources = randrange(100)

        # Configure pygame sprite
        self.screen = screen
        self.rect = self.image.get_rect()
