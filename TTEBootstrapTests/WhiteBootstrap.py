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
from BootstrapCalcTools import GetDailyReturns, GetMeanDailyReturn, GetPVal

# Global values for selecting different options


# --------------------------------------------------------------------------------------------------------------------

class WhiteBootstrap(BootstrapABC):

    def __init__(self):
        self._sample_means = []
        self._df = None
        self._detrended_data = None
        self._col_name = None
        self._num_iterations = None
        pass


    def init_test(self, df, col_name, num_iterations=5000):
        """
        init_test initializes the White Reality Check Bootstrap test

        :param df: dataframe containing data to bootstrap
        :param col_name: name of colume in data frame containing data
        :param num_iterations: number of iterations to build bootstrap sampling distribution
        :return: none
        """
        self._df = df
        self._detrended_data = None
        self._col_name = col_name
        self._num_iterations = num_iterations

        datalen = len(self._df.index)

        # Detrend the data
        meanDailyReturn, dailyreturns = GetMeanDailyReturn(self._df, self._col_name)
        dailyreturns = dailyreturns.apply(lambda x: x-meanDailyReturn)

        # Iterate over the daily returns and build a distribution of returns
        meanList = []
        for meanCount in xrange(0, self._num_iterations):
            sampleSum = 0
            for randomReturn in xrange(0, datalen):
                index = random.randint(0, datalen-1)
                sampleSum += dailyreturns.iat[index, 0]
            #sampleMean = sampleSum #/ datalen
            #meanList.append(sampleMean)
            meanList.append(sampleSum)

        #histogram, edges = np.histogram(meanList, bins=10)

        self._sample_means = meanList

        pass

    def plot_histogram(self, bins=20):
        if len(self._sample_means) > 0:
            plt.hist(self._sample_means, bins=bins)
            plt.grid(True)
            plt.show()
        return

    def has_predictive_power(self, rule_percent_return):

        return GetPVal(self._sample_means, rule_percent_return)


# --------------------------------------------------------------------------------------------------------------------
# Test functions


if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__


