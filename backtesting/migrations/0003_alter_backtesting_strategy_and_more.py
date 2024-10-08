# Generated by Django 4.0 on 2024-10-08 19:46

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('backtesting', '0002_alter_dailybacktesting_success_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backtesting',
            name='strategy',
            field=django_mysql.models.EnumField(choices=[('MOMENTUM_V1', 'MOMENTUM_V1'), ('ONE_MINUTE_CANDLESTICK_MOMENTUM', 'ONE_MINUTE_CANDLESTICK_MOMENTUM')]),
        ),
        migrations.AlterField(
            model_name='optimisation',
            name='strategy',
            field=django_mysql.models.EnumField(choices=[('MOMENTUM_V1', 'MOMENTUM_V1'), ('ONE_MINUTE_CANDLESTICK_MOMENTUM', 'ONE_MINUTE_CANDLESTICK_MOMENTUM')]),
        ),
    ]
