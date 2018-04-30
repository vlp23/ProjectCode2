import numpy as np

# Updated the simulation length to be 20 years based on the study and Delta T to be monthly (1/52) from Methods- Decision Model
# What is the population size?

POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 20     # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate
DELTA_T = 1/12      # years (length of time step, how frequently you look at the patient)

# Part 1: Annual mortality rates (Well -> Non-Stroke Death)
# For Aspirin and Aspirin/Clopidogrel dual platelet therapy
a = 0.0420
# For Warfarin
b = 0.0400
# For both doses of Dabigatran
c = 0.0390

# Part 2: Annual Stroke Rates (Well -> Stroke)
# Aspirin (base case)
d = 0.0270
# Aspirin and Clopidogrel, based on RR of 0.73
e = 0.0197
# Warfarin, based on RR of 0.44
s = 0.0118
# Dabigatran vs. Warfarin 110mg, based on RR of 1.11 of Warfarin therapy
f =  0.0132
#Dabigatran vs. Warfarin 150mg, based on RR of 0.76 of Warfarin therapy
g = 0.0090

#Part 3: Probabilities of (Stroke -> Minor/Major/TIA/Stroke-Death/no-residual effect)
# TIA (for all therapies)
p = 0.2800
# Probabilities of stroke on aspirin or aspirin/clopidogrel that were...
# minor
h = 0.4100
# major
i = 0.3000
# fatal (Stroke-Death)
j = 0.1790
# no residual
k = 0.1100

#Probabilities of stroke on warfarin and dabigatran that were...
# minor
l = 0.4250
# major
m = 0.4020
# fatal (Stroke-Death)
n = 0.0820
# no residual
o = 0.0910


# Part 4: Rate of recurrent stroke (annual) (Post-Stroke -> TIA/Minor/Major)
recur_stroke_rate = 2.6

# Part 5: Rate of transition from Stroke state to Post-stroke state (annual)
q = 1/(1/52)

# Part 6: Transition rate matrices on base case and 4 therapies


# transition rate matrix (aspirin)
TRANS_MATRIX_ASPIRIN = [
    [None,  d*h,  d*i, d*p, d*j, 0.0, a],  # Well
    [0.0,   None, 0.0, 0.0, 0.0, q, 0.0],  # Minor Stroke
    [0.0, 0.0, None, 0.0, 0.0, q, 0.0],    # Major Stroke
    [0.0, 0.0, 0.0, None, 0.0, q, 0.0],    # TIA
    [0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0],  # Stroke-Death
    [0.0, d*h*recur_stroke_rate, d*i*recur_stroke_rate, d*p*recur_stroke_rate, d*j,   None,  a],   # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
    ]

# transition rate matrix (aspirin/clopidogrel)
TRANS_MATRIX_DUAL = [
    [None,  e*h,  e*i, e*p, e*j, 0.0, a],  # Well
    [0.0,   None, 0.0, 0.0, 0.0, q, 0.0],  # Minor Stroke
    [0.0, 0.0, None, 0.0, 0.0, q, 0.0],    # Major Stroke
    [0.0, 0.0, 0.0, None, 0.0, q, 0.0],    # TIA
    [0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0],  # Stroke-Death
    [0.0, e*h*recur_stroke_rate, e*i*recur_stroke_rate, e*p*recur_stroke_rate, e*j,   None,  a],   # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
    ]

# transition rate matrix (Warfarin)
TRANS_MATRIX_WARFARIN = [
    [None,  s*l,  s*m, s*p, s*j, 0.0, b],  # Well
    [0.0,   None, 0.0, 0.0, 0.0, q, 0.0],  # Minor Stroke
    [0.0, 0.0, None, 0.0, 0.0, q, 0.0],    # Major Stroke
    [0.0, 0.0, 0.0, None, 0.0, q, 0.0],    # TIA
    [0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0],  # Stroke-Death
    [0.0, s*h*recur_stroke_rate, s*i*recur_stroke_rate, s*p*recur_stroke_rate, s*j,   None,  b],   # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
    ]


# transition rate matrix (Dabigatran 110)
TRANS_MATRIX_DABIGATRAN110= [
    [None,  f*h,  f*i, f*p, f*j, 0.0, c],  # Well
    [0.0,   None, 0.0, 0.0, 0.0, q, 0.0],  # Minor Stroke
    [0.0, 0.0, None, 0.0, 0.0, q, 0.0],    # Major Stroke
    [0.0, 0.0, 0.0, None, 0.0, q, 0.0],    # TIA
    [0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0],  # Stroke-Death
    [0.0, f*h*recur_stroke_rate, f*i*recur_stroke_rate, f*p*recur_stroke_rate, f*j,   None,  c],   # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
    ]


# transition rate matrix (Dabigatran 150)
TRANS_MATRIX_DABIGATRAN150= [
    [None,  g*h,  g*i, g*p, g*j, 0.0, c],  # Well
    [0.0,   None, 0.0, 0.0, 0.0, q, 0.0],  # Minor Stroke
    [0.0, 0.0, None, 0.0, 0.0, q, 0.0],    # Major Stroke
    [0.0, 0.0, 0.0, None, 0.0, q, 0.0],    # TIA
    [0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0],  # Stroke-Death
    [0.0, g*h*recur_stroke_rate, g*i*recur_stroke_rate, g*p*recur_stroke_rate, g*j,   None,  c],   # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
    ]




#annual cost of each health state
ANNUAL_STATE_COST = [
0, #well
2470.0, #minor long term
5400.0, #major long term
625.0, #tia, short term event divided by 12
10000.0, #stroke death copied from non-stroke, nonhemmorage death below
200.0, #poststroke copied from homework
10000.0 #death
]

# annual health utility of each health state

ANNUAL_STATE_UTILITY = [
1.0, #well
0.75, #minor
0.39, #major
0.9, #tia, short term
0.0, #stroke death
0.12, #poststroke
0.0 #death
]

# annual drug costs per year
ASPIRIN_COST = 10.0
DUAL_COST= 1857.0
WARFARIN_COST = 180
DABIGATRAN_COST = 3240.0
