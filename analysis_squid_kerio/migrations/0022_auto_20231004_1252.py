# Generated by Django 3.2.7 on 2023-10-04 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_squid_kerio', '0021_logskeriopartitioned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slicetmp',
            name='end',
            field=models.IntegerField(default=10, verbose_name='Slice fin'),
        ),
        migrations.AlterField(
            model_name='slicetmp',
            name='multiplier',
            field=models.IntegerField(default=10, verbose_name='Multiplicador '),
        ),
        migrations.AlterField(
            model_name='slicetmp',
            name='start',
            field=models.IntegerField(default=0, verbose_name='Slice inicio'),
        ),
        migrations.AlterField(
            model_name='slicetmp',
            name='step',
            field=models.IntegerField(default=10, verbose_name='Slice paso'),
        ),
    ]
