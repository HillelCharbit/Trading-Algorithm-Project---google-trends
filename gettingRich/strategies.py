import pandas as pd
from models import ActionType, Position, PositionType, StrategySignal
from abc import ABC, abstractmethod
from typing import Tuple


class BaseStrategy(ABC):
    def __init__(self, sl_rate: float = None, tp_rate: float = None) -> None:
        super().__init__()
        self.sl_rate = sl_rate
        self.tp_rate = tp_rate

    @abstractmethod
    def calc_signal(self, data: pd.DataFrame):
        pass

    def calc_qty(self, real_price: float, balance: float, action: ActionType, **kwargs) -> float:
        if action == ActionType.BUY:
            qty = balance / real_price

        elif action == ActionType.SELL:
            qty = balance / real_price

        return qty

    def check_sl_tp(self, row: pd.Series, position: Position) -> Tuple[float, float, ActionType]:
        sl_res = self.is_stop_loss(row, position)
        if sl_res is not None:
            return sl_res

        tp_res = self.is_take_profit(row, position)
        if tp_res is not None:
            return tp_res

    def is_stop_loss(self, row: pd.Series, position: Position) -> Tuple[float, float, ActionType]:
        """
        Checks if the price has hit the stop-loss level.

        Returns:
            Tuple[float, float, ActionType] or None: If stop-loss is triggered, returns a tuple containing quantity and stop-loss price and action type, otherwise returns None.
        """
        if self.sl_rate is not None:
            long_stop_loss_price = position.price * (1 - self.sl_rate)
            if position.type == PositionType.LONG and row['Low'] >= long_stop_loss_price:
                return position.qty, long_stop_loss_price, ActionType.SELL

            short_stop_loss_price = position.price * (1 + self.sl_rate)
            if position.type == PositionType.SHORT and row['High'] <= short_stop_loss_price:
                return position.qty, short_stop_loss_price, ActionType.BUY

    def is_take_profit(self, row: pd.Series, position: Position) -> Tuple[float, float, ActionType]:
        """
        Checks if the price has hit the take-profit level.

        Returns:
            Tuple[float, float, ActionType] or None: If take-profit is triggered, returns a tuple containing quantity and take-profit price and action type, otherwise returns None.
        """
        if self.tp_rate is not None:
            long_take_profit_price = position.price * (1 + self.tp_rate)
            if position.type == PositionType.LONG and row['High'] <= long_take_profit_price:
                return position.qty, long_take_profit_price, ActionType.SELL

            short_take_profit_price = position.price * (1 - self.tp_rate)
            if position.type == PositionType.SHORT and row['Low'] >= short_take_profit_price:
                return position.qty, short_take_profit_price, ActionType.BUY


class best_crypto_strat(BaseStrategy):
    def __init__(self, sl_rate: float = None, tp_rate: float = None) -> None:
        super().__init__(sl_rate, tp_rate)

    @staticmethod
    def calc_TR(df):
        df['prev_close'] = df['close'].shift(1)
        tr = pd.Series(
            data=df.apply(
                lambda row: max(row['high'], row['prev_close']) - min(row['low'], row['prev_close'])
                if pd.notnull(row['prev_close']) else row['high'] - row['low'],
                axis=1
            ),
            index=df.index
        )
        return tr

    @staticmethod
    def calc_ATR(df, atr_length=14):
        # Calculate True Range (TR)
        tr = best_crypto_strat.calc_TR(df)

        # Calculate the Average True Range (ATR)
        atr = tr.rolling(window=atr_length,
                         min_periods=1).mean()  # Use min_periods=1 to get ATR values even if < atr_length
        return atr

    @staticmethod
    def calc_crossover(df, a, b):
        signals = pd.Series([StrategySignal.DO_NOTHING] * len(df))
        signals[(df[a] > df[b]) & (df[a].shift(1) < df[b].shift(1))] = StrategySignal.BUY
        signals[(df[a] < df[b]) & (df[a].shift(1) > df[b].shift(1))] = StrategySignal.SELL

        return signals

    @staticmethod
    def calc_UTBot(df, key_value, atr_length):
        loss_threshold = key_value * df['ATR']
        trailing_stop = pd.Series([None] * len(df))

        for i in range(1, len(df)):
            # implementation of calc_UTBot function here
            pass

        signals = best_crypto_strat.calc_crossover(df, 'close', 'trailing_stop')
        return signals

    @staticmethod
    def calc_EMA(df, length):
        EMA = df['close'].ewm(span=length, min_periods=length, adjust=False).mean()
        return EMA

    @staticmethod
    def MacdDiff(df, fast_length, slow_length):
        fastEMA = best_crypto_strat.calc_EMA(df, fast_length)
        slowEMA = best_crypto_strat.calc_EMA(df, slow_length)
        return fastEMA - slowEMA

    @staticmethod
    def smooth_srs(srs, smoothing_f):
        # implementation of smooth_srs function here
        pass

    @staticmethod
    def NormalizeSmoothSrs(series, window_length, smoothing_f):
        # implementation of NormalizeSmoothSrs function here
        pass
