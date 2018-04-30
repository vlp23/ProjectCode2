from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputData as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random


class HealthStats(Enum):
    """ health states of patients with AF """
    WELL = 0
    MINOR_STROKE =1
    MAJOR_STROKE = 2
    TIA = 3
    STROKE_DEATH=4
    POST_STROKE = 5
    NON_STROKE_DEATH = 6



class Therapies(Enum):
    """ Aspirin v dual v warfarin v dabigitran 110 v dabigitran 150 """
    ASPIRIN = 0
    DUAL_THERAPY = 1
    WARFARIN = 2
    DABIGITRAN110 = 3
    DABIGITRAN150 = 4




class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # calculate the adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT*Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # annual treatment cost
        if self._therapy == Therapies.ASPIRIN:
            self._annualTreatmentCost = 10.0
        if self._therapy == Therapies.DABIGITRAN110:
            self._annualTreatmentCost = 3240
        if self._therapy == Therapies.DABIGITRAN150:
            self._annualTreatmentCost = 3240
        else:
            self._annualTreatmentCost = Data.WARFARIN_COST

        # transition rate matrix of the selected therapy
        self._rate_matrix = []
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.ASPIRIN:
            self._rate_matrix = Data.TRANS_MATRIX_ASPIRIN
            # convert rate to probability
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T)
           # print('Upper bound on the probability of two transitions within delta_t:', p)
        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.DABIGITRAN110:
            self._rate_matrix = Data.TRANS_MATRIX_DABIGATRAN110
            # convert rate to probability
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T)
           # print('Upper bound on the probability of two transitions within delta_t:', p)
        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.DABIGITRAN150:
            self._rate_matrix = Data.TRANS_MATRIX_DABIGATRAN150
            # convert rate to probability
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T)
           # print('Upper bound on the probability of two transitions within delta_t:', p)
        else:
            self._rate_matrix = Data.TRANS_MATRIX_WARFARIN
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T)
           # print('Upper bound on the probability of two transitions within delta_t:', p)

        # annual state costs and utilities
        self._annualStateCosts = Data.ANNUAL_STATE_COST
        self._annualStateUtilities = Data.ANNUAL_STATE_UTILITY

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self,state):
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self,state):
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost
