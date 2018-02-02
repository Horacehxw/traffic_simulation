from Cars import *
from Constants import *
from CarFactory import *
from LaneChange import *
from IDM import *
from numpy.random import shuffle
import numpy as np



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
        self.time, self.flow_out_speed, self.flow_in_speed = 0, 0, 0
        self.vehicle_wait, self.vehicle_in, self.vehicle_out = 0, 0, 0

    def update(self, q_in):
        self.time += self.dt
        #self.assertion() # debug
        self.insert_BC() # add boundary
        self.accelerate() # calculate new velocity
        self.change_lanes()
        self.clear_BC() # remove boundary

        self.translate() # pos += vel * dt
        self.sort() # derease order of car.pos

        self.io_flow(q_in)
        if self.time % 100 == 0:
            self.calc_io_flow()
        # report current flow information

    def report(self):
        self.vehicle_in, self.vehicle_out = 0, 0

        vels = [car.vel for car in self.street]
        lane_count = np.zeros(self.num_lane)
        for car in self.street:
            lane_count[car.lane] += 1
        print("-----------------------------------------------------------------")
        print ("time = {:5.2f}".format(self.time))
        print("total vehicle: {:4}, average speed {:4.2f}, flow in {:3.2f} vehicle/s, flow out {:3.2f} vehicle/s"\
              .format(len(self.street), np.average(vels), self.flow_in_speed, self.flow_out_speed))
        # print("\t min speed: {:4.2f}, max speed: {:4.2f}".format(np.min(vels), np.max(vels)))
        print("\t num cars in each lane {}".format(lane_count))
        print("-----------------------------------------------------------------")

######################### Private Method Below ##########################################
    def calc_io_flow(self):
        self.flow_in_speed = self.vehicle_in / (self.dt * 100)
        self.flow_out_speed = self.vehicle_out / (self.dt * 100)


    def assertion(self):
        '''
        only debug use: make sure the order is preserved
        :return:
        '''
        for lane in range(self.num_lane):
            idx = self.last_index_on_lane(lane)
            next_id = self.next_index_on_lane(lane, idx)
            while(idx != -1 and next_id != -1):
                assert (self.street[idx].distance_to(self.street[next_id]) > 0)
                idx = next_id
                next_id = self.next_index_on_lane(lane, idx)
        for idx in range(1, len(self.street)):
            assert (self.street[idx-1].pos >= self.street[idx].pos)



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
                f_old = self.street[self.next_index_on_lane(car.lane, idx)]
                b_old = self.street[self.prev_index_on_lane(car.lane, idx)]
                f_new = self.street[self.next_index_on_lane(lane, idx)]
                b_new = self.street[self.prev_index_on_lane(lane, idx)]
                if car.change(f_new=f_new, f_old=f_old, b_new=b_new, b_old=b_old):
                    self.street[idx].lane = lane

    def io_flow(self, q_in):
        '''
        Handle the in and out flow of the street
        The flow-in car is assigned to each lane with equivalent probability.
            max flow-in per update is the number of lanes

        :param q_in: number of vehicle per second
        '''
        self.o_flow()
        self.i_flow(q_in)


    def i_flow(self, q_in):
        # in
        self.vehicle_wait += q_in * self.dt  # add to waitlist
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
                    self.street.append(self.carfatory.create_vehicle(0, distance, lane))
                    self.vehicle_in += 1

    def o_flow(self):
        # out
        origin = len(self.street)
        self.street = [car for car in self.street if car.pos < self.road_length]
        self.vehicle_out += origin - len(self.street)

class StreetRamp(Street):
    # TODO: use delegation instead of inheritance for more control on the strange bias_right factor
    '''
    Let lane 0 be the on ramp, where the road is closed from 1/3 of the roadlength.
    '''
    RAMP = 0
    MERGE_POS = 0.33

    def __init__(self, num_lane, road_length, car_factory, ramp_prob, dt = TIME_STEP):
        '''
        :param num_lane: this is main lane number, the on ramp is automatically added
        :param road_length:
        :param car_factory:
        :param ramp_prob:
        :param dt:
        '''
        assert(num_lane > 0)
        super().__init__(num_lane+1, road_length, car_factory, TIME_STEP)
        self.ramp_prob = ramp_prob
        self.wait_main = 0
        self.wait_ramp = 0
        self.street.append(Obstacle(x=self.road_length * self.MERGE_POS, lane = self.RAMP, length = self.road_length * (1-self.MERGE_POS)))

    def i_flow(self, q_in):
        self.wait_main += q_in * (1-self.ramp_prob)
        self.wait_ramp += q_in * self.ramp_prob

        if self.wait_ramp > 1:
            idx_fwd = self.last_index_on_lane(self.RAMP)
            if idx_fwd == -1:
                distance = self.road_length
            else:
                distance = self.street[idx_fwd].pos

            if distance >= INSERT_GAP:
                self.wait_ramp -= 1
                car = self.carfatory.create_vehicle(0, distance, self.RAMP)
                # TODO: restore this parameter after merge to main road.
                car.lane_change.bias_right = 1. # they are more likely to turn to main road
                self.street.append(car)
                self.vehicle_in += 1


        lanes = np.arange(1, self.num_lane); shuffle(lanes)
        for lane in lanes:
            if self.wait_main > 1:
                idx_fwd = self.last_index_on_lane(lane)
                if idx_fwd == -1:
                    distance = self.road_length
                else:
                    distance = self.street[idx_fwd].pos

                if distance >= INSERT_GAP:
                    self.wait_main -= 1
                    self.street.append(self.carfatory.create_vehicle(0, distance, lane))
                    self.vehicle_in += 1

class StreetAuto():
    '''
    One lane exclusive use for autonomous cars.
    '''

    def __init__(self, num_lane, road_length, auto_prob, ramp_prob, car_prob = 0.8, dt = TIME_STEP, num_auto = 1):
        assert(num_lane > num_auto)
        car_factory_auto = CarFactory(1, car_prob)
        car_factory_human = CarFactory(0, car_prob)
        self.main_road = StreetRamp(num_lane-num_auto, road_length, car_factory_human, ramp_prob, dt)
        self.auto_road = StreetRamp(num_auto, road_length, car_factory_auto, ramp_prob, dt)
        self.auto_prob = auto_prob

    def update(self, q_in):
        self.main_road.update(q_in * (1 - self.auto_prob))
        self.auto_road.update(q_in * self.auto_prob)

    def report(self):
        self.auto_road.vehicle_in, self.auto_road.vehicle_out = 0, 0
        self.main_road.vehicle_in, self.main_road.vehicle_out = 0, 0

        avg1 = np.sum([car.vel for car in self.main_road.street])
        avg2 = np.sum([car.vel for car in self.auto_road.street])
        avg = (avg1 + avg2)/(1+len(self.main_road.street) + len(self.auto_road.street))
        print("-----------------------------------------------------------------")
        print("time = {:5.2f}".format(self.main_road.time))
        print("total vehicle: {:4}, average speed {:4.2f}" \
              .format(len(self.main_road.street) + len(self.auto_road.street), avg))
        # print("\t min speed: {:4.2f}, max speed: {:4.2f}".format(np.min(vels), np.max(vels)))
        #print("\t num cars in each lane {}".format(lane_count))
        print("-----------------------------------------------------------------")
