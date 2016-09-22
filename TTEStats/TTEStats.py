# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 9/21/2016
#
# Fin 5350
# Trade Testing Engine:
#
# TTEStats.py
#
# This file provides interface for trade testing statistics.  This code uses the following models to create simulations
# of the market:
# 1. Random walk
# 2. AR(1)
# 3. GARCH-M
# 4. EGARCH
#
# --------------------------------------------------------------------------------------------------------------------

# Import standard packages


# Import my classes


# Global values for selecting different options


class TTEStats:


    def __init__(self):

        return



# --------------------------------------------------------------------------------------------------------------------
# Test functions

import TSPlottingTools as ts

def testRandomWalk():
    data = [xrange(0,20,1)]
    ts.GenPlot(data)
    return

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    testRandomWalk()
