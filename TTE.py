# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 9/21/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# tte.py
#
# This file handles the interface to most of the code in this project.
#
# --------------------------------------------------------------------------------------------------------------------

# Import standard packages
import math
import pandas as pd
import datetime as dt
from matplotlib import pyplot
import yahoo_finance as yfinance


# Import my classes
from TradeTracking.TradeHistory import TradeTracking
from pytte.TTEBootstrapTests import WhiteBootstrap, MonteCarloBootstrap, TTEBootstrap


class TTE:
    # Bootstrap options that are available with this package
    BOOTSTRAP_TTE = 0
    BOOTSTRAP_MONTE_CARLO = 1
    BOOTSTRAP_WHITE = 2
    # Trading direction options\
    CASH = 0
    LONG = 1
    SHORT = -1

    def __init__(self):

        # Trade tracking
        self._tt = TradeTracking(trackDailyPositions=True)
        self._trade_history = None
        # Bootstrap initializations
        self._bs_tte = None
        self._bs_mc = None
        self._bs_wh = None
        self._bs = None  # this is the currently selected bootstrap
        # Dataframe for trade data
        self._df = None
        self._column = None
        self._ticker = None

        return

    def get_hist_data(self, ticker, startdate, stopdate, column="Adj_Close"):
        # get historical data
        # Inputs
        # 1. ticker - ticker sympol of desired equite.  Ex. 'SPY'
        # 2. startdate - start date to start collecting data from. Ex. startdate = '2016-08-20'
        # 3. stopdate - stop date to stop collecting data from. Ex. endDate = '2016-09-16'
        # 4. column - this is the column in the dataframe to use to get price information from.  Default is 'Adj_Close'
        # Returns
        # 1. dataframe containing data for the specified inputs
        #
        # Get a dataframe with data between the two dates for the specified ticker.  This will automatically load
        # the historical data into the local _df variable.
        # Get the historical data and load into the dataframe variable.  Return the historical data to the calling
        # function for the user to cycle through it to generate trade signals.

        #self._df = GetHistoricalStockData(ticker, startdate, stopdate)

        # Get the data from yahoo finance, reorder the data, and then put the data into a dataframe for easy use.
        yahoo = yfinance.Share(ticker)
        data = yahoo.get_historical(start_date=startdate, end_date=stopdate)

        # data comes in reversed order.  Put it in ascending order.
        data = data[::-1]

        # Put the data into a dataframe
        df = pd.DataFrame(data=data)

        # Load historical data and initialize other values
        self.load_hist_data(ticker, df, column)

        return df

    def load_hist_data(self, ticker, hist_data, column="Adj_Close"):
        # Load the specified data set.  This is only used if the user loads historical data from a different source
        # (forex data for example).
        # Inputs
        # 1. hist_data - historical data in the format of a dataframe
        # 2. column - this is the column in the dataframe to use to get price information from.  Default is 'Adj_Close'

        self._ticker = ticker
        self._df = hist_data
        self._tt.InitTickData(self._df)
        self._column = column
        self._trade_history = [0]*len(self._df[self._column])  # Make trade history the same length as the data

        pass

    def reset(self):
        '''
        reset - dataframe is left alone, but all other internal tracking is reset so system can run a new test
        :return:
        '''
        print "TODO: reset still needs to be implemented"
        pass


    def open_trade(self, index, direction):
        '''

        :param index: index into the dataframe.
        :param direction: direction of the trade (CASH, LONG, or SHORT)
        :return: None
        '''

        # Make sure index is in a valid range
        if index < 0 or index > len(self._df[self._column]):
            print "open_trade error! index is out of bounds (%d)\n" %index
            return False

        openprice = self._df.ix[index][self._column]
        spread = 0.0
        timestamp = self._df.ix[index]['Date']
        self._tt.OpenTrade(self._ticker, openprice=openprice, spread=spread, direction=direction, timestamp=timestamp)

        return True

    def close_trade(self, index):

        # Make sure index is in a valid range
        if index < 0 or index > len(self._df[self._column]):
            print "close_trade error! index is out of bounds (%d)\n" %index
            return False

        closeprice = self._df.ix[index][self._column]
        timestamp = self._df.ix[index]['Date']
        self._tt.CloseTrade(closeprice=closeprice, timestamp=timestamp, direction=self.CASH)

        return True

    def select_bootstrap(self, selection):
        '''
        set_bootstrap

        Set the bootstrap to be used for all subsequent queries.  This can be updated at any time to get information
        relevant to the specified bootstrap.

        :return:
        '''

        if selection == self.BOOTSTRAP_TTE:
            self._bs = TTEBootstrap.TTEBootstrap()
        elif selection == self.BOOTSTRAP_MONTE_CARLO:
            self._bs = MonteCarloBootstrap.MonteCarloBootstrap()
        elif selection == self.BOOTSTRAP_WHITE:
            self._bs = WhiteBootstrap.WhiteBootstrap()
        else:
            print "select_bootstrap error! selection was invaled (%d)\n" %(selection)
            print "Valid selections are the following: \n"
            print " BOOTSTRAP_TTE, BOOTSTRAP_MONTE_CARLO, BOOTSTRAP_WHITE\n\n"
            return False

        return True

    def get_pvalue(self, iterations=5000):

        # Calculate the total return based on what has been tracked in the trade tracker
        rule_percent_return = self._tt.GetPercentReturn()

        # Initialize the test
        self._bs.init_test(self._df, self._column, num_iterations=iterations)
        # Determine what the p-value is for this bootstrap method
        pvalue = self._bs.has_predictive_power(rule_percent_return)

        return pvalue

    def get_trade_stats(self):

        return self._tt.GetTradeStatsStr()

    def print_trade_stats(self):

        print "\n", self._tt.GetTradeStatsStr()
        pass

    def print_trade_history(self):
        self._tt.PrintHistory()
        pass

    def plot_pdf(self):
        '''
        plot_pdf

        # Display a plot showing the probability density function of returns calculated.
        :return:
        '''
        self._bs.plot_histogram()
        pass

    def plot_trades_equity(self):
        '''
        plot_trades_equity

        Generate a plot that shows the trades and the equity curve for the given dataframe

        :return:
        '''

        #print len(self.pairtimestmps), len(self.pairhistory), len(self.visualRewardHistory)

        pyplot.figure(1)
        #pyplot.subplot(211)

        pyplot.plot(self._df[self._column])
        #pyplot.subplot(212)
        #pyplot.plot(self.visualRewardHistory)
        #pyplot.subplot(313)
        #pyplot.plot(self.visualTradeHistory)
        #x1,x2,y1,y2 = pyplot.axis()
        #pyplot.axis((x1,x2,(y1-0.25), (y2+0.25)))

        pyplot.xticks( rotation= 45 )

        pyplot.show()
        pass

    def plot_all(self, title=None):

        #pyplot.xlabel('Smarts')
        #pyplot.ylabel('Probability')

        pyplot.figure(1)

        pyplot.subplot(311)
        pyplot.title(title)
        sample_means = self._bs.get_histogram_data()
        pyplot.hist(sample_means, bins=20)
        pyplot.grid(True)

        pyplot.subplot(312)
        pyplot.plot(self._df[self._column])

        pyplot.subplot(313)
        dates = self._df['Date'].tolist()
        x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
        pyplot.plot(self._df['Position'])
        #pyplot.plot(x, self._df['Position'])
        #pyplot.gcf().autofmt_xdate()
        pyplot.xticks( rotation= 45 )
        x1,x2,y1,y2 = pyplot.axis()
        pyplot.axis((x1,x2,(y1-0.25), (y2+0.25)))

        pyplot.show()
        pass

# --------------------------------------------------------------------------------------------------------------------
# Test functions


# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__


