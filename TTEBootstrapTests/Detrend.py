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
from matplotlib import pyplot
import pandas

# Import my classes

# Global values for selecting different options





# --------------------------------------------------------------------------------------------------------------------

"""
    def init_test(self, df, col_name, num_iterations=5000):

        init_test initializes the White Reality Check Bootstrap test

        :param df: dataframe containing data to bootstrap
        :param col_name: name of colume in data frame containing data
        :param num_iterations: number of iterations to build bootstrap sampling distribution
        :return: none

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
        self._detrend_data = self.detrend_data(self._df, self._col_name, dailyGain)
        print self._detrend_data


        pass

    def detrend_data(self, orig_data, col_name, value):

        detrended_data = orig_data[col_name].apply(lambda x: float(x)-value)

        return detrended_data
"""
# --------------------------------------------------------------------------------------------------------------------
# Test functions




if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__


