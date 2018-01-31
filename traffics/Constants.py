
'''
Store list of constants
'''

# s* function
DELTA = 4.0

# car length
LEN_CAR = 3
LEN_TRUCK = 5

############LaneChange parameters#####################
# safety
MAIN_BSAVE_CAR = 9. # max deceleration
MAIN_BSAVE_TRUCK = 8.
MAIN_SMIN = 2. # gap for change lane

# lane-change incentive
BIAS_RIGHT_CAR = 0.1
BIAS_RIGHT_TRUCK = 0.3
BIAS_RIGHT_AUTO = 0

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
B_INIT_TRUCK_MSII = 4.0
