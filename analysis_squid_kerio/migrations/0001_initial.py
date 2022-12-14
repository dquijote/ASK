# Generated by Django 3.2.7 on 2022-09-09 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryBlackListDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('typeEntity', models.CharField(choices=[('UEB', 'UEB'), ('Dir', 'Direccion')], default='UEB', max_length=10, verbose_name='Clasificacion')),
            ],
        ),
        migrations.CreateModel(
            name='LogsKerio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addres', models.IntegerField(verbose_name='IP')),
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
        ),
        migrations.CreateModel(
            name='LogsSquid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.CharField(default=1627704012, max_length=100, verbose_name='Time Stamp')),
                ('date_time', models.DateTimeField(verbose_name='Fecha')),
                ('time_request', models.IntegerField(verbose_name='Duracion de consulta')),
                ('ip_client', models.IntegerField(verbose_name='Ip cliente')),
                ('cache_result_code', models.CharField(max_length=50, verbose_name='Codigo de cache')),
                ('size_transfered', models.IntegerField(verbose_name='Tamanno de transf')),
                ('http_method', models.CharField(max_length=50, verbose_name='Metodo http')),
                ('url', models.CharField(max_length=10000, verbose_name='Url')),
                ('user_name', models.CharField(max_length=200, verbose_name='Usuario')),
                ('request_server_name', models.CharField(max_length=200, verbose_name='Nombre servidor')),
                ('content_type', models.CharField(max_length=100, verbose_name='Tipo de contenido')),
            ],
        ),
        migrations.CreateModel(
            name='SearchParameterSquid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_slice', models.IntegerField(verbose_name='Paso Slice')),
                ('start_slice', models.IntegerField(verbose_name='Inicio Slice')),
                ('end_slice', models.IntegerField(verbose_name='Fin Slice')),
                ('multiplier_slice', models.IntegerField(verbose_name='Multiplicador Slice')),
                ('date_start', models.DateField(verbose_name='Fecha Inicial')),
                ('date_end', models.DateField(verbose_name='Fecha Final')),
                ('user', models.CharField(blank=True, default=None, max_length=50, verbose_name='Usuario')),
                ('category_black_list', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='analysis_squid_kerio.categoryblacklistdomain')),
            ],
        ),
        migrations.CreateModel(
            name='SliceTmp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField(verbose_name='Slice inicio')),
                ('end', models.IntegerField(verbose_name='Slice fin')),
                ('step', models.IntegerField(verbose_name='Slice paso')),
                ('multiplier', models.IntegerField(verbose_name='Multiplicador ')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('cell', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('lastName1', models.CharField(max_length=200, verbose_name='Primer Apellido')),
                ('lastName2', models.CharField(max_length=200, verbose_name='Segundo Apellido')),
                ('mail', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('planeData', models.IntegerField(verbose_name='Plan de Datos (MB)')),
                ('serviceTypeMail', models.CharField(choices=[('nacional', 'Nacional'), ('internacional', 'Internancional')], default='nacional', max_length=15, verbose_name='Tipo de servicio Mail')),
                ('serviceTypeNavPC', models.CharField(choices=[('nacional', 'Nacional'), ('internacional', 'Internancional')], default='nacional', max_length=15, verbose_name='Tipo de servicio Nav PC')),
                ('serviceTypeNavCell', models.CharField(choices=[('internacional', 'Internancional'), ('correo', 'correo')], default='internacional', max_length=15, verbose_name='Tipo de servicio Nav Cell')),
                ('root', models.BooleanField(default=False, verbose_name='Permiso Admin')),
                ('quickAnswer', models.BooleanField(default=False, verbose_name='Grup. Respueta Rapida')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis_squid_kerio.entity')),
            ],
        ),
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_social_network', models.CharField(max_length=500, verbose_name='Id Red Social')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre de red social')),
                ('description', models.CharField(max_length=300, verbose_name='Descripcion')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis_squid_kerio.user')),
            ],
        ),
        migrations.CreateModel(
            name='BlackListDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateTimeField(verbose_name='Fecha entrada')),
                ('domain', models.CharField(max_length=1000, verbose_name='Dominio')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis_squid_kerio.categoryblacklistdomain')),
            ],
        ),
        migrations.CreateModel(
            name='LogsSquidTmp',
            fields=[
                ('parameter_search', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='analysis_squid_kerio.searchparametersquid')),
                ('log_squid', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='analysis_squid_kerio.logssquid')),
            ],
        ),
    ]
