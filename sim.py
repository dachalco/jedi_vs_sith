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

class Trajectory:
    def __init__(self, row=0, col=0,
                       row_velocity=0, col_velocity=0,
                       row_low=0, row_high=100, col_low=0, col_high=100):
        # Set boundaries
        self.row_high = row_high
        self.row_low = row_low
        self.col_high = col_high
        self.col_low = col_low

        # Kinetics
        self.position = [row, col]
        self.velocity = [row_velocity, col_velocity]


        # Trajectory representation as list of linear segments
        # Note the longest path is the diagonal
        self.foresight_ticks = math.ceil(math.sqrt( (col_high - col_low)**2 + (row_high - row_low)**2))
        self.n_segments = 4
        self.segments = []
        self.solve(self.position, self.velocity, self.n_segments, self.segments)

    def move(self):
        '''
        Single iteration of a player
        '''
        # Continue with expected movement
        self.position = [self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1]]

        if not self.isStationary():
            segment = self.segments[0]
            collision_point = segment[1]
            next_velocity   = segment[2]

            if self.position == collision_point:
                # The segment is done. Update per its solutions
                self.segments.pop(0)
                self.velocity = next_velocity

                # Replaced the used up segment by appending a new one
                final_segment = self.segments[-1]
                final_position = final_segment[1]
                final_velocity = final_segment[2]
                next_trajectory = self.solve(final_position,
                                             final_velocity,
                                             0,
                                             self.segments)

    def isStationary(self):
        return self.velocity == [0, 0]

    def solve(self, start_position, start_velocity, segment_i, solution):
        '''
        Get predicted position of player in N ticks
        '''
        if segment_i < 0:
            return solution

        # We need to solve for collision point, however we must take into account that collisions
        # can occur "off the wall" since velocity increments in discrete steps
        next_velocity = start_velocity.copy()
        row_velocity = start_velocity[0]
        col_velocity = start_velocity[1]
        row = start_position[0]
        col = start_position[1]

        if row_velocity > 0:
            ticks_to_row_collision = math.ceil( (self.row_high - row) / row_velocity )
        elif row_velocity == 0:
            ticks_to_row_collision = None
        else:
            ticks_to_row_collision = math.ceil( (row - self.row_low) / abs(row_velocity) )

        if col_velocity > 0:
            ticks_to_col_collision = math.ceil( (self.col_high - col) / col_velocity )
        elif col_velocity == 0:
            ticks_to_col_collision = None
        else:
            ticks_to_col_collision = math.ceil( (col - self.col_low) / abs(col_velocity) )



        # Determine true collision point, and consequent velocity
        if ticks_to_row_collision != None and ticks_to_col_collision != None:
            ticks_to_collision = min( ticks_to_row_collision, ticks_to_col_collision )

            # Determine resulting velocity. It will be cached
            if ticks_to_col_collision == ticks_to_row_collision:
                next_velocity[0] = -start_velocity[0]
                next_velocity[1] = -start_velocity[1]
            elif ticks_to_row_collision < ticks_to_col_collision:
                next_velocity[0] = -start_velocity[0]
            elif ticks_to_col_collision < ticks_to_row_collision:
                next_velocity[1] = -start_velocity[1]

        elif ticks_to_row_collision != None and ticks_to_col_collision == None:
            ticks_to_collision = ticks_to_row_collision
            next_velocity[0] = -start_velocity[0]
        elif ticks_to_row_collision == None and ticks_to_col_collision != None:
            ticks_to_collision = ticks_to_col_collision
            next_velocity[1] = -start_velocity[1]
        else:
            # Stationary node
            ticks_to_collision = None
            return solution

        # We now have ticks till collision. Determine point of collision, which will
        # indicate the END of a trajectory segment
        collision_point = [row + ticks_to_collision * row_velocity,
                           col + ticks_to_collision * col_velocity]

        solution.append((start_position, collision_point, next_velocity))

        return self.solve( collision_point,
                           next_velocity,
                           segment_i - 1,
                           solution)

class Player:
    def __init__(self, screen, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        self.color = (0, 255, 0)
        self.radius = 10
        self.trajectory = Trajectory(row, col,
                                     row_velocity, col_velocity,
                                     self.radius, screen.get_height() - self.radius,
                                     self.radius, screen.get_width() - self.radius)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.trajectory.position, self.radius)
        self.drawTrajectory(screen)

    def drawTrajectory(self, screen, ticks_into_future=100):
        '''
        Trajectory is always linear, and is represented as a sequence of lines
        :return:
        '''
        red = 0
        blue = 0
        for segment in self.trajectory.segments:
            pygame.draw.line(screen, (red,255,blue), segment[0], segment[1])
            pygame.display.update()
            red = (red + 50) % 256
            blue = (blue + 50) % 256

    def move(self):
        self.trajectory.move()

class Jedi(Player):
    '''
    Jedis try ONLY try to maximize average resources points to Jedi collectively.
    Upon impact with Jedi, Jedis will split their resource points evenly.
    Upon impact with Sith, Sith steals resource points from Jedi and reallocs
    the gained resources to its own resources.
    '''
    def __init__(self, screen, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        super().__init__(screen, row, col, row_velocity, col_velocity, sources)

        self.color = (0, 0, 255)

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
    def __init__(self, screen, row=0, col=0, row_velocity=0, col_velocity=0, sources=100):
        super().__init__(screen, row, col, row_velocity, col_velocity, sources)

        self.color = (255, 0, 0)

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

    def addPlayer(self, newb):
        '''
        Creates a new player, with random position in arena
        '''

        newb.draw(self.screen)
        self.players.add(newb)
        pygame.display.update()

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
            player.move()
            player.draw(self.screen)
            pygame.display.update()

        # Draw and increment time
        pygame.display.update()
        self.clock.tick(60)

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
                if event.button == 1:
                    arena.addPlayer(Jedi(screen,
                                         randrange(screen.get_height()),
                                         randrange(screen.get_width()),
                                         randrange(10),
                                         randrange(10)))
                elif event.button == 3:
                    arena.addPlayer(Sith(screen,
                                         randrange(screen.get_height()),
                                         randrange(screen.get_width()),
                                         randrange(10),
                                         randrange(10)))
                print(pygame.mouse.get_pos())
            elif event.type == pygame.QUIT:
               simulating = False

        # Iterate the arena
        arena.incrementTime()

if __name__ == '__main__':
    exit(main())