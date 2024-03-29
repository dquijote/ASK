# Generated by Django 3.2.7 on 2022-12-08 21:09

from django.db import migrations
from psqlextra.backend.migrations.operations import PostgresAddRangePartition


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_squid_kerio', '0008_auto_20221208_2109'),
    ]

    operations = [
        PostgresAddRangePartition(
            model_name="LogsSquidPartitioned",
            name="logsquid_20221011_20221016",
            from_values="2022-10-11",
            to_values="2022-10-16",
        ),
    ]
