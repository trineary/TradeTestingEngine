# --------------------------------------------------------------------------------------------------------------------
# Patrick Neary
# CS 6110
# Project
# 10/6/2016
#
# TradeDetails.py
#
# This file
# --------------------------------------------------------------------------------------------------------------------

import datetime


class TradeDetails:

    CASH = 0
    LONG = 1
    SHORT = -1

    def __init__(self):
        self.openPrice = 0.0
        self.closePrice = 0.0
        self.spread = 0.0
        self.tradeDirection = self.CASH
        self.equityName = ""
        self.openTimeStamp = None
        self.closeTimeStamp = None
        self.duration = None
        self.currPL = 0.0
        self.stopLoss = None
        self.profitTarget = None
        self.totalPL = 0.0
        self.ID = None
        return

    def __str__(self):
        mystr = "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.equityName, self.openTimeStamp, self.closeTimeStamp,
                    self.duration, self.openPrice, self.closePrice, self.currPL, self.totalPL, self.ID)
        return mystr

    def OpenTrade(self, equity, openprice, spread, direction, timestamp, id=None):
        # timestamp - needs to be a string in format of "year-month-day" or in datetime format.
        if isinstance(timestamp, str) == True:
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")

        # Check to make sure timestamp is a date/time format
        if isinstance(timestamp, datetime.datetime) == False:
            print "Timestamp needs to be in datetime format"
            return

        self.openPrice = openprice
        self.equityName = equity
        self.spread = spread
        self.tradeDirection = direction
        self.openTimeStamp = timestamp
        self.ID = id # ID of entity making the trade
        return

    def CloseTrade(self, closeprice, timestamp):
        # timestamp - needs to be a string in format of "year-month-day" or in datetime format.
        if isinstance(timestamp, str) == True:
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")

        # Check to make sure timestamp is a date/time format
        if isinstance(timestamp, datetime.datetime) == False:
            print "Timestamp needs to be in datetime format"
            return

        # Close the trade
        self.closePrice = closeprice
        self.closeTimeStamp = timestamp
        #self.tradeDirection = self.CASH

        self.GetCurrentPL(closeprice)
        self.GetTradeDuration()
        #self.ID = None
        return

    def GetCurrentPL(self, currprice):
        # Calculate the change in price from open to now.  This includes the cost of the spread.

        if self.tradeDirection is self.CASH:
            self.currPL = 0.0
        elif self.tradeDirection is self.SHORT:
            self.currPL = float(self.openPrice) - float(currprice) - float(self.spread)
        else:
            self.currPL = float(currprice) - float(self.openPrice) - float(self.spread)

        #print "GetCurrentPL: ", self.currPL, self.tradeDirection, self.spread

        return self.currPL

    def GetTradeDuration(self):
        duration = self.closeTimeStamp - self.openTimeStamp
        self.duration = duration
        return self.duration

    def RedefineDirection(self, cash, long, short):
        self.CASH = cash
        self.LONG = long
        self.SHORT = short
        return

    def SetTotalPL(self, totalPL):
        self.totalPL = totalPL
        return

    def GetCurrentTradeID(self):
        return self.ID

# --------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------

def TestTradeDetails():

    openTS = datetime.datetime(2016, 04, 18)
    closeTS = datetime.datetime(2016, 04, 19)
    openPrice = 78.8
    closePrice = 78.2
    spread = 0.032

    td = TradeDetails()
    td.OpenTrade("AUDJPY", openPrice, spread, 1, openTS)
    td.CloseTrade(closePrice, closeTS)
    print td

    return

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run
# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    TestTradeDetails()
