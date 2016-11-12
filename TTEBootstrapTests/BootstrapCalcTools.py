# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 11/12/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# BootstrapCalcTools.py
#
# This file contains tools common to the bootstrap processes.
#
# --------------------------------------------------------------------------------------------------------------------


# Import standard packages
import pandas
import math



# --------------------------------------------------------------------------------------------------------------------


def GetDailyReturns(df, colName):
    """
    Generate a dataframe containing the mean daily returns from the specified data frame and column name.  The daily
    returns are calculated using log(day/prev day).

    :param df:
    :param colName:
    :return:
    """

    prev = None
    returns = []
    for index, rowVal in df[colName].iteritems():
        print rowVal
        if(prev == None):
            dreturn = 0.0
        else:
            dreturn = math.log10(float(rowVal)/prev)
        prev = float(rowVal)
        returns.append(dreturn)

    print len(df.index), len(returns)

    return pandas.DataFrame(data=returns)


def GetMeanDailyReturn(df, colName):
    """
    Given the dataframe and column, calculate the daily return for the sequence and then determine the mean daily
    return.

    :param df:
    :param colName:
    :return: return the mean along with the dataframe containing the data
    """

    dailyReturns = GetDailyReturns(df, colName)
    meanDailyReturn = dailyReturns[0].mean()
    print "meanDailyreturn: ", meanDailyReturn

    return meanDailyReturn, dailyReturns



