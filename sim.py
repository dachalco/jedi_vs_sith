import pygame
import colour
from random import randrange

'''
A simulation that is meant to show WHY team work makes the dream work.
Players are randomly placed with velocity per random motion.
Once an objective is within player radius, the player approaches the objective, 
and upon reaching the objective, duels or collaborates with the player objective.
'''

class Player:
    radius = 10

    def __init__(self, row=0, col=0, sources=100):
        self.position = (row, col)
        self.velocity = (randrange(self.radius) - self.radius//2,
                         randrange(self.radius) - self.radius//2)

    def move(self):
        '''
        Single iteration of a player
        '''
        self.position = (self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1])


class Jedi(Player):
    '''
    Jedis try ONLY try to maximize average resources points to Jedi collectively.
    Upon impact with Jedi, Jedis will split their resource points evenly.
    Upon impact with Sith, Sith steals resource points from Jedi and reallocs
    the gained resources to its own resources.
    '''
    def __init__(self):
        super().__init__()
        

        # Jedis have the "right" things for the "right" reasons
        self.lust_resources = randrange(100)
        self.gluttony_resources = randrange(100)
        self.greed_resources = randrange(100)
        self.sloth_resources = randrange(100)
        self.wrath_resources = randrange(100)
        self.envy_resources = randrange(100)
        self.pride_resources = randrange(100)


class Sith(Player):
    '''
    Sith tries to maximize resource points for itself.
    '''
    def __init__(self):
        super().__init__()



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
        # Reset the screen to black. Old drawings persist.
        self.screen.fill((0, 0, 0))

        # Determine new positions for all players.
        for player in self.players:
            player.move()
            self.drawPlayer(player)

        # Draw and increment time
        pygame.display.update()
        self.clock.tick(60)
        print('t=%d\n' % self.clock.get_time())

def main(rows=512, cols=512):
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
               simulating = False

        # Iterate the arena
        arena.incrementTime()

if __name__ == '__main__':
    exit(main())