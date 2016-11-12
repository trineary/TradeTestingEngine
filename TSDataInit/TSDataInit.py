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
import pandas.io.data as web
import pandas as pd
import numpy as np
import csv
import math

# Import my classes
from pytte import TSPlottingTools as tsplot


class TSBootstrapInit:

    tickerData = {}
    adjClose = {}
    writeBlocksToFile = True
    blockFileName = "BlockOutput.csv"

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

        # Block length <2 doesn't do us any good.  If this happens then set to 2
        if blockLen < 2:
            blockLen = 2

        return blockLen

    def GetBlock(self, ticker, startIndex, blockLength):
        # Get the pandas block for the ticker at the start index for the specified block length
        dataLen = len(self.adjClose[ticker])
        # Make sure indexes are integers
        startIndex = int(startIndex)
        blockLength = int(blockLength)

        if startIndex + blockLength < dataLen:
            block1 = self.adjClose[ticker].iloc[startIndex:(startIndex+blockLength)]
            block = [block1]
        else:
            block1 = self.adjClose[ticker].iloc[startIndex:dataLen-1]
            block2 = self.adjClose[ticker].iloc[0:(blockLength - (dataLen-startIndex))]
            block = [block1, block2]
            print "block wrapped around"

        return block

    #----------------------------------------------------------------------------------------------------------------
    # Straight blocking grabbing and block shifting approach.
    #----------------------------------------------------------------------------------------------------------------

    def ShiftBlock(self, existingBlock, newBlock):
        # shift newBlock up or down to be close to end of existing block
        # Get the length of the existing block and the last value in that block
        lastIndex = len(existingBlock)-1
        lastValue = existingBlock[lastIndex]
        lenNewBlock = len(newBlock)
        returnBlock = newBlock

        # Get the first value of the newBlock
        firstValue = newBlock[0]
        diff = (firstValue - lastValue)
        diff = diff + diff*0.01

        # Shift the newBlock so that it's closer to end of existing block
        for index in xrange(0, lenNewBlock):
            returnBlock[index] = newBlock[index] - diff

        return returnBlock


    def GetBootstrapByShiftedBlocks(self, ticker):
        # Get a stationary bootstrap of of the loaded data set.  A list of floats is returned.
        dataLen = len(self.adjClose[ticker])
        bootStrapLen = 0
        stationaryBootStrap = None

        while bootStrapLen < dataLen:
            startIndex = self.GetStartIndex(ticker)
            blockLen = self.GetRandomBlockLen(ticker)
            newBlocks = self.GetBlock(ticker, startIndex, blockLen)

            for block in newBlocks:
                newBlock = block[ticker].tolist()

                if stationaryBootStrap is None:
                    stationaryBootStrap = newBlock
                    self.WriteBlockToFile(newBlock)
                else:
                    shiftedBlock = self.ShiftBlock( stationaryBootStrap, newBlock)
                    stationaryBootStrap = stationaryBootStrap + shiftedBlock
                    self.WriteBlockToFile(shiftedBlock)

            bootStrapLen = len(stationaryBootStrap)

        return stationaryBootStrap

    #----------------------------------------------------------------------------------------------------------------
    #  Bootstrap approach using percent change between consecutive returns.  Time series is generated based on
    #  the percent changes.
    #----------------------------------------------------------------------------------------------------------------

    def GetPriceByPercentReturn(self, lastBootstrapPrice, price, nextPrice):
        # lastPrice - last price in the bootstrap list
        # price - older price in the time series
        # nextPrice - next price in the time series

        percentReturn = math.log(nextPrice) - math.log(price)
        nextBootStrapValue = lastBootstrapPrice + lastBootstrapPrice*percentReturn
        return nextBootStrapValue

    def GenerateSeriesFromBlock(self, stationaryBootstrap, nextBlock):
        # Generate a new sequence of prices to be added to the stationaryBootstrap from nextBlock

        for i in range(0, (len(nextBlock)-1)):
            newValue = self.GetPriceByPercentReturn(stationaryBootstrap[len(stationaryBootstrap)-1], nextBlock[i], nextBlock[i+1])
            stationaryBootstrap.append(newValue)

        return stationaryBootstrap


    def GetStationaryBootstrap(self, ticker):
        # Get a stationary bootstrap of of the loaded data set.  A list of floats is returned.
        # This constructs a time series that grows out of the first price received from GetBlock.  All other
        # prices are generated based on a percent return from consecutive prices.

        dataLen = len(self.adjClose[ticker])
        bootStrapLen = 0
        stationaryBootStrap = None
        lastBootstrapValue = None

        while bootStrapLen < dataLen:
            startIndex = self.GetStartIndex(ticker)
            blockLen = self.GetRandomBlockLen(ticker)
            newBlocks = self.GetBlock(ticker, startIndex, blockLen)

            for block in newBlocks:
                newBlock = block[ticker].tolist()

                # Seed the first value in our new time series
                if lastBootstrapValue is None:
                    lastBootstrapValue = newBlock[0]
                    stationaryBootStrap = [lastBootstrapValue]
                else:
                    self.GenerateSeriesFromBlock(stationaryBootStrap, newBlock)

            bootStrapLen = len(stationaryBootStrap)

        return stationaryBootStrap

    def GetOriginalCloseData(self, ticker):
        # Get the original adjusted close data
        return self.adjClose[ticker]

    def WriteBlockToFile(self, block):
        # If flag is set to true then write block to file.
        if self.writeBlocksToFile is True:
            myfile = open(self.blockFileName, 'a')
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(block)

        return

    #def PrintDataColumns(self):
    #    # If it's unclear as to what columns are in the pandas data, this can be called to print them.
    #    return

# --------------------------------------------------------------------------------------------------------------------
# Test functions

def testyahoo():
    # Test ability to connect to yahoo and get data from it.
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

    return

def TestBootstrapByBlock():
    # Test code that grabs a block from data set and shifts it to fit into current time series
    np.random.seed(2)
    bs = TSBootstrapInit()

    bs.LoadFromYahooFinance(["GLD"], '2014-01-01', '2016-01-01')
    bootStrap = bs.GetBootstrapByShiftedBlocks("GLD")

    tsplot.GenPlot([bootStrap])

    return

def TestGetNextBootstrapValue():

    np.random.seed(10)
    bs = TSBootstrapInit()
    nextValue = bs.GetPriceByPercentReturn(101, 110, 112)

    print nextValue

    return

def TestStationaryBootstrap():
    # Test the stationary bootstrap that generates time series by looking at percent change in random blocks
    # from original series.
    #np.random.seed(1)
    bs = TSBootstrapInit()

    #bs.LoadFromYahooFinance(["GLD"], '2014-01-01', '2016-01-01')
    bs.LoadFromYahooFinance(["SPY"], '2010-01-01', '2014-01-01')
    bootStrap = bs.GetStationaryBootstrap("SPY")

    tsplot.GenPlot([bootStrap])

    return
# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    #testyahoo()
    #TestGetNextBootstrapValue()
    #TestBootstrapByBlock()
    TestStationaryBootstrap()
