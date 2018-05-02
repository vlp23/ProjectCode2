import ParameterClassesSens1 as P
import MarkovModel as MarkovCls
import SupportMarkovModel150Sens1 as SupportMarkov
#NEW OUTCOMES WHEN THE BASELINE STROKE RATE IS INCREASED
# Dab 150
# create a cohort
cohort_dabigitran150 = MarkovCls.Cohort(id=4, therapy=P.Therapies.DABIGITRAN150)
simOutputs_dabigitran150 = cohort_dabigitran150.simulate()

# Warfarin
# create a cohort
cohort_warfarin= MarkovCls.Cohort(id=1, therapy=P.Therapies.WARFARIN)
simOutputs_warfarin = cohort_warfarin.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_warfarin, simOutputs_dabigitran150)

# print the estimates
SupportMarkov.print_outcomes(simOutputs_dabigitran150, "Dabigitran150 therapy")
SupportMarkov.print_outcomes(simOutputs_warfarin, "Warfarin theraoy")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_warfarin, simOutputs_dabigitran150)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_warfarin,simOutputs_dabigitran150)

