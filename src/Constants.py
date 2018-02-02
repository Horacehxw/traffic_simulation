
'''
Store list of constants
'''
# Probability of Auto/Car, Car/Truck
PROB_AUTO = 0.5
PROB_TRUCK = 0.5 #Prob car actually

# minimum insertion gap
INSERT_GAP = 10

# boundary car distance
BOUNDARY_DISTANCE = 200

# update time interval
TIME_STEP = 0.5

# s* function
DELTA = 4.0

# car length
LEN_CAR = 3
LEN_TRUCK = 5

# highway speed limit
SPEED_LIMIT_KMH = 96 #kmh

############LaneChange parameters#####################
# safety
MAIN_BSAVE = 6. #加速度最小是-6
MAIN_BSAVE_CAR = 9. # max deceleration
MAIN_BSAVE_TRUCK = 8.
MAIN_SMIN = 5. # gap for change lane

# lane-change incentive
BIAS_RIGHT_CAR = 0.
BIAS_RIGHT_TRUCK = 0.
BIAS_RIGHT_AUTO = 0.

P_FACTOR_CAR = 0.2 # Politeness
P_FACTOR_TRUCK = 0.3
P_FACTOR_AUTO = 1

DB_CAR = 0.3 # change lane threshold
DB_TRUCK = 0.2
DB_AUTO = 0

# time to check lane change
T_DELAY_CHANGE = 1.6


############## IDM parameters ######################
# designed maximum speed
V0_INIT_CAR_KMH = 120 # this is in KMH 112.65KMH = 70 mph
V0_INIT_TRUCK_KMH = 90

S0_INIT_HUMAN = 3 # minimum distance allowed
S0_INIT_AUTO = 2

# reaction time !!!
T_REACTION_HUMAN = 1.5
T_REACTION_AUTO = 0

# acceleration factor
A_INIT_CAR_MSII = 0.5
A_INIT_TRUCK_MSII = 0.4

# braking factor
B_INIT_CAR_MSII = 3.0 # b in IDM parameter
B_INIT_TRUCK_MSII = 2.0


