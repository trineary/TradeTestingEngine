# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 12/14/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# TTEPaperEx1.py
#
# This file shows illustrates an example of trading rules that are active during a trend that, while provfitable,
# fails to reject the null hypothesis.
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
    #tte.plot_trades_equity()
    tte.print_trade_history()

    pass


def TestTTEBootstrap(tte, df):
    print "TTE Bootstrap"
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
    startDate = '2016-02-12'
    endDate = '2016-04-20'

    tte = TTE()
    df = tte.get_hist_data(equity, startDate, endDate)

    # Trade 1
    tte.open_trade(0, tte.LONG)
    tte.close_trade(5)

    # Trade 2
    tte.open_trade(10, tte.LONG)
    tte.close_trade(15)

    # Trade 3
    tte.open_trade(10, tte.LONG)
    tte.close_trade(20)

    # Trade 4
    #tte.open_trade(20, tte.LONG)
    #tte.close_trade(25)

    # Trade 5
    #tte.open_trade(30, tte.LONG)
    #tte.close_trade(35)

    # Trade 6
    #tte.open_trade(40, tte.LONG)
    #tte.close_trade(45)

    #TestWhiteRealityCheck(tte, df)
    #TestMonteCarloBootstrap(tte, df)
    TestTTEBootstrap(tte, df)



