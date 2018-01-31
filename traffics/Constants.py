
'''
Store list of constants
'''

# s* function
DELTA = 4.0

############LaneChange parameters#####################
# safety
MAIN_BSAVE = 12.
MAIN_BSAVE_SELF = 12.
MAIN_SMIN = 2.

# lane-change incentive
BIAS_RIGHT_CAR = 0.1
BIAS_RIGHT_TRUCK = 0.3
BIAS_RIGHT_AUTO = 0
P_FACTOR_CAR = 0.2 # Politeness
P_FACTOR_TRUCK = 0.2
P_FACTOR_AUTO = 1
DB_CAR = 0.3 # change lane threshold
DB_TRUCK = 0.2
DB_AUTO = 0


############## IDM parameters ######################
# designed maximum speed
V0_INIT_CAR_KMH = 120 # this is in KMH 112.65KMH = 70 mph
V0_INIT_TRUCK_KMH = 90
V0_INIT_AUTO_KMH = 120

S0_INIT_CAR = 3 # minimum distance allowed
S0_INIT_TRUCK = 3
S0_INIT_AUTO = 2

# reaction time !!!
T_REACTION_CAR = 1.5
T_REACTION_TRUCK = 1.5
T_REACTION_AUTO = 0

# acceleration factor
A_INIT_CAR_MSII = 0.5
A_INIT_TRUCK_MSII = 0.4

# braking factor
B_INIT_CAR_MSII = 3.0 # b in IDM parameter
B_INIT_TRUCK_MSII = 4.0
B_INIT_AUTO_MSII = 3.0
MAX_BRAKING = 20.0 # maximum deceleration