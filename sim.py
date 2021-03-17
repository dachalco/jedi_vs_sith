import pygame
import colour
from random import randrange


class Player:
    radius = 1

    def __init__(self, row=0, col=0):
        self.position = (row, col)

class Arena:
    '''
    Responsible for redrawing all players
    '''
    def __init__(self, screen):
        assert type(screen) == pygame.Surface

        self.screen = screen
        self.rows = screen.get_height()
        self.cols = screen.get_width()
        self.clock = pygame.time.Clock()
        self.players = set()

    def addPlayer(self):
        '''
        Creates a new player, with random position in arena
        '''

        newb = Player(randrange(self.rows), randrange(self.cols))
        self.players.add(newb)
        self.drawPlayer(newb)
        pygame.display.update()

    def killPlayer(self, newb):
        assert newb in self.players, 'Can not kill non-existing player!'
        self.players.discard(newb)

    def drawPlayer(self, player):
        assert player in self.players, 'Can not draw non-existing player!'
        pygame.draw.circle(self.screen, (0,0,255), player.position, player.radius)

    def incrementTime(self):
        '''
        Prepares new positions for all players, redraws them, and ticks the clock
        '''
        # Determine new positions for all players. Note, these

        # Increment time
        self.clock.tick()
        print('t=%d\n' % self.clock.get_time())

def main(rows=256, cols=256):
    pygame.init()
    pygame.display.set_caption('Jedi vs. Sith')
    screen = pygame.display.set_mode((rows, cols))
    screen.fill((0, 0, 0))
    pygame.display.update()

    arena = Arena(screen)

    simulating = True
    while simulating:
        # First process events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                arena.addPlayer()

            if event.type == pygame.QUIT:
                pass

        # Iterate the arena
        arena.incrementTime()

if __name__ == '__main__':
    exit(main())