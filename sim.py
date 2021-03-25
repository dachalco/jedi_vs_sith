import os
import pygame
import colour
import math
from random import randrange
from sith import Sith
from jedi import Jedi

'''
A simulation that is meant to show WHY team work makes the dream work.
Players are randomly placed with velocity per random motion.
Once an objective is within player radius, the player approaches the objective, 
and upon reaching the objective, duels or collaborates with the player objective.
'''


def spawnSith(screen):
    # Spawn some Sith by default
    for i in range(10):
        member = Sith(screen,
                      randrange(screen.get_height()),
                      randrange(screen.get_width()),
                      randrange(5),
                      randrange(5))

def clear_callback(surface, rect):
    black = (0,0,0)
    surface.fill(black, rect)

def main(rows=512, cols=512):
    pygame.init()
    pygame.display.set_caption('Jedi vs. Sith')
    screen = pygame.display.set_mode((rows, cols))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    pygame.display.update()

    # Some sith are spawned by default
    spawnSith(screen)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Jedi.show_trajectory = not Jedi.show_trajectory
            if event.type == pygame.QUIT:
               simulating = False

        # Iterate the arena
        Jedi.group.update()
        Jedi.group.clear(screen, clear_callback)
        Jedi.group.draw(screen)

        Sith.group.update()
        Sith.group.clear(screen, clear_callback)
        Sith.group.draw(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    exit(main())