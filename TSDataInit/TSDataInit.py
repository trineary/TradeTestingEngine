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
import numpy as np
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

    def GetStartIndex(self, ticker):
        # Start index is uniform discrete on {1, .... N}
        # random_integers returns a uniform distribution
        N = len(self.adjClose[ticker])

        start = np.random.random_integers(0, N)

        return start

    def GetRandomBlockLen(self, ticker):
        # Length should be a geometric distribution
        dataLen = len(self.adjClose[ticker])
        meanBlockLen = dataLen/20.0
        p = 1/meanBlockLen

        blockLen = (np.random.geometric(p, 1)) % (dataLen-1)

        return blockLen

    def GetBlock(self, ticker, startIndex, blockLength):
        # Get the pandas block for the ticker at the start index for the specified block length
        dataLen = len(self.adjClose[ticker])
        # Make sure indexes are integers
        startIndex = int(startIndex)
        blockLength = int(blockLength)

        if startIndex + blockLength < dataLen:
            block = self.adjClose[ticker].iloc[startIndex:(startIndex+blockLength)]
        else:
            block1 = self.adjClose[ticker].iloc[startIndex:dataLen-1]
            block2 = self.adjClose[ticker].iloc[0:(blockLength - (dataLen-startIndex))]
            frames = [block1, block2]
            block = pd.concat(frames)

        return block

    def GetStationaryBootstrap(self, ticker):
        # Get a stationary bootstrap of of the loaded data set.  A pandas array is returned.
        dataLen = len(self.adjClose[ticker])
        bootStrapLen = 0
        stationaryBootStrap = None

        while bootStrapLen < dataLen:
            startIndex = self.GetStartIndex(ticker)
            blockLen = self.GetRandomBlockLen(ticker)
            newBlock = self.GetBlock(ticker, startIndex, blockLen)
            if stationaryBootStrap is None:
                stationaryBootStrap = newBlock
                print "Create new block"
            else:
                #print "concatonate block. blocklen: ", blockLen, startIndex, startIndex+blockLen
                frames = [stationaryBootStrap, newBlock]
                stationaryBootStrap = pd.concat(frames)


            bootStrapLen = len(stationaryBootStrap)
            #print "Bootstrap len: ", bootStrapLen

        return stationaryBootStrap

    def GetOriginalCloseData(self, ticker):
        # Get the original adjusted close data
        return self.adjClose[ticker]

    #def PrintDataColumns(self):
    #    # If it's unclear as to what columns are in the pandas data, this can be called to print them.
    #    return

# --------------------------------------------------------------------------------------------------------------------
# Test functions

def testyahoo():

    bs = TSBootstrapInit()

    bs.LoadFromYahooFinance(["GLD"], '2014-01-01', '2016-01-01')
    data = bs.GetOriginalCloseData("GLD")
    for index in xrange(0,50):
        startIndex = bs.GetStartIndex("GLD")
        blockLen = bs.GetRandomBlockLen("GLD")
        print startIndex, blockLen

    block = bs.GetBlock("GLD", startIndex, blockLen)

    print block
    print data

    #plt.plot(data)
    #plt.show()

    return

def TestBootstrap():

    bs = TSBootstrapInit()

    bs.LoadFromYahooFinance(["GLD"], '2014-01-01', '2016-01-01')
    data = bs.GetOriginalCloseData("GLD")

    bootStrap = bs.GetStationaryBootstrap("GLD")

    print bootStrap
    tsplot.GenPlot([bootStrap['GLD'].tolist()])

    return

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    #testyahoo()
    TestBootstrap()
