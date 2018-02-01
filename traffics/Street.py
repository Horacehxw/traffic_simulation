from Cars import *
from Constants import *
from CarFactory import *
from LaneChange import *
from IDM import *




class Street():
    '''
    Representation of a multi-lane road section for one direction. The main
    elements of MicroStreet are

        street, a vector of Moveable's representiung the vehicles,
        The *update* method invoked in every time step. Ammong others, it calls all
    emthods mentioned below.
        Methods for moving the vehicles (translate), accelerating them
    (accelerate) and performing the lane changes (changeLanes).
        A sorting routine sort for rearranging the vehicle order in street in the
    order of decreasing longitudinal positions
        The method io_flow implementing the upstream and downstream boundary
    conditions (inflow and outflow).
    '''
    def __init__(self, num_lane, road_length, car_factory, dt = TIME_STEP):
        self.num_lane, self.road_length, self.carfatory,self.dt= \
                num_lane, road_length, car_factory, dt
        self.street = [] # positions sorted in decreasing order
        # num of car need to add, already in/out in this update
        self.vehicle_wait, self.vehicle_in, self.vehicle_out = 0, 0, 0

    def update(self, q_in):
        self.insert_BC() # add boundary
        self.accelerate() # calculate new velocity
        self.change_lanes()
        self.clear_BC() # remove boundary

        self.translate() # pos += vel * dt
        self.sort() # derease order of car.pos
        self.io_flow(q_in)


    def first_index_on_lane(self, lane):
        '''
        :return: index i or -1 if no vehicle on lane
        '''
        if lane >= self.num_lane:
            raise IndexError("max lane = {}".format(lane))
        for idx in range(len(self.street)):
            if self.street[idx].lane == lane:
                return idx
        return -1

    def last_index_on_lane(self, lane):
        if lane >= self.num_lane:
            raise IndexError("max lane = {}".format(lane))
        for idx in range(len(self.street)-1, -1, -1):
            if self.street[idx].lane == lane:
                return idx
        return -1

    def next_index_on_lane(self, lane, idx):
        if lane >= self.num_lane:
            raise IndexError("max lane = {}".format(lane))
        for idx in range(idx-1, -1, -1):
            if self.street[idx].lane == lane:
                return idx
        return -1

    def prev_index_on_lane(self, lane, idx):
        if lane >= self.num_lane:
            raise IndexError("max lane = {}".format(lane))
        for idx in range(idx+1, len(self.street)):
            if self.street[idx].lane == lane:
                return idx
        return -1

    def sort(self):
        '''
        use bubble sort to maintain the decreasing order

        since the order is only change a little after lane change, only need
            2 pass in most cases.
        '''
        sorted = False
        while not sorted:
            sorted = True
            for i in range(1, len(self.street)):
                if self.street[i-1].pos < self.street[i].pos:
                    self.street[i-1], self.street[i] = \
                        self.street[i], self.street[i-1]
                    sorted = False

    def translate(self):
        for car in self.street:
            car.translate(self.dt)

    def accelerate(self):
        for idx in range(len(self.street)):
            fwd = self.next_index_on_lane(self.street[idx].lane, idx)
            self.street[idx].acceleration(self.street[fwd])
        for car in self.street:
            car.accelerate(self.dt)

    def change_lanes(self):
        pass

    def insert_BC(self):
        '''
        set boundary cars so that every one is defined
        :return:
        '''
        dx = BOUNDARY_DISTANCE
        for lane in range(self.num_lane):
            id_first = self.first_index_on_lane(lane)
            id_last = self.last_index_on_lane(lane)
            if id_first == -1:
                first_vel = 0
            else:
                first_vel = self.street[id_first].vel
            if id_last == -1:
                last_vel = 0
            else:
                last_vel = self.street[id_last].vel
            self.street.insert(0, BCCar(self.road_length+dx,
                                        first_vel,
                                        lane,
                                        self.carfatory.car_human_IDM))
            self.street.insert(len(self.street),
                               BCCar(0 - dx,
                                     last_vel,
                                     lane,
                                     self.carfatory.car_human_IDM))

    def clear_BC(self):
        '''
        remove all BCCar classes
        :return:
        '''
        self.street = [car for car in self.street if not isinstance(car, BCCar)]

    def change_lanes(self):
        for idx in range(len(self.street)):
            new_lane = []
            car = self.street[idx]
            # add possible new lanes, otherwise next loop do nothing
            if car.time_to_change(self.dt):
                if car.lane - 1 >= 0:
                    new_lane.append(car.lane - 1) # left is shadowed if right is True
                if car.lane + 1 < self.num_lane:
                    new_lane.append(car.lane + 1) # right first
            for lane in new_lane:
                f_old = self.next_index_on_lane(car.lane, idx)
                b_old = self.prev_index_on_lane(car.lane, idx)
                f_new = self.next_index_on_lane(lane, idx)
                b_new = self.prev_index_on_lane(lane, idx)
                if car.change(f_new=f_new, f_old=f_old, b_new=b_new, b_old=b_old):
                    self.street[idx].lane = lane

    def io_flow(self, q_in):
        from numpy.random import shuffle
        import numpy as np
        '''
        Handle the in and out flow of the street
        The flow-in car is assigned to each lane with equivalent probability.
            max flow-in per update is the number of lanes

        :param q_in: number of vehicle per second
        '''
        # out
        origin = len(self.street)
        self.street = [car for car in self.street if car.pos > self.road_length]
        self.vehicle_out = origin - len(self.street)

        # in
        self.vehicle_wait += q_in * self.dt # add to waitlist
        lanes = np.arange(self.num_lane); shuffle(lanes)
        for lane in lanes:
            if self.vehicle_wait > 1:
                self.vehicle_wait -= 1
                idx_fwd = self.last_index_on_lane(lane)
                if idx_fwd == -1:
                    distance = self.road_length
                else:
                    distance = self.street[idx_fwd].pos

                if distance >= INSERT_GAP:
                    self.street.insert(0,
                                       self.carfatory.create_vehicle(0, distance, lane))




