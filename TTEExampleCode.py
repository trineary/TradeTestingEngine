# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 9/22/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# TestFile.py
#
# This file shows how to use the TTE package
#
# --------------------------------------------------------------------------------------------------------------------


# Import standard packages

# Import my classes
from pytte.tte import TTE


def TestWhiteRealityCheck(tte, df):

    #tte.open_trade(4, tte.LONG)
    #tte.close_trade(11)

    tte.open_trade(10, tte.SHORT)
    tte.close_trade(13)

    tte.select_bootstrap(tte.BOOTSTRAP_WHITE)
    pval = tte.get_pvalue(iterations=5000)
    print "pval:", pval
    tte.plot_pdf()
    print tte.get_trade_stats()
    tte.plot_trades_equity()

    pass


def TestMonteCarloBootstrap(tte, df):

    #tte.open_trade(4, tte.LONG)
    #tte.close_trade(11)

    tte.open_trade(10, tte.SHORT)
    tte.close_trade(13)

    tte.select_bootstrap(tte.BOOTSTRAP_MONTE_CARLO)
    pval = tte.get_pvalue(iterations=5000)
    print "pval:", pval
    tte.plot_pdf()
    print tte.get_trade_stats()
    tte.plot_trades_equity()

    pass


def TestTTEBootstrap(tte, df):

    #tte.open_trade(4, tte.LONG)
    #tte.close_trade(11)

    tte.open_trade(10, tte.SHORT)
    tte.close_trade(13)

    tte.select_bootstrap(tte.BOOTSTRAP_TTE)
    pval = tte.get_pvalue(iterations=5000)
    print "pval:", pval, "\n"
    tte.plot_pdf()
    tte.plot_trades_equity()
    tte.print_trade_history()
    tte.print_trade_stats()

    pass

def CompareBootstrapOutputs(tte, df):
    #tte.open_trade(4, tte.LONG)
    #tte.close_trade(11)

    tte.open_trade(10, tte.SHORT)
    tte.close_trade(13)

    # Get and display TTE Bootstrap pvalue
    #tte.select_bootstrap(tte.BOOTSTRAP_TTE)
    #pval = tte.get_pvalue(iterations=5000)
    #print "TTE pval:", pval

    # Get and display TTE Bootstrap pvalue
    #tte.select_bootstrap(tte.BOOTSTRAP_MONTE_CARLO)
    #pval = tte.get_pvalue(iterations=5000)
    #print "Monte Carlo pval:", pval

    # Get and display TTE Bootstrap pvalue
    tte.select_bootstrap(tte.BOOTSTRAP_WHITE)
    pval = tte.get_pvalue(iterations=5000)
    print "White pval:", pval

    pass

if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    equity = "SPY"
    startDate = '2016-08-20'
    endDate = '2016-09-16'

    tte = TTE()
    df = tte.get_hist_data(equity, startDate, endDate)

    #TestWhiteRealityCheck(tte, df)
    #TestMonteCarloBootstrap(tte, df)
    #TestTTEBootstrap(tte, df)
    CompareBootstrapOutputs(tte, df)













