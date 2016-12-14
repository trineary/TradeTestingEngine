# --------------------------------------------------------------------------------------------------------------------
# Patrick Neary
# Fin5350
# Project
# 10/6/2016
#
# TradeHistory.py
#
# This file
# --------------------------------------------------------------------------------------------------------------------

import datetime
import numpy as np
from TradeDetails import TradeDetails


class TradeTracking:

    def __init__(self, trackHistory=True, trackDailyPositions=False):
        self.totalPL = 0.0
        self.tradeHistory = []
        self.currTrade = TradeDetails()
        self.trackHistory = trackHistory
        self.totalWins = 0
        self.totalLosses = 0
        self.longWins = 0
        self.shortWins = 0
        self.longLosses = 0
        self.shortLosses = 0
        self.tickData = None
        self.trackDailyPositions = trackDailyPositions
        self.ID = None
        self.isTradeOpen = False
        self.currTradeDirection = 0
        self.currPrice = 0.0
        self.CASH = 0
        self.LONG = 1
        self.SHORT = -1
        self.firsttimestamp = None
        self.lasttimestamp = None
        self.cnt = 0
        return

    def __str__(self):
        tradehistorystr = ""
        for trade in self.tradeHistory:
            tradehistorystr += trade.__str__() + "\n"
        return tradehistorystr

    def InitTickData(self, tickData):
        # tickData - data frame containing time stamped tick information.  A column will be added to this data to
        #            track every time period's position.  0 - No trade, 1 - Long position, -1 - Short position.

        self.tickData = tickData

        # Add column to track position for every time period and make sure entries are 0 for 'no trade'
        self.tickData['Position'] = np.zeros((len(tickData), 1))
        pass

    def UpdateTradePositions(self):
        # Find and update the positions between the open and close dates in the dataframe.  This function is based
        # off of values in self.currTrade.  This shouldn't be called until after openTimeStamp, closeTimeStamp, and
        # tradeDirection have been set.. or after CloseTrade has been called.

        # Only run through this if we're tracking daily positions
        if self.trackDailyPositions == False:
            return
        # Iterate through the array looking for relevant time stamps.

        index = 0
        for idx in self.tickData.iterrows():
            #print idx
            currtimestamp = datetime.datetime.strptime(self.tickData.ix[index]['Date'], "%Y-%m-%d")
            if currtimestamp >= self.currTrade.openTimeStamp and currtimestamp <= self.currTrade.closeTimeStamp:
                self.tickData.set_value(index, 'Position', self.currTrade.tradeDirection)
            index += 1

        pass

    def OpenTrade(self, equity, openprice, spread, direction, timestamp, id=None):
        if self.firsttimestamp == None:
            self.firsttimestamp = timestamp
        self.currTrade = TradeDetails()
        self.currTrade.OpenTrade(equity, openprice, spread, direction, timestamp, id)
        self.ID = id
        self.isTradeOpen = True
        self.currTradeDirection = direction
        #print "OpenTrade", equity, openprice, spread, direction, timestamp, id
        return

    def UpdateStats(self, closeprice):
        tradePL = self.currTrade.GetCurrentPL(closeprice)
        if tradePL > 0:
            if self.currTradeDirection == self.LONG:
                self.longWins += 1
            else:
                self.shortWins += 1
            self.totalWins += 1
        else:
            if self.currTradeDirection == self.LONG:
                self.longLosses += 1
            else:
                self.shortLosses += 1
            self.totalLosses += 1
        pass

    def CloseTrade(self, closeprice, timestamp, direction):
        self.lasttimestamp = timestamp
        # Close the trade
        self.currTrade.CloseTrade(closeprice, timestamp)
        tradePL = self.currTrade.GetCurrentPL(closeprice)

        if tradePL > 0 or self.cnt == 0:
            # add trade to the history if enabled
            if self.trackHistory == True:
                # Drop half of the losing trades
                self.tradeHistory.append(self.currTrade)
            # Add trade results to total PL
            self.totalPL += tradePL
            self.currTrade.SetTotalPL(self.totalPL)
            # Update stats
            self.UpdateStats(closeprice)
            # Update trade positions for this trade if it's being tracked
            self.UpdateTradePositions()
        if tradePL < 0:
            if self.cnt < 3:
                self.cnt += 1
            if self.cnt >= 3:
                self.cnt = 0
        self.ID = None
        self.isTradeOpen = False
        self.currTradeDirection = direction
        return

    def GetTradeCurrPL(self, currPrice):
        return self.currTrade.GetCurrentPL(currPrice)

    def UpdateCurrPrice(self, currPrice):
        self.currPrice = currPrice
        pass

    def GetTimeStepPL(self, nextPrice):
        # This gets the difference between the updated price and the next price.  Order of subtraction is based on
        # the direction of the trade.
        if self.currTradeDirection == self.LONG:
            return nextPrice - self.currPrice
        elif self.currTradeDirection == self.SHORT:
            return self.currPrice - nextPrice
        else:
            return 0.0

    def GetTradeCurrDuration(self):
        return self.currTrade.GetTradeDuration()

    def GetTotalPL(self):
        # This returns the cumulative PL prior to current trade (if any)
        return self.totalPL

    def GetTradeStatsStr(self):

        tradestatsstr = ""
        totalTrades = max((self.totalWins + self.totalLosses), 1)

        tradestatsstr += "Trading Stats:\n"
        tradestatsstr += "Total trades:\t %d\n" % totalTrades
        tradestatsstr += "Total Wins:\t\t %d, \t%0.2f%%\n" %(self.totalWins, (float(self.totalWins)/totalTrades)*100)
        tradestatsstr += "Total Losses:\t %d, \t%0.2f%%\n" %(self.totalLosses, (float(self.totalLosses)/totalTrades)*100)
        longTrades = max((self.longWins + self.longLosses), 1)
        shortTrades = max((self.shortWins + self.shortLosses), 1)
        tradestatsstr += "Long wins:\t\t %d, \t%0.2f%%\n" %(self.longWins, (float(self.longWins)/longTrades)*100)
        tradestatsstr += "Long losses:\t %d, \t%0.2f%%\n" %(self.longLosses, (float(self.longLosses)/longTrades)*100)
        tradestatsstr += "Short wins:\t\t %d, \t%0.2f%%\n" %(self.shortWins, (float(self.shortWins)/shortTrades)*100)
        tradestatsstr += "Short losses:\t %d, \t%0.2f%%\n" %(self.shortLosses, (float(self.shortLosses)/shortTrades)*100)
        tradestatsstr += "Total P/L:\t\t %0.2f\n" % self.totalPL
        tradestatsstr += "First timestamp: %s\n" % self.firsttimestamp
        tradestatsstr += "Last timestamp:\t %s\n" % self.lasttimestamp

        return tradestatsstr

    def PrintHistory(self):
        tradehistorystr = ""
        for trade in self.tradeHistory:
            tradehistorystr += trade.__str__()
            print trade

        totalTrades = max((self.totalWins + self.totalLosses), 1)
        print "Trading Stats:"
        print "Total trades:\t", totalTrades
        print "Total Wins:\t\t", self.totalWins, ", %0.2f%%" % ((float(self.totalWins)/totalTrades)*100)
        print "Total Losses:\t", self.totalLosses, ", %0.2f%%" % ((float(self.totalLosses)/totalTrades)*100)
        longTrades = max((self.longWins + self.longLosses), 1)
        shortTrades = max((self.shortWins + self.shortLosses), 1)
        print "Long wins:\t\t", self.longWins, ", %0.2f%%" % ((float(self.longWins)/longTrades)*100)
        print "Long losses:\t", self.longLosses, ", %0.2f%%" % ((float(self.longLosses)/longTrades)*100)
        print "Short wins:\t\t", self.shortWins, ", %0.2f%%" % ((float(self.shortWins)/shortTrades)*100)
        print "Short losses:\t", self.shortLosses, ", %0.2f%%" % ((float(self.shortLosses)/shortTrades)*100)
        print "Total P/L:\t\t", self.totalPL
        print "First timestamp:", self.firsttimestamp
        print "Last timestamp:\t", self.lasttimestamp
        return tradehistorystr

    def GetHistory(self):
        # Return list of TradeDetails
        return self.tradeHistory

    def getCurrID(self):
        # If application is interested in the ID for the current trade then it will be available (if set).
        return self.ID

    def GetIsTradeOpen(self):
        return self.isTradeOpen

    def GetCurrTradeDirection(self):
        return self.currTradeDirection



# --------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------
def ExecuteTestTrades():
    CASH = 0
    LONG = 1
    SHORT = 2

    openTS = datetime.datetime(2016, 04, 18)
    closeTS = datetime.datetime(2016, 04, 19)
    openPrice = 78.8
    closePrice = 78.2
    spread = 0.032

    tt = TradeTracking()
    tt.OpenTrade("AUDJPY", openPrice, spread, LONG, openTS)
    tt.CloseTrade(closePrice, closeTS)
    print tt

    openTS = datetime.datetime(2016, 04, 20)
    closeTS = datetime.datetime(2016, 04, 22)
    openPrice = 79.0
    closePrice = 79.8
    spread = 0.032

    tt.OpenTrade("AUDJPY", openPrice, spread, LONG, openTS)
    tt.CloseTrade(closePrice, closeTS)
    print ""
    print tt

    return

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run
# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    ExecuteTestTrades()
