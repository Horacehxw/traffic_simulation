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
    def set_position(self, x):
        pass

    def set_velocity(self, v):
        pass

    def set_lane(self, lane):
        pass

    def set_model(self, model):
        pass

    def set_lane_change(self, lane_change):
        pass

    def set_length(self, length):
        pass

    # def set_color(self, color):
    #     pass

    def position(self):
        '''
        :return: meters from start of road
        '''
        pass

    def velocity(self):
        '''
        :return: m/s
        '''
        pass

    def lane(self):
        pass

    # def color(self):
    #     pass

    def length(self):
        pass

    def model(self):
        pass

    def change(self, f_old, b_old, f_new, b_new):
        pass

    def time_to_change(self, dt):
        pass

    def translate(self, fwd):
        pass

    def accelerate(self, dt, fwd):
        pass

    def acceleration(self):
        pass

    def acceleration(self, fwd):
        pass

    def distance_to(self, other):
        pass