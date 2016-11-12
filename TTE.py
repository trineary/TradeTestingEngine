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


# Import my classes

from tradelogger import TradeLogger
from TSData.TSData import TSData, ReturnsDataSource, TSDataSource
from TSDataInit import TSDataInit


class TTE:

    def __init__(self,

                 data_source=TSDataSource.source_yahoo,
                 returns_calc=ReturnsDataSource.original_data):
        """
        Initialize the Trede Testing Engine parameters.


        data_source: source of data to use, internal connection to yahoo or from user data set.  Default is yahoo.
        returns_calc: approach to calculating returns based on rule entries/exits.  Default is to use the original data.

        """

        self.__tsdata = TSData()

        return



# --------------------------------------------------------------------------------------------------------------------
# Test functions


# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__


