# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 11/12/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# kWhiteRealityCheck.py
#
# This file is an implementation of White's Reality Check for evaluating the significance of a trading rule's
# predictive power.
#
# --------------------------------------------------------------------------------------------------------------------


# Import standard packages
import random
from matplotlib import pyplot as plt
from BootstrapABC import BootstrapABC

# Import my classes
from BootstrapCalcTools import GetDailyReturns, GetMeanDailyReturn, GetDetrendedReturns, GetPVal

# Global values for selecting different options


# --------------------------------------------------------------------------------------------------------------------
class MonteCarloBootstrap(BootstrapABC):

    def __init__(self):
        self._sample_means = []
        self._daily_rules = []
        pass

    def init_test(self, df, col_name, num_iterations=5000):
        """
        init_test initializes the White Reality Check Bootstrap test

        :param df: dataframe containing data to bootstrap
        :param col_name: name of colume in data frame containing data
        :param daily_rules: list of rules applied to the time series in the data frame.  rules take on (+1, -1) values
        :param num_iterations: number of iterations to build bootstrap sampling distribution
        :return: none
        """
        self._df = df
        self._detrended_data = None
        self._col_name = col_name
        self._num_iterations = num_iterations

        datalen = len(self._df.index)
        #gain = float(self._df.at[datalen-1, col_name]) - float(self._df.at[0, col_name])
        #dailyGain = gain/datalen

        pass


    def plot_histogram(self, bins=20):
        if len(self._sample_means) > 0:
            plt.hist(self._sample_means, bins=bins)
            plt.grid(True)
            plt.show()
        return

    def run_monte_carlo_round(self, detrended_data):
        # Run through one iteration of pairing daily rules with detrended returns.  Calculate the average return
        # and return that value.

        # check length of detrended data and daily rules.  They should be the same length.
        if len(detrended_data) != len(self._daily_rules):
            print "Monte Carlo error! Detrended data and daily rules not the same length."
            return -1

        # Get a copy of the detrended data
        detrended_copy = detrended_data[0].tolist()

        # Cycle through the data now
        total_val = 0
        for daily_direction in self._daily_rules:
            index = random.randint(0, len(detrended_copy)-1)
            total_val += daily_direction * detrended_copy.pop(index)

        total_val /= len(detrended_data)*1.0
        #print total_val

        return total_val

    def has_predictive_power(self, daily_rules, rule_percent_return):

        # Set daily rules
        self._daily_rules = daily_rules

        # Get one-day market price changes

        # Detrend the data
        detrended_returns = GetDetrendedReturns(self._df, self._col_name)

        # Run through iterations and collect distribution
        self._sample_means = []
        for i in range(0, self._num_iterations, 1):
            avg_val = self.run_monte_carlo_round(detrended_returns)
            self._sample_means.append(avg_val)

        # Calculate and return the p-value for the sample mean distribution calculated above
        return GetPVal(self._sample_means, rule_percent_return)

# --------------------------------------------------------------------------------------------------------------------
# Test functions

def test_monte_carlo_round():
    rules = [1, 1, -1, -1, -1]
    data = [2, 3, 4, 3, 2]

    mc = MonteCarloBootstrap()
    mc._daily_rules = rules

    mean = mc.run_monte_carlo_round(data)
    print "mean result: ", mean

    pass

def test_monte_carlo_prediction():
    rules = [1, 1, -1, -1, -1]
    data = [2, 3, 4, 3, 2]

    mc = MonteCarloBootstrap()
    mc._daily_rules = rules

    mean = mc.run_monte_carlo_round(data)
    print "mean result: ", mean

    pass

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    #test_monte_carlo_round()
    test_monte_carlo_prediction()
