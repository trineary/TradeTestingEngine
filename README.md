# TradeTestingEngine

**Background**

The Trade Testing Engine is a Python package for helping ascertain whether trading strategies have predictive capabilities or not.  These statistical approaches were originally developed and written about in a number of different journals [1], [2], [3].

This project attempts to implement a variation of White's test, a Monte Carlo test, and a new test.  The purpose of these tests is to establish a null hypothesis that it's not possible to predict where the market is going to go.  The goal is to reject the null hypothesis and show that there is a high probability that a trading strategy does indeed have some predictive ability.  Generally with hypothesis testing, a p-value of 0.05 or less is considered significant.  The output of the TTE test is a p-value that the user is able to interpret.

This code consists of several different blocks: the interface, trade tracking, and the bootstrap algorithms.

*Interface*

The interface provides a handful of easy calls that the user interacts with in conjuction with their trading algorithm.  These calls will be discussed in more detail later with an example.

*Trade Tracking*

The trade tracking component tracks all trades made by the user and generates a handful of statistics at the end.  It helps track information that is used by the bootstrap algorithms.

*Bootstrap Algorithms*

As previously mentioned, the bootstrap algorithms implement some statistical tools to help determine if a trading strategy has predictive capability.  For those that are interested, the White and Monte Carlo tests are described in detail here [4].



**Example**

This example is modified from the TTEPaperEx2 file in this repository.  I'll post the code and then describe what's happening.


    equity = "DIA"
    startDate = '2016-01-04'
    endDate = '2016-03-20'

    tte = TTE()
    df = tte.get_hist_data(equity, startDate, endDate)

    *Trade 1*
    tte.open_trade(0, tte.SHORT)
    tte.close_trade(5)

    * Trade 2*
    tte.open_trade(8, tte.SHORT)
    tte.close_trade(12)

    * Trade 3*
    tte.open_trade(15, tte.LONG)
    tte.close_trade(20)

    tte.select_bootstrap(tte.BOOTSTRAP_TTE)
    pval = tte.get_pvalue(iterations=5000)
    tte.print_trade_history()
    tte.print_trade_stats()
    tte.plot_all(title)    

*Example Explanation*

This example starts out by defining an equity, start date, and end date.  After the tte object is created, those three values are used to grab a historical set of open, high, low, close data from yahoo finance.  The get_hist_data call returns the specified data in a dataframe.  That information is also stored internally for use by the algorithms.

As the user steps sequentially through the time series in the dataframe, the user's algorithm will specify when to make entries and exits.  When a new position is to be entered, the user calls open_trade with two parameters.  The first parameter is the index to the current line in the dataframe in which the entry is made.  The second parameter is the direction of the trade.  When the trade is done, the user again supplies the index for the dataframe entry that their algorithm decides to claose the trade on.

Once the user has finished opening and closing trades, they specify which bootstrap to use by calling select_bootstrap.  The user may then get the pvalue for the trades made by calling get_pvalue.

Of interest as well are some of the printing and plotting functions.  The print_trade_history call generates a list of all the trades made during the back test.  The print_trade_stats call lists some basic stats of the trades made, number of winning nad losing trades, etc.  Finally the plot_all call brings up a plot showing the distribution for the bootstrap, the time series that the user specified, and a graph showing where the long and short trades were made.

This project is a work in progress, so any constructive criticism is welcome.

**Pseudo Bibliography**

[1] Halbert White, A Reality Check for Data Snooping, Econometrica, 2000

[2] William Brock and Josef Lakonishok and Blake Lebaron, Simple Technical Trading Rules and the Stochastic Properties of Stock Returns, The Journal of Finance, 1992

[3] Ryan Sullivan and Allan Timmermann and Halbert White, Data-Snooping, Technical Trading Rule Performance, and the Bootstrap, The Journal of Finance, 1999

[4] David Aronson, Evidence-Based Technical Analysis, Wiley & Sons, 2007
