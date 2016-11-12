# --------------------------------------------------------------------------------------------------------------------
#
# Patrick Neary
# Date: 11/12/2016
#
# Fin 5350 / Dr. Tyler J. Brough
# Trade Testing Engine:
#
# BootstrapABC.py
#
# Abstract base class for all tests developed to evaluate rules.
#
# --------------------------------------------------------------------------------------------------------------------


# Import standard packages
from abc import ABCMeta, abstractmethod


class BootstrapABC():
    """
    Base test class for bootstrap tests.

    InitTest will initialize the bootstrap test with data that it needs and parameters needed to build the
    sampling distribution.

    HasPredictivePower will take a percent gain from a rule and determine what the predictive power is

    SaveOutput will generate output for the test.. maybe
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def init_test(self):
        pass

    @abstractmethod
    def has_predictive_power(self):
        pass

    #@abstractmethod
    #def SaveOutput(self):
    #s    pass


