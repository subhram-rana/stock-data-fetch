from django.core.management.base import BaseCommand
from backtesting.momentum_1min_candle.optimisation.common import run_algo_on_test_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        run_algo_on_test_data()
