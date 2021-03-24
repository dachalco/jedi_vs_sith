import os
import pygame
import colour
import math
from random import randrange
from trajectory import Trajectory

'''
A simulation that is meant to show WHY team work makes the dream work.
Players are randomly placed with velocity per random motion.
Once an objective is within player radius, the player approaches the objective, 
and upon reaching the objective, duels or collaborates with the player objective.
'''

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
        (row, col) = self.trajectory.move()
        self.rect.x = row - self.image.get_height() // 2
        self.rect.y = col - self.image.get_width() // 2

    def update(self):
        self.clear()
        self.move()
        self.draw()

class Jedi(Player):
    '''
    Jedis try ONLY try to maximize average resources points to Jedi collectively.
    Upon impact with Jedi, Jedis will split their resource points evenly.
    Upon impact with Sith, Sith steals resource points from Jedi and reallocs
    the gained resources to its own resources.
    '''

    group = pygame.sprite.Group()

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
        self.image = pygame.image.load(os.path.join('assets', 'jedi', 'jedi.png'))
        self.image = pygame.transform.scale(self.image, [25,25])
        self.rect = self.image.get_rect()


    def update(self):
        self.move()
        self.draw()

class Sith(Player):
    '''
    Sith tries to maximize resource points for itself.
    '''

    group = pygame.sprite.Group()

    def __init__(self, screen, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        Player.__init__(self, screen, row, col, row_velocity, col_velocity, sources)
        self.add(Sith.group)

        self.show_trajectory = False
        self.color = (255, 0, 0)

        # Configure pygame sprite
        self.screen = screen
        self.image = pygame.image.load(os.path.join('assets', 'sith', 'sith.png'))
        self.rect = self.image.get_rect()




def spawnSith(screen):
    # Spawn some Sith by default
    for i in range(10):
        member = Sith(screen,
                      randrange(screen.get_height()),
                      randrange(screen.get_width()),
                      randrange(5),
                      randrange(5))


def main(rows=512, cols=512):
    pygame.init()
    pygame.display.set_caption('Jedi vs. Sith')
    screen = pygame.display.set_mode((rows, cols))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    pygame.display.update()

    # Some sith are spawned by default
    #spawnSith(screen)

    # Simulate time in arena
    simulating = True
    while simulating:
        # First process events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # left click
                    Jedi(screen,
                         randrange(screen.get_height()),
                         randrange(screen.get_width()),
                         randrange(10),
                         randrange(10))
                elif event.button == 3:
                    pass

                print(pygame.mouse.get_pos())
            elif event.type == pygame.QUIT:
               simulating = False

        # Iterate the arena
        screen.fill((0, 0, 0))
        Jedi.group.update()
        Jedi.group.draw(screen)

        #Sith.group.update()
        #Sith.group.draw(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    exit(main())