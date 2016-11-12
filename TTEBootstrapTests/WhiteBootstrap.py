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
from matplotlib import pyplot
import pandas

# Import my classes
from BootstrapCalcTools import GetDailyReturns, GetMeanDailyReturn

# Global values for selecting different options


from BootstrapABC import BootstrapABC


# --------------------------------------------------------------------------------------------------------------------

class WhiteBootstrap(BootstrapABC):

    def __init__(self):
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
        print "datalen: ", datalen
        print "first entry:", self._df.at[0, col_name]
        print "last entry:", self._df.at[datalen-1, col_name]
        gain = float(self._df.at[datalen-1, col_name]) - float(self._df.at[0, col_name])
        dailyGain = gain/datalen

        print datalen, gain, dailyGain

        meanDailyReturn, dailyreturns = GetMeanDailyReturn(self._df, self._col_name)
        print "Mean daily return:", meanDailyReturn
        print "Before adjustment:", dailyreturns
        dailyreturns = dailyreturns.apply(lambda x: x-meanDailyReturn)
        print "After adjustement:", dailyreturns

        # Iterate over the daily returns and build a distribution of returns

        for meanCount in xrange(0, self._num_iterations):
            sampleSum = 0
            for randomReturn in xrange(0, datalen):
                index = random.randint(0, datalen-1)
                sampleSum += dailyreturns.iat[index, 0]
            sampleMean = sampleSum / datalen
            print "Samplemean:", sampleMean
            break

        pass

    def has_predictive_power(self):
        pass

# --------------------------------------------------------------------------------------------------------------------
# Test functions




if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    wb = WhiteBootstrap()
