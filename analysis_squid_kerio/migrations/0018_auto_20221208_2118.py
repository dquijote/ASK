# Generated by Django 3.2.7 on 2022-12-08 21:18

from django.db import migrations
from psqlextra.backend.migrations.operations import PostgresAddRangePartition


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_squid_kerio', '0017_auto_20221208_2118'),
    ]

    operations = [
        PostgresAddRangePartition(
            model_name="LogsSquidPartitioned",
            name="logsquid_20221126_20221201",
            from_values="2022-11-26",
            to_values="2022-12-01",
        ),
    ]
