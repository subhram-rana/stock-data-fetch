from django.db import models


class Price(models.Model):
    timestamp = models.DateTimeField(null=False, db_index=True)
    tick_price = models.FloatField(null=False, default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f"timestamp: {self.timestamp}, Tick price: {self.tick_price}"


class NiftyPrice(Price):
    class Meta:
        db_table = 'nifty_price'


class BankNiftyPrice(Price):
    class Meta:
        db_table = 'bank_nifty_price'
