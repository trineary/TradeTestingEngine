# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 12/14/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# TTEPaperEx2.py
#
# This file illustrates an example of trading rules that are engaged in a varied environment that is profitable
# and rejects the null hypothesis.
#
# --------------------------------------------------------------------------------------------------------------------


# Import standard packages

# Import my classes
from pytte.tte import TTE


def TestWhiteRealityCheck(tte, df):
    print "White Bootstrap"
    tte.select_bootstrap(tte.BOOTSTRAP_WHITE)
    pval = tte.get_pvalue(iterations=5000)
    print "pval:", pval
    tte.plot_pdf()
    print tte.get_trade_stats()
    tte.plot_trades_equity()

    pass


def TestMonteCarloBootstrap(tte, df):
    print "Monte Carlo Bootstrap"
    tte.select_bootstrap(tte.BOOTSTRAP_MONTE_CARLO)
    pval = tte.get_pvalue(iterations=5000)
    print "pval:", pval
    tte.plot_pdf()
    print tte.get_trade_stats()
    tte.plot_trades_equity()

    pass


def TestTTEBootstrap(tte, df):

    tte.select_bootstrap(tte.BOOTSTRAP_TTE)
    pval = tte.get_pvalue(iterations=5000)
    print "pval:", pval, "\n"
    tte.plot_pdf()
    tte.plot_trades_equity()
    tte.print_trade_history()
    tte.print_trade_stats()

    pass


if __name__ == "__main__":
    # Functions to run if this file is executed
    print "Run default function for ", __file__

    equity = "DIA"
    startDate = '2016-01-04'
    endDate = '2016-03-20'

    tte = TTE()
    df = tte.get_hist_data(equity, startDate, endDate)
    print len(df)

    # Trade 1
    tte.open_trade(0, tte.SHORT)
    tte.close_trade(5)

    # Trade 2
    tte.open_trade(8, tte.SHORT)
    tte.close_trade(12)

    # Trade 3
    tte.open_trade(15, tte.LONG)
    tte.close_trade(20)

    # Trade 4
    tte.open_trade(29, tte.LONG)
    tte.close_trade(34)

    # Trade 5
    tte.open_trade(39, tte.LONG)
    tte.close_trade(46)

    # Trade 6
    tte.open_trade(47, tte.SHORT)
    tte.close_trade(50)

    #TestWhiteRealityCheck(tte, df)
    TestMonteCarloBootstrap(tte, df)
    #TestTTEBootstrap(tte, df)



