import pygame
import pymunk
from trajectory import Trajectory

class Player(pygame.sprite.DirtySprite):

    show_trajectory = True

    def __init__(self, screen, space, row=0, col=0, row_velocity=0, col_velocity=0, sources=100, groups=[]):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen


    def draw(self):
        pass

    def getCenterPosition(self):
        return [self.rect.x +  self.image.get_height() // 2,
                self.rect.y + self.image.get_width() // 2]

    def getVelocity(self):
        return None

    def flipy(self, y):
        """Small hack to convert chipmunk physics to pygame coordinates"""
        return -y + self.screen.get_height()

    def update(self):
        '''
        Sprite drawing is handled by drawing engine, and only requires self.image and self.rect.
        Upon update, we must translate the update from the physics engine to the drawing engine
        '''
        position = self.shape.body.position
        rotation = self.shape.body.rotation_vector

        # Translate coords
        self.rect.x, self.rect.y = int(position.x) - self.radius, int(self.flipy(position.y) - self.radius)

        pygame.draw.circle(self.screen,
                           pygame.Color("green"),
                           (self.rect.x + self.radius, self.rect.y + self.radius),
                           int(self.shape.radius), 2)

        # Process collisions
        self.postProcessCollision()
