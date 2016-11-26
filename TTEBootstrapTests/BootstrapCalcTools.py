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
        if(prev == None):
            dreturn = 0.0
        else:
            dreturn = math.log10(float(rowVal)/prev)
        prev = float(rowVal)
        returns.append(dreturn)

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

    return meanDailyReturn, dailyReturns


def GetDetrendedReturns(df, col_name):

    # Get the daily returns and the mean daily return
    meanDailyReturn, dailyreturns = GetMeanDailyReturn(df, col_name)
    # Detrend the daily returns by subtracting off the mean daily return
    detrended_returns = dailyreturns.apply(lambda x: x-meanDailyReturn)

    return detrended_returns


def GetPVal(sample_dist, rule_percent_return):
    '''

    :param sample_dist: sample distribution, this is assumed to be a distribution around zero
    :param rule_percent_return: percent return of the trading rule
    :return: return the pvalue associated with the trading rule
    '''

    lessThanCnt = 0
    for meanReturn in sample_dist:
        if meanReturn < rule_percent_return:
            lessThanCnt += 1

    percentage = lessThanCnt/float(len(sample_dist))
    pval = 1-percentage

    return pval
