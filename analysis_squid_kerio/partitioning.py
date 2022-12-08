from psqlextra.partitioning import PostgresPartitioningManager

from dateutil.relativedelta import relativedelta

from psqlextra.partitioning import (
    PostgresPartitioningManager,
    PostgresCurrentTimePartitioningStrategy,
    PostgresTimePartitionSize,
    partition_by_current_time,
)
from psqlextra.partitioning.config import PostgresPartitioningConfig

from analysis_squid_kerio.models import LogsSquidPartitioned
from .models import LogsSquid, LogsKerio

# manager = PostgresPartitioningManager(...)

# myapp/settings.py


manager = PostgresPartitioningManager([
    # 3 partitions ahead, each partition is one month
    # delete partitions older than 6 months
    # partitions will be named `[table_name]_[year]_[3-letter month name]`.
    # PostgresPartitioningConfig(
    #     model=LogsSquid,
    #     strategy=PostgresCurrentTimePartitioningStrategy(
    #         size=PostgresTimePartitionSize(months=1),
    #         count=3,
    #         max_age=relativedelta(months=6),
    #     ),
    # ),
    # # 6 partitions ahead, each partition is two weeks
    # # delete partitions older than 8 months
    # # partitions will be named `[table_name]_[year]_week_[week number]`.
    # PostgresPartitioningConfig(
    #     model=MyPartitionedModel,
    #     strategy=PostgresCurrentTimePartitioningStrategy(
    #         size=PostgresTimePartitionSize(weeks=2),
    #         count=6,
    #         max_age=relativedelta(months=8),
    #     ),
    # ),
    # 12 partitions ahead, each partition is 5 days
    # old partitions are never deleted, `max_age` is not set
    # partitions will be named `[table_name]_[year]_[month]_[month day number]`.
    PostgresPartitioningConfig(
        model=LogsSquidPartitioned,
        strategy=PostgresCurrentTimePartitioningStrategy(
            size=PostgresTimePartitionSize(days=5),
            count=36,
            max_age=relativedelta(months=6),

        ),
    ),
])
