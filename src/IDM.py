import numpy as np

from Moveable import Moveable
from Constants import *

'''
Basis classes for the microscopic traffic model IDM (intelligent-driver model,
 * see <a href="http://xxx.uni-augsburg.de/abs/cond-mat/0002177"> M. Treiber, A.
 * Hennecke, and D. Helbing, Congested Traffic States in Empirical Observations
 * and Microscopic Simulations, Phys. Rev. E 62, 1805 (2000)].</a> <br>
 * <br>

IDM:
    general IDM follower strategy realization

IDMAuto:
    IDM + autonomous car cooperation.
    e.g. IDMAuto cars can lock on the forward car if they are close enough and have same speed.
         Once locked, the backward car's acceleration is overwritten by the forward one.
         Besides, the backward car will change its distance between forward into s0 gradually
            by adding \delta m more every update.
'''

class IDM():
    '''
    The IDM is a static class for calculation based on condition of specific car.
    It is shared between all the cars with the same

    ismax； max distance effect for the car following model.
    MAX_BRAKING: max deceleration m/s^2
    '''

    # ismax specify the distance where
    ismax = 100 # ve(s) = ve(ismax) if s > ismax

    def __init__(self, v0, a, b, s0=2, T=1.5):
        '''

        :param v0:
            max speed of the car
        :param delta:
            technical term in the acc calculation
        :param a:
            max acceleration m/s^2
        :param b:
            normal deceleration m/s^2
        :param s0: default 2
            least safe distance between two cars
            --> exceed this means need to brake immediately
        :param T:  default 1.5
            human reaction time T for s*
        '''
        self.v0, self.delta, self.a, self.b, self.s0,  \
            self.T = v0, DELTA, a, b, s0, T
        self.sqrtab = np.sqrt(a*b)
        self.veq_table = np.zeros(self.ismax + 1)
        self.initialize() #generate equilibrium velocity table


    def initialize(self):
        dt = 0.5 #relaxation timestep 0.5s
        kmax = 20 #number of iteration in relaxation
        for s in range(1, self.ismax+1):
            Ve = self.veq_table[s-1]
            for k in range(0, kmax):
                s_star = self.s0 + Ve*self.T
                acc = self.a * (1.-np.power(Ve/self.v0, self.delta) - (s_star**2) / (s**2))
                Ve += acc * dt
                Ve = max(Ve, 0) # can't be lower
            self.veq_table[s] = Ve

    def Veq(self, dx):
        '''
        function for equilibrium velocity using veq_table;
            ve(s>ismax)=ve(ismax)
        this value is used to set up initial speed of vehicle
        :param dx: the distance between the current and forward car
        :return: velocity in m/s
        '''
        s = int(np.floor(dx))
        V = 0
        if s < 0:
            pass # V=0
        elif s < self.ismax:
            rest = dx - s
            V = (1-rest) * self.veq_table[s] + rest * self.veq_table[s+1]
        else:
            V = self.veq_table[self.ismax]
        return V



    def calc_acc(self, bwd: Moveable, fwd: Moveable):
        '''
        :param bwd: Moveable, The current vehicle
        :param fwd: Moveable, The vehicle in the forward vehicle
        :return: acceleration m/s^2
        '''
        delta_v = bwd.vel - fwd.vel
        s = bwd.distance_to(fwd)
        vel = bwd.vel
        s_star_raw = self.s0 + vel * self.T\
                        + (vel * delta_v) / (2 * self.sqrtab)
        s_star = max(s_star_raw, self.s0)
        acc = self.a * (1 - np.power(vel / self.v0, self.delta) - (s_star **2) / (s**2))
        acc = max(acc, -MAIN_BSAVE)
        return acc

    def get_v0(self):
        '''
        get maximum designed speed of this vehicle
        '''
        return self.v0

class IDMAuto(IDM):
    ROUND_VEL = 1e-2

    def calc_acc(self, bwd: Moveable, fwd: Moveable):
        '''
        Define the special following behavior between autonomous cars
        '''
        if (isinstance(fwd.model, IDMAuto)):
            v1, v2 = bwd.vel, fwd.vel
            pos1, pos2 = bwd.pos, fwd.pos
            # The fwd's acceleration must be already clear
            # use one pass calcAcc then do the real acceleration
            # "lock" the autonomous vehicles
            if np.isclose(v1, v2, atol=self.ROUND_VEL):
                assert(pos1 < pos2) # make sure fwd is really forward
                acc = v2 - v1 + fwd.acc #syncronize the speed, then the acc is the same
                if bwd.distance_to(fwd) > self.s0:
                    acc = max(self.a, acc+.2) #can't exceed the maximum value
                return acc
        return super().calc_acc(bwd, fwd)

