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
            print('jedi-jedi collision!')
            other_jedi = collided_sprite

            # Jedis help each other out
            for i in range(7):
                avg_resources = (self.resources[i] + other_jedi.resources[i]) / 2
                self.resources[i] = avg_resources + 5
                other_jedi.resources[i] = avg_resources + 5

                if self.resources[i] > 100:
                    self.resources[i] = 100

                if other_jedi.resources[i] > 100:
                    other_jedi.resources[i] = 100

        self.add(Jedi.group)

        # Jedi-Sith collision
        collided_sprite = pygame.sprite.spritecollideany(self, Sith.group, pygame.sprite.collide_mask)
        if collided_sprite != None:
            print('jedi-sith collision!')
            sith = collided_sprite

            # Sith steal from Jedi
            for i in range(len(self.resources)):
                self.resources[i] -= 5
                sith.resources[i] += 5

                if self.resources[i] < 0:
                    self.resources[i] = 0

                if sith.resources[i] >= 100:
                    sith.resources[i] = 100