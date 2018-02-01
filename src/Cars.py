from interface import implements
from Moveable import Moveable
from LaneChange import LaneChange
from IDM import IDM
from Constants import *


class Car(implements(Moveable)):
    '''
    Instantiation for real cars.
    '''

    def __init__(self, x, v, lane, model: IDM, lane_change: LaneChange,
                 length):
        self.pos, self.vel, self.lane, self.model, self.lane_change, \
            self.length = x, v, lane, model, lane_change, length
        self.acc = 0  # current acceleration
        self.acc_history = 0 # acc 1 calculation before
        self.tdelay = 0  # cumulative waiting time
        self.Tdelay = T_DELAY_CHANGE  # time to check whether change lane or not

    def __copy__(self):
        return Car(self.pos, self.vel, self.lane, self.model, self.lane_change, \
                   self.length)

    def time_to_change(self, dt):
        '''
        Count the wait time to check whether to change lane or not.
        :param dt: update time interval
        :return: bool, whether the cumulative time exceed threshold
        '''
        self.tdelay += dt
        if self.tdelay > self.Tdelay:
            self.Tdelay -= self.tdelay
            return True
        return False

    def translate(self, dt):
        self.pos += dt * self.vel

    def accelerate(self, dt, fwd=None):
        '''
        Need to calculate the acceleration before call it
        '''
        assert (fwd == None)
        if fwd != None:
            self.acceleration(fwd)
        self.vel += self.acc * dt
        if (self.vel < 0.):
            self.vel = 0.

    def acceleration(self, fwd=None):
        if fwd == None:
            return self.acc
        else:
            return self.model.calc_acc(self, fwd)

    def distance_to(self, fwd):
        return fwd.pos - self.pos - self.length

    def change(self, f_old, b_old, f_new, b_new):
        return self.lane_change.change_ok(self, f_old,
                                          b_old, f_new, b_new)

class CarHuman(Car):
    '''
    Human is stupid, their reaction is delayed by a time interval.

    '''
    acc_history = 0

    def accelerate(self, dt, fwd=None):
        '''
        Need to calculate the acceleration before call it
        '''
        if fwd != None:
            self.acceleration(fwd)
        self.vel += self.acc_history * dt
        self.acc_history = self.acc
        if (self.vel < 0.):
            self.vel = 0.

class BCCar(implements(Moveable)):
    '''
    virtual cars so that acceleration, lanechange etc
    always defined (they need in general all next neighbours)
    '''

    def __init__(self, x, v, lane, model, length=0):
        self.pos, self.vel, self.lane, self.model, self.length = \
            x, v, lane, model, length

    @property
    def lane_change(self):
        return None

    @lane_change.setter
    def lane_change(self, lanechange):
        pass

    def time_to_change(self, dt):
        return False

    def translate(self, dt):
        pass

    def accelerate(self, dt, fwd=None):
        pass

    def acceleration(self, fwd=None):
        return 0.

    def distance_to(self, fwd):
        return fwd.pos - self.pos - self.length

    def change(self, f_old, b_old, f_new, b_new):
        pass


class Obstcle(implements(Moveable)):
    '''
    model necessary since obstacle=type "Moveable" and lane change checks
    acceleration! influences 3 following locations labeld with xxx
    '''

    def __init__(self, x, lane, length=0):
        class MicroModelOb():
            def calc_acc(self, bwd, vwd):
                return 0

            def Veq(self, dx):
                return 0

        self.pos, self.lane, self.length = x, lane, length
        self.vel = 0
        self.model = MicroModelOb()

    @property
    def lane_change(self):
        return None

    @lane_change.setter
    def lane_change(self, lanechange):
        pass

    def time_to_change(self, dt):
        return False

    def translate(self, dt):
        pass

    def accelerate(self, dt, fwd=None):
        pass

    def acceleration(self, fwd=None):
        return 0.

    def distance_to(self, fwd):
        return fwd.pos - self.pos - self.length

    def change(self, f_old, b_old, f_new, b_new):
        return False

