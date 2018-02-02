from Constants import *
import numpy as np

from Moveable import Moveable


'''
    Implementation of the lane-changing model MOBIL                             
    ("Minimizing Overall Brakings Induced by Lane-changes"), see <a             
        href="http://141.30.51.183/~treiber/publications/MOBIL.pdf"> M. Treiber and 
        D. Helbing, Realistische Mikrosimulation von Stra�enverkehr mit einem       
        einfachen Modell </a>, 16. Symposium "Simulationstechnik ASIM 2002" Rostock,
        10.09 -13.09.2002, edited by Djamshid Tavangarian and Rolf Gr\"utzner pp.   
        514--520.

    Horace He: add support for multi lane change
        idea: when it check about changing a lane, check both right and left if possible

    This is a "static class" only the logic of lane change, actual change happens in Street.                                                                   
'''


class LaneChange():
    '''
    Implementation of the lane-changing model MOBIL
    ("Minimizing Overall Brakings Induced by Lane-changes")

    LEFT = -1
    RIGHT = 1

    '''
    def __init__(self, p, db, gap_min=MAIN_SMIN, bsave=MAIN_BSAVE_CAR, bias_right=0):
        '''
        :param p: politeness factor
        :param db: change lane incentive penalty
        :param gap_min: max safe distance
        :param bsave: max safe braking deceleration
        :param bias_right: bias (m/s^2) to drive right
        '''
        self.p, self.db, self.gap_min, self.bsave, self.bias_right = \
                        p, db, gap_min, bsave , bias_right

    def set_bias_right(self, bias):
        self.bias_right = bias


    def change_ok(self, me: Moveable, f_old: Moveable, b_old: Moveable,
                    f_new: Moveable, b_new: Moveable):
        '''
        :param me: the current car
        :param f_old: forward car old
        :param b_old: .. (maybe useless but keep for further use)
        :param f_new: ..
        :param b_new: ..
        :return: bool
            change or not
        '''
        #assert isinstance(me, Moveable) and isinstance(f_new, Moveable)
        # is 1 if new lane is on the right, else 0
        is_right = int(f_new.lane > me.lane)
        # check whether there's enough gap to change lane
        if (me.distance_to(f_new) <= self.gap_min or
                b_new.distance_to(me) <= self.gap_min):
            return False

        # check safety criterion (a > -bsave)
        # this means we need a immediate braking after switch lane
        b_new_acc = b_new.model.calc_acc(b_new, me)
        me_new_acc = me.model.calc_acc(me, f_new)
        if (b_new_acc < -self.bsave or me_new_acc < -self.bsave):
            return False

        # my advantage of acceleration on lane change
        me_acc_adv = me_new_acc - me.model.calc_acc(me, f_old) + \
                            is_right * self.bias_right
        b_new_acc_disadv = b_new.model.calc_acc(b_new, f_new) - b_new_acc
        # this means new back car gets more acceleration for my switch
        #   counter-intuitive case...
        if b_new_acc_disadv < 0:
            b_new_acc_disadv = 0
        return me_acc_adv - self.p * b_new_acc_disadv > self.db

