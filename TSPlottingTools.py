# TSPlottingTools.py
# Patrick Neary
# 03/02/2016
# CS 6950
#
# Description:  Class for plotting time series data.  (Other data too perhaps, but main emphasis is time series.)


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab


#==================================================================================================================
#
#==================================================================================================================

def GetDates(numdays):
    dates = pd.date_range(pd.datetime.today(), periods=numdays).tolist()
    return dates

def GenPlot(plots, plotsInSubPlot=[1], dataLabels=None, subplotTitles=None, xlabels=None, ylabels=None, xaxis=None,
            gridon=False):

    # plots - a list of data sets to be added to the plot
    # plotsInSubPlot - list of number of data sets to add to each plot.  For example [2, 3] two data sets in first
    #                   subplot and 3 data sets in the second subplot
    # plotLabels - list of labels for data series. plotLabels=['label1', 'label2', 'label3', etc.]
    # subplotTitles - list of titles for each of the subplots
    # xlabel - x label for all subplots
    # ylabel - y label for all subplots
    # xaxis - xaxis values.  Default is to just use 0-N
    # example of call: pt.GenPlot([close, sma, sma], plotsInSubPlot=[2,1])
    numSubplots = len(plotsInSubPlot)
    plotCount = 0

    # if x axis isn't defined then just generate values 0 to N
    if xaxis is None:
        if(numSubplots > 1):
            stop = len(plots[0])
        else:
            stop = len(plots[0])
        xaxis = range(0, stop, 1)

    xindex = range(0, len(plots[0]), 1)

    f, axarr = pylab.subplots(nrows=numSubplots, sharex=True)

    for subplot in range(0, numSubplots, 1):
        numplots = plotsInSubPlot[subplot]

        # get title for the subplot
        plottitle = ''
        if subplotTitles != None:
            plottitle = subplotTitles[subplot]

        xlabel = ''
        ylabel = ''
        # get x label for subplot
        if xlabels != None:
            xlabel = xlabels[subplot]
        # get y label for subplot
        if ylabels != None:
            ylabel = ylabels[subplot]

        slabel = ''
        for count in range(0, numplots):
            # Get data series labels
            if dataLabels != None:
                if dataLabels[plotCount]:
                    slabel = dataLabels[plotCount]
            #else: slabel = ""


            # Check to see if there is a label in first cell of data.  If so remove it.  If there isn't currently a
            # label for the data, then set it as the label.
            data = plots[plotCount]
            #print "Subplot: ", subplot, " plotCount: ", plotCount, " Data: ", data
            if isinstance(data[0], basestring):
                print "First entry is a string"
                if slabel is '':
                    slabel = data[0]
                data = data[1:len(data)]
                if len(data) != len(xaxis):
                    xindex = xindex[1:len(xaxis)]

            # Add data series to the subplot
            if(numSubplots > 1):
                axarr[subplot].plot(xindex, data, label=slabel)
                axarr[subplot].legend(loc='upper right')
                axarr[subplot].set_title(plottitle)
                axarr[subplot].set_ylabel(ylabel)
                axarr[subplot].set_xlabel(xlabel)
                axarr[subplot].grid(gridon)
            else:
                pylab.plot(xindex, data, label=slabel)
                pylab.xticks(xindex, xaxis)
                pylab.legend(loc='upper right')
                pylab.title(plottitle)
                pylab.ylabel(ylabel)
                pylab.xlabel(xlabel)
                pylab.grid(gridon)
            plotCount += 1

    f.autofmt_xdate()
    pylab.tight_layout() # This improves the layouts so words aren't overlapping each other
    pylab.legend(loc='upper right')
    pylab.show()
    print "Done generating plot"
    return


def PlotPortfolioPerformance(baseline, accountBalance, dates, baselineName):
    # baseline - DJIA/SPY, etc. to compare performance against
    # accountBalance - account value over time of interest
    # dates - dates/x axis values to plot against

    ylabel = "Price (USD)"
    GenPlot([baseline, accountBalance], plotsInSubPlot=[2], plotLabels=[baselineName, 'Account Val'], ylabels=[ylabel], xaxis=dates, gridon=True)

    return

#==================================================================================================================
#
#==================================================================================================================

def test1():
    # Test PlotPortfolioPerformance code
    baseline = np.random.random(100)
    accountBalance = np.random.random(100)
    dates = GetDates(100)
    PlotPortfolioPerformance(baseline, accountBalance, dates, baselineName='DJIA')
    return


def test2():
    # Test GenPlot code
    baseline = np.random.random(100)
    accountBalance = np.random.random(100)
    stock2 = np.random.random(100)
    dates = GetDates(100)
    print "Dates type"
    print type(dates)
    print dates

    #GenPlot([baseline, accountBalance, stock2], plotsInSubPlot=[2, 1], dataLabels=['plot1', 'plot2', 'plot3'],
    #           subplotTitles=['title1',  'title2'], xlabels=['xaxis1', 'xaxis2'], ylabels=['yaxis1', 'yaxis2'],
    #           gridon=True, xaxis=dates)

    #print baseline

    GenPlot([baseline], plotsInSubPlot=[1], dataLabels=['plot1'],
            subplotTitles=['title1'], xlabels=['xaxis1'], ylabels=['yaxis1'],
            gridon=True, xaxis=dates)
    return


#==================================================================================================================
#
#==================================================================================================================

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__
    test2()


