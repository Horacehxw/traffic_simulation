from numpy.random import rand
from IDM import *
from Constants import *
from LaneChange import *
from Cars import *

class CarFactory():
    '''
    Class for generating all kinds of cars by demand
    '''
    def __init__(self, auto_prob, car_prob):
        self.auto_prob, self.car_prob =  auto_prob, car_prob

        self.car_human_IDM = IDM(v0 = V0_INIT_CAR_KMH / 3.6,
                                 a  = A_INIT_CAR_MSII,
                                 b  = B_INIT_CAR_MSII,
                                 s0 = S0_INIT_HUMAN,
                                 T  = T_REACTION_HUMAN)

        self.truck_human_IDM = IDM(v0 = V0_INIT_TRUCK_KMH / 3.6,
                                   a  = A_INIT_TRUCK_MSII,
                                   b  = B_INIT_TRUCK_MSII,
                                   s0 = S0_INIT_HUMAN,
                                   T  = T_REACTION_HUMAN)

        self.car_auto_IDM = IDMAuto(v0 = V0_INIT_CAR_KMH / 3.6,
                                    a  = A_INIT_CAR_MSII,
                                    b  = B_INIT_CAR_MSII,
                                    s0 = S0_INIT_AUTO,
                                    T  = T_REACTION_AUTO)

        self.truck_auto_IDM = IDMAuto(v0 = V0_INIT_TRUCK_KMH / 3.6,
                                      a  = A_INIT_TRUCK_MSII,
                                      b  = B_INIT_TRUCK_MSII,
                                      s0 = S0_INIT_AUTO,
                                      T  = T_REACTION_AUTO)

        self.lane_change_human_car = LaneChange(p = P_FACTOR_CAR,
                                                db = DB_CAR,
                                                gap_min = MAIN_SMIN,
                                                bsave = MAIN_BSAVE_CAR,
                                                bias_right = BIAS_RIGHT_CAR)

        self.lane_change_human_truck = LaneChange(p = P_FACTOR_TRUCK,
                                                  db = DB_TRUCK,
                                                  gap_min = MAIN_SMIN,
                                                  bsave = MAIN_BSAVE_TRUCK,
                                                  bias_right = BIAS_RIGHT_TRUCK)

        self.lane_change_auto_car = LaneChange(p = P_FACTOR_AUTO,
                                                   db = DB_AUTO ,
                                                   gap_min = MAIN_SMIN,
                                                   bsave = MAIN_BSAVE_CAR,
                                                   bias_right = BIAS_RIGHT_AUTO)

        self.lane_change_auto_truck = LaneChange(  p=P_FACTOR_AUTO,
                                                   db=DB_AUTO ,
                                                   gap_min=MAIN_SMIN,
                                                   bsave=MAIN_BSAVE_TRUCK,
                                                   bias_right=BIAS_RIGHT_AUTO)


    def create_vehicle(self, position, initial_gap, lane):
        # car_prob and auto_prob are independent Probability
        if rand() < self.auto_prob:
            if rand() < self.car_prob:
                IDM = self.car_auto_IDM
                lc = self.lane_change_auto_car
                return Car(position, IDM.Veq(initial_gap), lane, IDM, lc, LEN_CAR)
            else:
                IDM = self.truck_auto_IDM
                lc = self.lane_change_auto_truck
                return Car(position, IDM.Veq(initial_gap), lane, IDM, lc, LEN_TRUCK)
        else:
            if rand() < self.car_prob:
                IDM = self.car_human_IDM
                lc =self.lane_change_human_car
                return CarHuman(position, IDM.Veq(initial_gap), lane, IDM, lc, LEN_CAR)
            else:
                IDM = self.truck_human_IDM
                lc = self.lane_change_human_truck
                return CarHuman(position, IDM.Veq(initial_gap), lane, IDM, lc, LEN_TRUCK)