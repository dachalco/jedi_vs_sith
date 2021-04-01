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
    image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'jedi', 'jedi.png')), [100, 100])

    def __init__(self, screen, space, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        Player.__init__(self, screen, space, row, col, row_velocity, col_velocity, sources)
        self.add([Jedi.group])

        # Configure pygame sprite
        self.screen = screen
        self.rect = self.image.get_rect()

        # Modify physics
        self.space = space
        self.color = (0, 255, 0)
        self.radius = 50
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

        # Process collisions. Only Jedis process collisions
        self.postProcessCollision()

        self.drawHealth()


    def postProcessCollision(self):
        # Temporarily remove self from collision list. Otherwise you detect collision with self
        self.remove(Jedi.group)

        # Jedi-Jedi collision
        collided_sprite = pygame.sprite.spritecollideany(self, Jedi.group, pygame.sprite.collide_mask)
        if collided_sprite != None:
            other_jedi = collided_sprite

            # Jedis help each other out
            avg_lust_resources = (self.lust_resources + other_jedi.lust_resources) / 2
            avg_gluttony_resources = (self.gluttony_resources + other_jedi.gluttony_resources) / 2
            avg_greed_resources = (self.greed_resources + other_jedi.greed_resources) / 2
            avg_sloth_resources = (self.sloth_resources + other_jedi.sloth_resources) / 2
            avg_wrath_resources = (self.wrath_resources + other_jedi.wrath_resources) / 2
            avg_envy_resources = (self.envy_resources + other_jedi.envy_resources) / 2
            avg_pride_resources = (self.pride_resources + other_jedi.pride_resources) / 2

            self.lust_resources = avg_lust_resources
            self.gluttony_resources = avg_gluttony_resources
            self.greed_resources = avg_greed_resources
            self.sloth_resources = avg_sloth_resources
            self.wrath_resources = avg_wrath_resources
            self.envy_resources = avg_envy_resources
            self.pride_resources = avg_pride_resources

            other_jedi.lust_resources = avg_lust_resources
            other_jedi.gluttony_resources = avg_gluttony_resources
            other_jedi.greed_resources = avg_greed_resources
            other_jedi.sloth_resources = avg_sloth_resources
            other_jedi.wrath_resources = avg_wrath_resources
            other_jedi.envy_resources = avg_envy_resources
            other_jedi.pride_resources = avg_pride_resources

        self.add(Jedi.group)

        # Jedi-Sith collision
        collided_sprite = pygame.sprite.spritecollideany(self, Sith.group, pygame.sprite.collide_mask)
        if collided_sprite != None:
            print('jedi-sith collision')
