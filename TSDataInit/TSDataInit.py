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
from PyTTE import TSPlottingTools as tsplot


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
            newBlock = self.GetBlock(ticker, startIndex, blockLen)
            newBlock = newBlock[ticker].tolist()

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
    #
    #----------------------------------------------------------------------------------------------------------------

    def ShiftBlock1(self, ticker, existingBlock, newBlock):
        # shift newBlock up or down to be close to end of existing block
        # Get the length of the existing block and the last value in that block
        # Shift according to return: r = log(p+1) - log(p) where p is price at time t and p+1 is price at time t+1
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

    def GetPriceByPercentReturn(self, lastBootstrapPrice, price, nextPrice):
        # lastPrice - last price in the bootstrap list
        # price - older price in the time series
        # nextPrice - next price in the time seris

        percentReturn = math.log(nextPrice) - math.log(price)
        nextBootStrapValue = lastBootstrapPrice + lastBootstrapPrice*percentReturn
        return nextBootStrapValue




    def GetBootstrapByBlock(self, ticker):
        # Get a stationary bootstrap of of the loaded data set.  A pandas array is returned.
        dataLen = len(self.adjClose[ticker])
        bootStrapLen = 0
        stationaryBootStrap = None

        while bootStrapLen < dataLen:
            startIndex = self.GetStartIndex(ticker)
            blockLen = self.GetRandomBlockLen(ticker)
            newBlock = self.GetBlock(ticker, startIndex, blockLen)
            newBlock = newBlock[ticker].tolist()

            if stationaryBootStrap is None:
                stationaryBootStrap = newBlock
                self.WriteBlockToFile(newBlock)
                print "Create new block"
            else:
                shiftedBlock = newBlock
                shiftedBlock = self.ShiftBlock( stationaryBootStrap, newBlock)
                stationaryBootStrap = stationaryBootStrap + shiftedBlock
                self.WriteBlockToFile(shiftedBlock)

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

def TestGetNextBootstrapValue():

    np.random.seed(10)
    bs = TSBootstrapInit()
    nextValue = bs.GetPriceByPercentReturn(101, 110, 112)

    print nextValue

    return

def TestBootstrapByBlock():

    np.random.seed(10)
    bs = TSBootstrapInit()

    bs.LoadFromYahooFinance(["GLD"], '2014-01-01', '2016-01-01')
    data = bs.GetOriginalCloseData("GLD")

    bootStrap = bs.GetBootstrapByShiftedBlocks("GLD")

    tsplot.GenPlot([bootStrap])

    return

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    #testyahoo()
    TestBootstrapByBlock()
    #TestGetNextBootstrapValue()
