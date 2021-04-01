import os
import pygame
import pymunk
import colour
import math
from random import randrange
from sith import Sith
from jedi import Jedi
from pymunk import Vec2d

'''
A simulation that is meant to show WHY team work makes the dream work.
Players are randomly placed with velocity per random motion.
Once an objective is within player radius, the player approaches the objective, 
and upon reaching the objective, duels or collaborates with the player objective.
'''


def spawnSith(screen, space):
    # Spawn some Sith by default
    for i in range(2):
        member = Sith(screen, space,
                      randrange(screen.get_height()),
                      randrange(screen.get_width()),
                      randrange(5),
                      randrange(5))


def clear_callback(surface, rect):
    black = (0,0,0)
    surface.fill(black, rect)

def initPhysics(screen, space):
    space.gravity = Vec2d(0.0, -900.0)
    frame = [
        pymunk.Segment(space.static_body,
                       (0, 0), (0, screen.get_height()),
                       0.0),
        pymunk.Segment(space.static_body,
                       (0, screen.get_height()),
                       (screen.get_width(), screen.get_height()),
                       0.0),
        pymunk.Segment(space.static_body,
                       (screen.get_width(), screen.get_height()),
                       (screen.get_width(), 0),
                       0.0),
        pymunk.Segment(space.static_body,
                       (screen.get_width(), 0),
                       (0, 0),
                       0.0),
    ]

    for l in frame:
        l.friction = 0.5
    space.add(*frame)

def main(rows=1000, cols=1000):
    fps = 60.0

    # Initialize drawinng engine
    pygame.init()
    pygame.display.set_caption('Jedi vs. Sith')
    screen = pygame.display.set_mode((rows, cols))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    pygame.display.update()

    # Initialize physics engine
    space = pymunk.Space()
    initPhysics(screen, space)
    dt = 1/fps

    # Some sith are spawned by default
    spawnSith(screen, space)

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
                         space,
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
        space.step(dt)

        Jedi.group.update()
        Jedi.group.clear(screen, clear_callback)
        Jedi.group.draw(screen)

        Sith.group.update()
        Sith.group.clear(screen, clear_callback)
        Sith.group.draw(screen)

        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    exit(main())