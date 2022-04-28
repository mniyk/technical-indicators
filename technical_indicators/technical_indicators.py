"""テクニカル指標のモジュール
"""
from typing import List

import numpy as np
from pandas import DataFrame
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.stochastic import percent_k
from pyti.stochastic import percent_d
from pyti.stochrsi import stochrsi


class TechnicalIndicators:
    def __init__(self, df: DataFrame) -> None:
        """初期化

        Args:
            df (DataFrame): ローソク足のデータフレーム

        Examples:
            >>> technical = TechnicalIndicators(df)
        """
        self.df = df

    def add_rci(
        self, 
        calculation_column: str, 
        periods: List, 
        digits: int=4, 
        change_range: bool = True):
        """RCIの追加

        Args:
            calculation_column (str): 計算用の列名
            periods (List): 期間のリスト
            digits (int): 小数点の桁数
            change_range (bool): TrueであればRCIの範囲を0~200に変更

        Examples:
            >>> technical.add_rci('close', [12, 26, 54])
        """
        for period in periods:
            column_title = f'rci_{period}'

            self.df[column_title] = np.nan

        for i, _ in self.df.iterrows():
            for period in periods:
                rci_col = f'rci_{period}'

                if i >= period:
                    period_df = self.df.loc[i - period:i - 1].copy()
                    period_df['date_rank'] = np.arange(period, 0, -1)
                    period_df = period_df.sort_values(
                        calculation_column, 
                        ascending=False).reset_index(drop=True)
                    period_df['price_rank'] = np.arange(1, period + 1)
                    period_df['delta'] = (
                        period_df['price_rank'] - period_df['date_rank']) ** 2
                    d = period_df['delta'].sum()
                    self.df.loc[i, rci_col] = (
                        (1 - (6 * d) / (period ** 3 - period)) * 100).round(
                            digits)

        if change_range:
            self.change_rci_range()

    def change_rci_range(self):
        """RCIの範囲を0~200に変更
        
        Examples:
            >>> self.change_rci_range()
        """
        for column in self.df.columns:
            if 'rci_' in column:
                self.df[column] = self.df[column] + 100

    def add_macd(
        self, 
        calculation_column: str, 
        short: int, 
        long: int, 
        signal: int, 
        digits: int=4):
        """MACDの追加

        Args:
            calculation_column (str): 計算用の列名
            short (int): 短期
            long (int): 長期
            signal (int): シグナル
            digits (int): 小数点の桁数
        
        Examples:
            >>> technical.add_macd('close', 12, 26, 9)
        """
        self.df[f'macd_{short}_{long}'] = macd(
            self.df[calculation_column].values.tolist(), short, long)
        self.df[f'macd_signal_{signal}'] = sma(
            self.df[f'macd_{short}_{long}'].values.tolist(), signal)

        self.df[f'macd_{short}_{long}'] = self.df[
            f'macd_{short}_{long}'].round(digits)
        self.df[f'macd_signal_{signal}'] = (
            self.df[f'macd_signal_{signal}'].round(digits))

    def add_stochastic(
        self, 
        calculation_column: str,
        periods: List,
        digits: int=4):
        """ストキャスティクスの追加

        Args:
            calculation_column (str): 計算用の列名
            periods (List): 期間のリスト
            digits (int): 小数点の桁数

        Examples:
            >>> technical.add_stochastic('close', [12, 26, 54])
        """
        for period in periods:
            self.df[f'stoch_k_{period}'] = percent_k(
                self.df[calculation_column].values.tolist(), 
                period).round(digits)
            self.df[f'stoch_d_{period}'] = percent_d(
                self.df[calculation_column].values.tolist(), 
                period).round(digits)
            self.df[f'stoch_rsi_{period}'] = stochrsi(
                self.df[calculation_column].values.tolist(), 
                period).round(digits)

    def add_previous_value_shift_and_diff(
        self, technical_indicator_name: str, diff: bool = True):
        """前回値と前回値との差を追加

        Args:
            technical_indicator_name (str): テクニカル指標の名前
            diff (bool): Trueであれば、前回値との差を追加
        
        Examples:
            >>> technical.add_previous_value_shift('RCI')
        """
        for column in self.df.columns:
            if technical_indicator_name.lower() in column:
                self.df[f'{column}_shift'] = self.df[column].shift()

                if diff:
                    self.df[f'{column}_shift_diff'] = (
                        self.df[column] - self.df[f'{column}_shift'])
