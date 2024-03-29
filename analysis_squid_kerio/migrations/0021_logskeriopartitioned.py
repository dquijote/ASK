# Generated by Django 3.2.7 on 2023-09-21 20:47

from django.db import migrations, models
import psqlextra.manager.manager


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_squid_kerio', '0020_alter_user_cell'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogsKerioPartitioned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addres', models.PositiveBigIntegerField(verbose_name='IP')),
                ('user_name', models.CharField(max_length=200, verbose_name='Usuario')),
                ('date_time', models.DateTimeField(verbose_name='Fecha')),
                ('time_zone', models.CharField(max_length=100, verbose_name='Zona horario')),
                ('http_method', models.CharField(max_length=50, verbose_name='Metodo http')),
                ('url', models.CharField(max_length=10000, verbose_name='Url')),
                ('version_http', models.CharField(max_length=50, verbose_name='Version de http')),
                ('code_http', models.CharField(max_length=200, verbose_name='Codigo http')),
                ('size_transfered', models.IntegerField(verbose_name='Tamanno de transf')),
                ('count_requests_transferred', models.CharField(max_length=1000, verbose_name='Cant de transferencia')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
    ]
