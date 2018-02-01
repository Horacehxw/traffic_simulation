from interface import Interface

'''
Moveable represents a general vehicle object with position, velocity eyc. In
 * each time step, the objects are updated by moving them forward (method
 * translate), by changing the velocity (method accelerate), and, in time steps
 * where timeToChange return true, by possibly changing the lane (method change) 
 * Implementations of this interface include
 *     Car: all "normal" cars and trucks
 *     Obstacle: These are implemented by immobile vehicles
 *     BCCar: These are introduced for bookkeeping purposes, only to make sure
 * that any Car has a predecessor required for calculating the acceleration.
'''

class Moveable(Interface):

    def time_to_change(self, dt):
        pass

    def translate(self, dt):
        pass

    def accelerate(self, dt, fwd=None):
        pass

    def acceleration(self, fwd=None):
        pass

    def distance_to(self, fwd):
        '''
        return fwd.pos - self.pos - self.length
        '''
        pass

    def change(self, f_old, b_old, f_new, b_new):
        pass