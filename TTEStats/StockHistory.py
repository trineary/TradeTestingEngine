# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 9/22/2016
#
# Fin 5350
# Trade Testing Engine:
#
# StockHistory.py
#
# This file provides interface for getting stock data.
#
# --------------------------------------------------------------------------------------------------------------------

# Import standard packages
import yahoo_finance as yfinance
import pandas

# Import my classes

# Global values for selecting different options


class StockHistory:


    def __init__(self):

        return


    def GetHistoricalStockData(self, equity, startDate, endDate):
        yahoo = yfinance.Share(equity)

        data = yahoo.get_historical(start_date=startDate, end_date=endDate)

        return data

# --------------------------------------------------------------------------------------------------------------------
# Test functions

from PyTTE import TSPlottingTools as ts

def testGetStockData(equity, startDate, endDate):
    # equity - String for the ticker symbol. Example: 'SPY'
    # startDate - Start date for historical data. Example: '2014-01-01'
    # stopDate - Start date for historical data. Example: '2014-02-28'

    # Open connection to yahoo finance
    sh = StockHistory()

    # Get equity data between the defined dates
    data = sh.GetHistoricalStockData(equity, startDate, endDate)

    # Put the data into a dataframe
    df = pandas.DataFrame(data=data)
    print df

    # Return the dataframe
    return df

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    equity = "SPY"
    startDate = '2016-08-20'
    endDate = '2016-09-16'

    df = testGetStockData(equity, startDate, endDate)

    dataList = df['Close'].tolist()

    ts.GenPlot([dataList], xaxis=df['Date'].tolist())
