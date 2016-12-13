# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 9/22/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# TestFile.py
#
# This file is to test out some concepts while working through the code.
#
# --------------------------------------------------------------------------------------------------------------------


# Import standard packages
import yahoo_finance as yfinance
import math
from matplotlib import pyplot
import pandas
from TTEBootstrapTests import WhiteBootstrap, MonteCarloBootstrap
from tradelogger import TradeHistory


# Import my classes

# Global values for selecting different options



def GetHistoricalStockData( equity, startDate, endDate):
    yahoo = yfinance.Share(equity)

    data = yahoo.get_historical(start_date=startDate, end_date=endDate)
    # data comes in reversed order.  Put it in ascending order.
    data = data[::-1]

    return data


def CalculateDailyReturn(dataset, startIndex=None, stopIndex=None):
    # calculate the daily returns for the provided data set.
    # daily returns based on end log(endprice/startprice) / number of days
    # If start and stop indexes are provided, then use them, otherwise just run the whole data set

    # Initialize the start/stop indexes
    if startIndex == None:
        startIndex = 0
    if stopIndex == None:
        stopIndex = len(dataset) - 1

    numDays = stopIndex - startIndex

    print "Start: (", dataset[stopIndex], ") Stop: (", dataset[startIndex], ") Days: (", numDays, ")"

    dailyReturn = math.log10(dataset[stopIndex]/dataset[startIndex])
    dailyReturn = math.log10(dataset[stopIndex]/dataset[startIndex])
    #dailyReturn /= numDays

    return dailyReturn


# --------------------------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------------------------
# Test functions
from pytte import TSPlottingTools as ts

def testGetStockData(equity, startDate, endDate):
    # equity - String for the ticker symbol. Example: 'SPY'
    # startDate - Start date for historical data. Example: '2014-01-01'
    # stopDate - Start date for historical data. Example: '2014-02-28'

    # Get equity data between the defined dates
    data = GetHistoricalStockData(equity, startDate, endDate)

    # Put the data into a dataframe
    df = pandas.DataFrame(data=data)

    # Return the dataframe
    return df

import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
def test1():
    data = [4, 5, 6, 5.5, 8.5, 7, 4.25, 7.5, 8]

    dailyreturn = CalculateDailyReturn(data)
    #print dailyreturn
    x = range(0, len(data))
    selection = 0
    if selection == 0:
        x = sm.add_constant(x, prepend=False)
        model = sm.OLS(data, x)
        results = model.fit()
        print results.summary()
        print "\nparams:", results.params # this is apparently the beta
        print "predict: ", results.predict()
        print "R^2:", results.rsquared
        #http://statsmodels.sourceforge.net/devel/generated/statsmodels.regression.linear_model.RegressionResults.html
        print "residuals: ", results.resid
        print "fitted:", results.fittedvalues
        pyplot.plot(data)
        pyplot.plot(results.predict())
        pyplot.show()
    else:
        lm = LinearRegression()
        print x, data
        print "lengths:", len(x), len(data)
        lm.fit(pd.DataFrame(x), pd.DataFrame(data))
        print "intercept: ", lm.intercept_
        print "coeff: ", lm.coef_
        #print lm.predict(data)
        print "data", data
        print "predict: ", lm.predict(pd.DataFrame(data))
        print "lens: ", len(pd.DataFrame(x)), len(lm.predict(pd.DataFrame(data))), len(data)
        pyplot.scatter(pd.DataFrame(x), lm.predict(pd.DataFrame(data)) - pd.DataFrame(data))
        pyplot.show()

    #pyplot.show()
    return

def TestWhiteRealityCheck():
    equity = "SPY"
    startDate = '2016-08-20'
    endDate = '2016-09-16'

    df = testGetStockData(equity, startDate, endDate)

    dataList = df['Close'].tolist()

    wbs = WhiteBootstrap.WhiteBootstrap()
    wbs.plot_histogram()
    wbs.init_test(df, 'Adj_Close', num_iterations=5000)
    wbs.plot_histogram()
    pval = wbs.has_predictive_power(rule_percent_return=0.0015)
    print "pval:", pval

    pass


def TestMonteCarloBootstrap():
    equity = "SPY"
    startDate = '2016-08-20'
    endDate = '2016-09-16'
    th = TradeHistory.TradeTracking(trackDailyPositions=True)

    df = testGetStockData(equity, startDate, endDate)
    th.InitTickData(df)
    th.OpenTrade('SPY', df.ix[4]['Close'], 0.0, 1, df.ix[4]['Date'])
    th.CloseTrade(df.ix[11]['Close'], df.ix[11]['Date'])

    rules = df['Position'].tolist()

    mcbs = MonteCarloBootstrap.MonteCarloBootstrap()
    mcbs.init_test(df, 'Close', num_iterations=5000)
    pval = mcbs.has_predictive_power(rules, rule_percent_return=0.00095)
    mcbs.plot_histogram()
    print "pval:", pval

    pass

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    #TestWhiteRealityCheck()
    #TestMonteCarloBootstrap()
    test1()

