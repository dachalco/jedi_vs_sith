import pygame
from trajectory import Trajectory

class Player(pygame.sprite.DirtySprite):

    show_trajectory = True

    def __init__(self, screen, row=0, col=0, row_velocity=0, col_velocity=0, sources=100, groups=[]):
        pygame.sprite.Sprite.__init__(self)


        self.screen = screen
        self.color = (0, 255, 0)
        self.radius = 10
        self.trajectory = Trajectory(row, col,
                                     row_velocity, col_velocity,
                                     self.radius, screen.get_height() - self.radius,
                                     self.radius, screen.get_width() - self.radius)

    def draw(self):

        if self.show_trajectory:
            self.trajectory.draw(self.screen)

    def move(self):
        (row, col) = self.trajectory.move(self.screen)
        self.rect.x = row - self.image.get_height() // 2
        self.rect.y = col - self.image.get_width() // 2

    def getCenterPosition(self):
        return [self.rect.x +  self.image.get_height() // 2,
                self.rect.y + self.image.get_width() // 2]

    def getVelocity(self):
        return self.trajectory.velocity

    def update(self):
        self.move()
        self.draw()

