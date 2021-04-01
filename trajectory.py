import math
import pygame
import sympy as sym

class Trajectory:
    def __init__(self, row=0, col=0,
                 row_velocity=0, col_velocity=0,
                 row_low=0, row_high=100, col_low=0, col_high=100,
                 mass=1):
        # Set boundaries
        self.row_high = row_high
        self.row_low = row_low
        self.col_high = col_high
        self.col_low = col_low

        # Kinetics
        self.mass     = mass
        self.position = [row, col]
        self.velocity = [row_velocity, col_velocity]


        # Trajectory representation as list of linear segments
        # Note the longest path is the diagonal
        self.foresight_ticks = math.ceil(math.sqrt( (col_high - col_low)**2 + (row_high - row_low)**2))
        self.n_segments = 4
        self.segments = []
        self.solve(self.position, self.velocity, self.n_segments, self.segments)

    def move(self, screen):
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
                # The segment is done. Clear it, and add a new segment
                old_segment = self.segments.pop(0)
                pygame.draw.line(screen, (0,0,0), old_segment[0], old_segment[1])
                self.velocity = next_velocity

                # Replaced the used up segment by appending a new one
                final_segment = self.segments[-1]
                final_position = final_segment[1]
                final_velocity = final_segment[2]
                next_trajectory = self.solve(final_position,
                                             final_velocity,
                                             0,
                                             self.segments)
        return self.position

    def reset(self, screen):
        # Clear the old segments
        for s in self.segments:
            pygame.draw.line(screen, (0,0,0), s[0], s[1])

        self.segments = []
        self.solve(self.position, self.velocity, self.n_segments, self.segments)

    def isStationary(self):
        return self.velocity == [0, 0]

    def getPosition(self):
        return self.position

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

    def solveCollisionRowVelocity(self, player):
        '''

        :return: consequent row velocity
        '''

        m1 = self.mass
        v1 = self.velocity[0]
        m2 = player.trajectory.mass
        v2 = player.trajectory.velocity[0]


        # Compute conserved momentum
        M = m1*v1 + m2*v2

        # Compute conserved kinetic energy
        K = 0.5*m1*v1**2 + 0.5*m2*v2**2

        # Represent the system of equations for solutions
        v1_f, v2_f = sym.symbols('v1_f, v2_f')
        f1 = sym.Eq(v1_f + v2_f, M)
        f2 = sym.Eq(0.5*m1*v1_f**2 + 0.5*m2*v2_f**2, K)

        # Solve the system
        solution = sym.solve([f1, f2], (v1_f, v2_f))
        return solution[0]

    def solveCollisionColVelocity(self, player):
        '''

        :return: consequent col velocity
        '''

        m1 = self.mass
        v1 = self.velocity[1]
        m2 = player.trajectory.mass
        v2 = player.trajectory.velocity[1]

        # Compute conserved momentum
        M = m1 * v1 + m2 * v2

        # Compute conserved kinetic energy
        K = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2

        # Represent the system of equations for solutions
        v1_f, v2_f = sym.symbols('v1_f, v2_f')
        f1 = sym.Eq(v1_f + v2_f, M)
        f2 = sym.Eq(0.5 * m1 * v1_f ** 2 + 0.5 * m2 * v2_f ** 2, K)

        # Solve the system
        solution = sym.solve([f1, f2], (v1_f, v2_f))
        return solution[1]


    def collidePlayer(self, screen, player):
        '''
        Kinematics for collision of two bodies of mass. Nullifies previous trajectories and replaces with new
        trajectories based on kinematic collision.

        Unit mass is used, for simplification, for now.

        We use conservation of energy and conservation of momentum to solve for two unknowns
        '''

        row_velocities = self.solveCollisionRowVelocity(player)
        col_velocities = self.solveCollisionColVelocity(player)

        self.velocity[0] = row_velocities[0]
        player.trajectory.velocity[0] = row_velocities[1]

        self.velocity[1] = col_velocities[0]
        player.trajectory.velocity[1] = col_velocities[1]

        self.move(screen)
        player.trajectory.move(screen)

        self.reset(screen)
        player.trajectory.reset(screen)

    def draw(self, screen):
        for segment in self.segments:
            '''
            Trajectory is always linear, and is represented as a sequence of lines
            :return:
            '''
            red = 0
            blue = 0
            for segment in self.segments:
                pygame.draw.line(screen, (red, 255, blue), segment[0], segment[1])
                pygame.display.update()
                red = (red + 50) % 256
                blue = (blue + 50) % 256

