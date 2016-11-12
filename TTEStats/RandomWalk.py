# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 9/22/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# RandomWalk.py
#
# This file provides interface for trade testing statistics.  This code provides the ability to create a couple
# different random walks with various configuration options.
#
# --------------------------------------------------------------------------------------------------------------------

# Import standard packages
import numpy
import random

# Import my classes


# --------------------------------------------------------------------------------------------------------------------
# Class
# --------------------------------------------------------------------------------------------------------------------
class RandomWalk:

    minValue = 30
    useRandomSeed = False
    randomSeed = 0
    useMinValue = True

    def __init__(self, useMinValue=True, minValue=30, useSeed=False, randomSeed=50):
        # useMinValue - Set a minimum value for the random walk results
        # minValue - minimum value for the random walk results
        # useSeed - T/F use a seed for random()
        # randomSeed - seed value for random()

        # Set parameters
        self.type = type
        self.minValue = minValue
        self.useRandomSeed = useSeed
        self.randomSeed = randomSeed
        self.useMinValue = useMinValue

        # Set random seed if enabled
        if self.useRandomSeed is True:
            random.seed(self.randomSeed)

        return


    # --------------------------------------------------------------------------------------------------------------------
    # Random walk functions
    # --------------------------------------------------------------------------------------------------------------------

    def GetRandomWalk(self, dataLength=1500):
        # dataLength - length of random walk data to return to caller

        data = []
        deltas = numpy.random.normal(loc=0.0, scale=1.0, size=dataLength)

        # Initialize first value in the list
        data.append(random.random()*100)

        # Create the random walk
        for x in xrange(0, dataLength, 1):
            newVal = data[x] + deltas[x]
            data.append(newVal)

        # Make sure entire data set is above the minimum value if option is set
        if self.useMinValue is True:
            minVal = min(data)

            if minVal <= self.minValue:
                data = [x+(self.minValue + abs(minVal)) for x in data]

            print "min value: ", minVal, ", new min value: ", min(data)

        return data

    def GetDriftingRandomWalk(self,dataLength=1500, driftVal=1):
        # dataLength - length of random walk data to return to caller
        # driftVal - value to apply to the drift function

        data = []
        deltas = numpy.random.normal(loc=0.0, scale=1.0, size=dataLength)

        # Initialize first value in the list
        data.append(random.random()*100)

        # Create the random walk
        for x in xrange(0, dataLength, 1):
            newVal = data[x] + deltas[x] + driftVal
            data.append(newVal)

        # Make sure entire data set is above the minimum value if option is set
        if self.useMinValue is True:
            minVal = min(data)

            if minVal <= self.minValue:
                data = [x+(self.minValue + abs(minVal)) for x in data]

            print "min value: ", minVal, ", new min value: ", min(data)

        return data


# --------------------------------------------------------------------------------------------------------------------
# Test functions
# --------------------------------------------------------------------------------------------------------------------

from pytte import TSPlottingTools as ts

def testRandomWalk():
    rw = RandomWalk()

    data = rw.GetRandomWalk()
    ts.GenPlot([data])
    return


def testDriftingRandomWalk():
    rw = RandomWalk()

    data = rw.GetDriftingRandomWalk(driftVal=0.01)
    ts.GenPlot([data])
    return

# --------------------------------------------------------------------------------------------------------------------
# Default function when the file is run
# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    #testRandomWalk()
    testDriftingRandomWalk()
