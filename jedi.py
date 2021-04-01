import os
import pygame
from BasePlayer import Player
from random import randrange
from sith import Sith
import pymunk

class Jedi(Player):
    '''
    Jedis try ONLY try to maximize average resources points to Jedi collectively.
    Upon impact with Jedi, Jedis will split their resource points evenly.
    Upon impact with Sith, Sith steals resource points from Jedi and reallocs
    the gained resources to its own resources.
    '''

    group = pygame.sprite.Group()
    image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'jedi', 'jedi.png')), [50, 50])

    def __init__(self, screen, space, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        Player.__init__(self, screen, space, row, col, row_velocity, col_velocity, sources)
        self.add([Jedi.group])

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

        # Modify physics
        self.space = space
        self.color = (0, 255, 0)
        self.radius = 25
        self.x = row
        self.y = col
        self.mass = 10
        self.moment = pymunk.moment_for_circle(self.mass, 0, 5)

        # Physics body
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = row, col
        self.body.velocity = row_velocity, col_velocity
        self.body.angle = 0

        # Physics shape
        self.shape = pymunk.Circle(radius=self.radius, body=self.body)
        self.shape.friction = 0.01
        self.shape.elasticity = 1.0

        self.space.add(self.body, self.shape)


    def update(self):
        super().update()

    def postProcessCollision(self):
        # Temporarily remove self from collision list. Otherwise you detect collision with self
        self.remove(Jedi.group)

        # Jedi-Jedi collision
        collided_sprite = pygame.sprite.spritecollideany(self, Jedi.group, pygame.sprite.collide_mask)
        if collided_sprite != None:
            print('jedi-jedi collision')

        self.add(Jedi.group)

        # Jedi-Sith collision
        collided_sprite = pygame.sprite.spritecollideany(self, Sith.group, pygame.sprite.collide_mask)
        if collided_sprite != None:
            print('jedi-sith collision')
