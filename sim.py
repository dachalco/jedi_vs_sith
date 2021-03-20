import pygame
import colour
import math
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
        self.position = [row, col]
        self.velocity = [randrange(self.radius) - self.radius//2,
                         randrange(self.radius) - self.radius//2]

    def move(self, bounding_row, bounding_col):
        '''
        Single iteration of a player
        '''
        self.position = [self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1]]

        # Wall collisions
        row = self.position[0]
        col = self.position[1]
        if row <= 0 or row >= bounding_row:
            self.velocity[0] = -self.velocity[0]
        if col <= 0 or col >= bounding_col:
            self.velocity[1] = -self.velocity[1]

    def trajectory(self, start_position, start_velocity, tick, bounding_rows, bounding_cols, solution):
        '''
        Get predicted position of player in N ticks
        '''
        if tick <= 0:
            return solution

        predicted_position = [start_position[0] + tick * start_velocity[0],
                              start_position[1] + tick * start_velocity[1]]

        # If there's going to be a wall collision, we must readjust
        collided_vertical = predicted_position[0] <= 0 or bounding_rows <= predicted_position[0]
        collided_horizontal = predicted_position[1] <= 0 or bounding_cols <= predicted_position[1]
        hcollision_position = None
        vcollision_position = None
        ticks_till_hcollision = None
        ticks_till_vcollision = None
        consequent_velocity = start_velocity.copy()

        if not collided_vertical and not collided_horizontal:
            solution.append((start_position, predicted_position))
            return solution

        if collided_vertical and start_velocity[0] != 0:
            if predicted_position[1] >= 0:
                ticks_till_vcollision = math.ceil( (bounding_rows - start_position[0]) / start_velocity[0])
            else:
                ticks_till_vcollision = math.ceil( (0 - start_position[0]) / start_velocity[0])

            # Flip the velocity, save the segment to collision point, and recurse
            consequent_velocity[0] = -start_velocity[0]
            vcollision_position = [start_position[0] + ticks_till_vcollision * start_velocity[0],
                                   start_position[1] + ticks_till_vcollision * start_velocity[1]]

        if collided_horizontal and start_velocity[1] != 0:
            if predicted_position[0] >= 0:
                ticks_till_hcollision = math.ceil( (bounding_cols - start_position[1]) / start_velocity[1])
            else:
                ticks_till_hcollision = math.ceil( (0 - start_position[1]) / start_velocity[1])

            # Flip the velocity, save the segment to collision point, and recurse
            consequent_velocity[1] = -start_velocity[1]
            hcollision_position = [start_position[0] + ticks_till_hcollision * start_velocity[0],
                                  start_position[1] + ticks_till_hcollision * start_velocity[1]]

        if collided_vertical and collided_horizontal:
           ticks_till_collision = min(ticks_till_vcollision, ticks_till_hcollision)
           collision_position = [start_position[0] + ticks_till_collision * start_velocity[0],
                                start_position[1] + ticks_till_collision * start_velocity[1]]
           consequent_velocity[0] = -start_velocity[0]
           consequent_velocity[1] = -start_velocity[1]

        # We've solved for tentative collision point, and have resulting velocity.
        collision_position = hcollision_position if vcollision_position is None else vcollision_position
        ticks_till_collision = ticks_till_hcollision if ticks_till_vcollision is None else ticks_till_vcollision

        # Save this segment, and solve the save problem from new collision point
        solution.append((start_position, collision_position))
        return self.trajectory(collision_position,
                               consequent_velocity,
                               tick - ticks_till_collision,
                               bounding_rows,
                               bounding_cols,
                               solution)


    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,255), self.position, self.radius)
        self.drawTrajectory(screen)

    def drawTrajectory(self, screen, ticks_into_future=64):
        '''
        Trajectory is always linear, and is represented as a sequence of lines
        :return:
        '''
        trajectory = []
        self.trajectory(self.position, self.velocity, ticks_into_future, screen.get_height(), screen.get_width(), trajectory)
        for segment in trajectory:
            pygame.draw.line(screen, (0,255,0), segment[0], segment[1])

class Jedi(Player):
    '''
    Jedis try ONLY try to maximize average resources points to Jedi collectively.
    Upon impact with Jedi, Jedis will split their resource points evenly.
    Upon impact with Sith, Sith steals resource points from Jedi and reallocs
    the gained resources to its own resources.
    '''
    def __init__(self, row=0, col=0, sources=100):
        super().__init__(row, col, sources)
        

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

    def addJedi(self, ):
        '''
        Creates a new player, with random position in arena
        '''

        newb = Player(randrange(self.rows), randrange(self.cols))
        newb.draw(self.screen)
        self.players.add(newb)

    def killPlayer(self, newb):
        assert newb in self.players, 'Can not kill non-existing player!'
        self.players.discard(newb)

    def collidePlayers(self, player):
        '''
        O(n^2) naive solution
        '''
        pass


    def incrementTime(self):
        '''
        Prepares new positions for all players, redraws them, and ticks the clock
        '''
        # Reset the screen to black. Old drawings persist.
        self.screen.fill((0, 0, 0))

        # Determine new positions for all players.
        for player in self.players:
            self.collidePlayers(player)
            player.move(self.rows, self.cols)
            player.draw(self.screen)
            pygame.display.update()

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
                arena.addJedi()
                print(pygame.mouse.get_pos())

            if event.type == pygame.QUIT:
               simulating = False

        # Iterate the arena
        arena.incrementTime()

if __name__ == '__main__':
    exit(main())