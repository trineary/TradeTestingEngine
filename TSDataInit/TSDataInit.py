# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 9/21/2016
#
# Fin 5350
# Trade Testing Engine:
#
# TSDataInit.py
#
# This file provides interface for time series data initialization.  User can select a number of data initialization
# options.  Among those options are creating a random time series and the other is to import a time series from
# some external source.  User can also load a data set from yahoo finance.
#
# --------------------------------------------------------------------------------------------------------------------

# Import standard packages
from yahoo_finance import Share
import pandas.io.data as web
import pandas as pd
import matplotlib

# Import my classes
from PyTTE import TSPlottingTools as tsplot


class TSBootstrapInit:

    tickerData = {}
    adjClose = {}

    def __init__(self):

        return

    #def LoadDataSet(self, data):
    #    # Load data into TSDataInit from an external data source.  Load data in a pandas object.
    #    # Check to make sure data is a pandas object.  If it isn't generate an error and return None.
    #    return

    #def LoadDataSets(self, data):
    #    # If it's desired to load multiple data sets, then add sets in dictionaries (or lists?) of Pandas objects
    #    return

    def LoadFromYahooFinance(self, tickers, startDate, endDate):
        # Load data into TSDataInit from YahooFinance
        # startDate and endDate - need to be in format of: '2014-04-25'.  Year-month-day with quotes included.
        # tickers - list of tickers that data should be collected for.  Should be in this format: ['GLD', 'SLV', 'WFC']

        for ticker in tickers:
            try:
                self.tickerData[ticker] = web.get_data_yahoo(ticker, startDate, endDate)
                self.adjClose[ticker] = pd.DataFrame({tic: data['Adj Close']
                                         for tic, data in self.tickerData.iteritems()})
            except:
                print "Can't find specified ticker"

        return

    def GetStationaryBootstrap(self):
        # Get a stationary bootstrap of of the loaded data set.  A pandas array is returned
        return

    def GetOriginalCloseData(self, ticker):

        return self.adjClose[ticker]

    def PrintDataColumns(self):
        # If it's unclear as to what columns are in the pandas data, this can be called to print them.
        return

# --------------------------------------------------------------------------------------------------------------------
# Test functions

def testyahoo():

    bs = TSBootstrapInit()

    bs.LoadFromYahooFinance(["GLD"], '2014-01-01', '2016-01-01')
    data = bs.GetOriginalCloseData("GLD")
    #plt.plot(data)
    #plt.show()



    return

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    testyahoo()
