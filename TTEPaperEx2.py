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


def PrintResults(tte, title=None):

    pval = tte.get_pvalue(iterations=5000)
    print "pval:", pval, "\n"
    tte.print_trade_history()
    tte.print_trade_stats()
    tte.plot_all(title)

    pass

def TestWhiteRealityCheck(tte):
    print "White Bootstrap"
    tte.select_bootstrap(tte.BOOTSTRAP_WHITE)
    PrintResults(tte, "White Bootstrap")

    pass


def TestMonteCarloBootstrap(tte):
    print "Monte Carlo Bootstrap"
    tte.select_bootstrap(tte.BOOTSTRAP_MONTE_CARLO)
    PrintResults(tte, "Monte Carlo Bootstrap")

    pass


def TestTTEBootstrap(tte):
    print "TTE Bootstrap"
    tte.select_bootstrap(tte.BOOTSTRAP_TTE)
    PrintResults(tte, "TTE Bootstrap")

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
    #tte.open_trade(15, tte.LONG)
    #tte.close_trade(20)

    # Trade 4
    tte.open_trade(29, tte.LONG)
    tte.close_trade(34)

    # Trade 5
    #
    tte.open_trade(39, tte.LONG)
    tte.close_trade(46)

    # Trade 6
    tte.open_trade(47, tte.LONG)
    tte.close_trade(50)

    #TestWhiteRealityCheck(tte)
    #TestMonteCarloBootstrap(tte)
    TestTTEBootstrap(tte)



