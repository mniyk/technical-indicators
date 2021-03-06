"""technical_indicators.pyのunittest
"""
import logging
import unittest
from numpy import short

import pandas as pd

from technical_indicators.technical_indicators import TechnicalIndicators


logging.basicConfig(
    level=logging.DEBUG,
    format='\t'.join([
        '%(asctime)s',
        '%(levelname)s',
        '%(filename)s',
        '%(funcName)s',
        '%(processName)s',
        '%(process)d',
        '%(threadName)s',
        '%(thread)d',
        '%(message)s']))

logger = logging.getLogger(__name__)


class TestTechnicalIndicators(unittest.TestCase):
    def setUp(self) -> None:
        df = pd.read_pickle('candles.pickle')

        self.technical = TechnicalIndicators(df[:1000])

    def test_add_rci(self):
        self.technical.add_rci(calculation_column='close', periods=[9, 16])

        logger.debug(self.technical.df.iloc[-1, :])

        self.technical.add_rci(
            calculation_column='close', 
            periods=[9, 16],
            digits=2)

        logger.debug(self.technical.df.iloc[-1, :])

        self.technical.add_rci(
            calculation_column='close', 
            periods=[9, 16],
            change_range=False)

        logger.debug(self.technical.df.iloc[-1, :])

    def test_add_macd(self):
        self.technical.add_macd(
            calculation_column='close', 
            short=12,
            long=26,
            signal=9)

        logger.debug(self.technical.df.iloc[-1, :])

    def test_add_stochastic(self):
        self.technical.add_stochastic(
            calculation_column='close',
            periods=[12, 26, 54])

        logger.debug(self.technical.df.iloc[-1, :])

    def test_add_previous_value_shift_and_diff(self):
        self.technical.add_macd(
            calculation_column='close', 
            short=12,
            long=26,
            signal=9)

        self.technical.add_previous_value_shift_and_diff('MACD')

        logger.debug(self.technical.df.iloc[-2, :])
        logger.debug(self.technical.df.iloc[-1, :])
