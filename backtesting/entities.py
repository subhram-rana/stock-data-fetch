import json
from typing import List
from datetime import date, time, datetime
from abc import ABC, abstractmethod
from backtesting.enums import Market
from backtesting.models import Trade, Backtesting, DailyBacktesting
from price_app.scripts.momentum_analysis.momentum_analysis import time_str_format


class ConfigBase(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, my_dict: dict):
        ...

    @abstractmethod
    def to_json(self) -> str:
        ...

    @staticmethod
    @abstractmethod
    def from_string(meta: str):
        ...


class ChartConfig(ConfigBase):
    def __init__(
            self,
            smooth_price_averaging_method: str = None,
            smooth_price_period: int = None,
            smooth_price_ema_period: int = None,
            smooth_slope_averaging_method: str = None,
            smooth_slope_period: int = None,
            smooth_slope_ema_period: int = None,
    ):
        self.smooth_price_averaging_method = smooth_price_averaging_method
        self.smooth_price_period = smooth_price_period
        self.smooth_price_ema_period = smooth_price_ema_period
        self.smooth_slope_averaging_method = smooth_slope_averaging_method
        self.smooth_slope_period = smooth_slope_period
        self.smooth_slope_ema_period = smooth_slope_ema_period

    def to_dict(self) -> dict:
        return {
            'smooth_price_averaging_method': str(self.smooth_price_averaging_method),
            'smooth_price_period': int(self.smooth_price_period),
            'smooth_price_ema_period': int(self.smooth_price_ema_period),
            'smooth_slope_averaging_method': str(self.smooth_slope_averaging_method),
            'smooth_slope_period': int(self.smooth_slope_period),
            'smooth_slope_ema_period': int(self.smooth_slope_ema_period),
        }

    @classmethod
    def from_dict(cls, my_dict: dict):
        return ChartConfig(
            my_dict['smooth_price_averaging_method'],
            my_dict['smooth_price_period'],
            my_dict['smooth_price_ema_period'],
            my_dict['smooth_slope_averaging_method'],
            my_dict['smooth_slope_period'],
            my_dict['smooth_slope_ema_period'],
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_string(meta: str):
        return ChartConfig.from_dict(json.loads(meta))


class EntryCondition:
    def __init__(
            self,
            max_variance: float = None,
            min_abs_trend_slope: float = None,
            min_abs_price_slope: float = None,
            min_abs_price_momentum: float = None,
    ):
        self.max_variance = max_variance
        self.min_abs_trend_slope = min_abs_trend_slope
        self.min_abs_price_slope = min_abs_price_slope
        self.min_abs_price_momentum = min_abs_price_momentum

    def to_dict(self) -> dict:
        return {
            'max_variance': self.max_variance,
            'min_abs_trend_slope': self.min_abs_trend_slope,
            'min_abs_price_slope': self.min_abs_price_slope,
            'min_abs_price_momentum': self.min_abs_price_momentum,
        }

    @classmethod
    def from_dict(cls, my_dict: dict):
        return EntryCondition(
            my_dict['max_variance'],
            my_dict['min_abs_trend_slope'],
            my_dict['min_abs_price_slope'],
            my_dict['min_abs_price_momentum'],
        )


class ExitCondition:
    def __init__(
            self,
            profit_target_type: str = None,
            profit_target_points: float = None,
            stoploss_type: str = None,
            stoploss_points: float = None,
    ):
        self.profit_target_type = profit_target_type
        self.profit_target_points = profit_target_points
        self.stoploss_type = stoploss_type
        self.stoploss_points = stoploss_points

    def to_dict(self) -> dict:
        return {
            'profit_target_type': str(self.profit_target_type),
            'profit_target_points': int(self.profit_target_points),
            'stoploss_type': str(self.stoploss_type),
            'stoploss_points': int(self.stoploss_points),
        }

    @classmethod
    def from_dict(cls, my_dict: dict):
        return ExitCondition(
            my_dict['profit_target_type'],
            my_dict['profit_target_points'],
            my_dict['stoploss_type'],
            my_dict['stoploss_points'],
        )


class TradeConfig(ConfigBase):
    def __init__(
            self,
            trend_line_time_period: int = None,
            min_entry_time: time = None,
            entry_conditions: List[EntryCondition] = None,
            exit_condition: ExitCondition = None,
    ):
        self.trend_line_time_period = trend_line_time_period
        self.min_entry_time = min_entry_time
        self.entry_conditions = entry_conditions
        self.exit_condition = exit_condition

    def to_dict(self):
        return {
            'trend_line_time_period': int(self.trend_line_time_period),
            'min_entry_time': str(self.min_entry_time.strftime(time_str_format)),
            'entry_conditions': [
                entry_condition.to_dict()
                for entry_condition in self.entry_conditions
            ],
            'exit_condition': self.exit_condition.to_dict(),
        }

    @classmethod
    def from_dict(cls, my_dict: dict):
        return TradeConfig(
            my_dict['trend_line_time_period'],
            datetime.strptime(my_dict['min_entry_time'], "%H:%M:%S").time(),
            [EntryCondition.from_dict(entry_condition) for entry_condition in my_dict['entry_conditions']],
            ExitCondition.from_dict(my_dict['exit_condition']),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_string(trade_config_str: str):
        return TradeConfig.from_dict(json.loads(trade_config_str))


class BacktestingInput:
    def __init__(
            self,
            market: Market = None,
            start_date: date = None,
            start_time: time = None,
            end_date: date = None,
            end_time: time = None,
            chart_config: ChartConfig = None,
            trade_config: TradeConfig = None,
            purpose: str = None,
    ):
        self.market = market
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.chart_config = chart_config
        self.trade_config = trade_config
        self.purpose = purpose

    def get_config_dict(self) -> dict:
        return {
            'market': self.market.name,
            'chart_config': self.chart_config.to_dict(),
            'trade_config': self.trade_config.to_dict(),
        }

    def to_dict(self) -> dict:
        d = self.get_config_dict()
        d['start_date'] = self.start_date
        d['start_time'] = self.start_time
        d['end_date'] = self.end_date
        d['end_time'] = self.end_time
        d['purpose'] = self.purpose

        return d

    @classmethod
    def from_json_file(
            cls,
            market: Market,
            start_date: date,
            start_time: time,
            end_date: date,
            end_time: time,
            json_abs_file_path: str
    ):
        with open(json_abs_file_path, "r") as json_file:
            data = json.load(json_file)

        return BacktestingInput(
            market=market,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            chart_config=ChartConfig.from_dict(data['chart_config']),
            trade_config=TradeConfig.from_dict(data['trade_config']),
            purpose=f'Running from JSON file: {datetime.now()}',
        )


class DailyBacktestingResult:
    def __init__(
            self,
            daily_back_testing: DailyBacktesting,
            trades: List[Trade],
    ):
        self.daily_back_testing = daily_back_testing
        self.trades = trades

    def calculate_success_rate(self):
        self.daily_back_testing.calculate_success_rate()

    def save_to_db(self):
        self.daily_back_testing.save()
        for trade in self.trades:
            trade.save()


class BacktestingResult:
    def __init__(
            self,
            back_testing: Backtesting,
            daily_back_testing_results: List[DailyBacktestingResult],
    ):
        self.back_testing = back_testing
        self.daily_back_testing_results = daily_back_testing_results

    def save_to_db(self):
        self.back_testing.save()
        for daily_back_testing_result in self.daily_back_testing_results:
            daily_back_testing_result.save_to_db()


class LinearRegressionLine:
    def __init__(self, m: float, c: float, variance: float):
        self.m = m
        self.c = c
        self.variance = variance
