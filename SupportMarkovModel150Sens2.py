import InputDataSens2Cost as Settings
import scr.FormatFunctions as F
import scr.StatisticalClasses as Stat
import scr.EconEvalClasses as Econ
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs


def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of time to stroke
    strokes_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_count_strokes().get_mean(),
        interval=simOutput.get_sumStat_count_strokes().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    cost_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_cost().get_mean(),
        interval=simOutput.get_sumStat_discounted_cost().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    utility_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_utility().get_mean(),
        interval=simOutput.get_sumStat_discounted_utility().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean and {:.{prec}%} CI of survival time:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean and {:.{prec}%} CI of time to stroke:".format(1 - Settings.ALPHA, prec=0),
          strokes_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} CI:".format(1 - Settings.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} CI:".format(1 - Settings.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def draw_survival_curves_and_histograms(simOutputs_warfarin, simOutputs_Dabigitran150):
    """ draws the survival curves and the histograms of time until stroke deaths
    :param simOutputs_warfarin: output of a cohort simulated under warfarin therapy
    :param simOutputs_Dabigitran150: output of a cohort simulated under dab 150 therapy
    """

    # get survival curves of both treatments
    survival_curves = [

        simOutputs_warfarin.get_survival_curve(),
        simOutputs_Dabigitran150.get_survival_curve()
    ]

    # graph survival curve
    PathCls.graph_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=['Warfarin', 'Dabigitran150 Therapy']
    )

    # histograms of survival times
    set_of_survival_times = [
        simOutputs_warfarin.get_survival_times(),
        simOutputs_Dabigitran150.get_survival_times()
    ]

    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_survival_times,
        title='Histogram of patient survival time',
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legend=['Warfarin Therapy', 'Dabigitran150 Therapy'],
        transparency=0.6
    )


def print_comparative_outcomes(simOutputs_warfarin, simOutputs_Dabigitran150):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under dab therapy compared to warf therapy
    :param simOutputs_warfarin: output of a cohort simulated under warfarin therapy
    :param simOutputs_Dabigitran150: output of a cohort simulated under dab150 therapy
    """

    # increase in survival time under dab therapy with respect to warf therapy
    increase_survival_time = Stat.DifferenceStatIndp(name="Increase in survival time",
                                                     x=simOutputs_Dabigitran150.get_survival_times(),
                                                     y_ref=simOutputs_warfarin.get_survival_times())
    # estimate and CI
    estimate_CI = F.format_estimate_interval(estimate=increase_survival_time.get_mean(),
                                             interval=increase_survival_time.get_t_CI(alpha=Settings.ALPHA),
                                             deci=2)

    print("Average increase in survival time "
          "and {:.{prec}%} CI:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # increase in discounted total cost under dab therapy with respect to warfarin therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_Dabigitran150.get_costs(),
        y_ref=simOutputs_warfarin.get_costs())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_cost.get_mean(),
        interval=increase_discounted_cost.get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)
    print("Average increase in discounted cost "
          "and {:.{prec}%} CI:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # increase in discounted total utility under dab therapy with respect to warfarin therapy
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_Dabigitran150.get_utilities(),
        y_ref=simOutputs_warfarin.get_utilities())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_utility.get_mean(),
        interval=increase_discounted_utility.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in discounted utility "
          "and {:.{prec}%} CI:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)


def report_CEA_CBA(simOutputs_warfarin, simOutputs_Dabigitran150):
    warfarin_therapy_strategy = Econ.Strategy(name="Warfarin therapy", cost_obs=simOutputs_warfarin.get_costs(),
                                                   effect_obs=simOutputs_warfarin.get_utilities())
    Dabigitran150_therapy_strategy = Econ.Strategy(name="Dabigitran150 therapy",
                                              cost_obs=simOutputs_Dabigitran150.get_costs(),
                                              effect_obs=simOutputs_Dabigitran150.get_utilities())

    listofStrategies = [warfarin_therapy_strategy, Dabigitran150_therapy_strategy]

    CEA = Econ.CEA(listofStrategies, if_paired=False)

    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )

    CBA = Econ.CBA(listofStrategies, if_paired=False)

    CBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=50000,
        x_label="Willingness-to-pay for one additional QALY ($)",
        y_label="Incremental Net Monetary Benefit ($)",
        interval=Econ.Interval.CONFIDENCE,
        transparency=0.4,
        show_legend=True,
        figure_size=6,
        title='cost benefit analysis')
