import ParameterClassesSens1 as P
import MarkovModelSens1 as MarkovCls
import SupportMarkovModel110Sens1 as SupportMarkov
#NEW OUTCOMES WHEN STROKE RATE IS INCREASED
# Dab 110
# create a cohort
cohort_dabigitran110 = MarkovCls.Cohort(id=3, therapy=P.Therapies.DABIGITRAN110)
simOutputs_dabigitran110 = cohort_dabigitran110.simulate()

# Warfarin
# create a cohort
cohort_warfarin= MarkovCls.Cohort(id=1, therapy=P.Therapies.WARFARIN)
simOutputs_warfarin = cohort_warfarin.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_warfarin, simOutputs_dabigitran110)

# print the estimates
SupportMarkov.print_outcomes(simOutputs_dabigitran110, "Dabigitran110 therapy")
SupportMarkov.print_outcomes(simOutputs_warfarin, "Warfarin therapy")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_warfarin,simOutputs_dabigitran110)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_warfarin,simOutputs_dabigitran110)

