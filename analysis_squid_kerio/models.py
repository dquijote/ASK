from django.db import models

# Create your models here.


class LogsKerio(models.Model):
    ip_addres = models.GenericIPAddressField("IP")
    user_name = models.CharField("Usuario", max_length=200)
    date_time = models.DateTimeField("Fecha")
    time_zone = models.CharField("Zona horario", max_length=100)
    http_method = models.CharField("Metodo http", max_length=50)
    url = models.CharField("Url", max_length=10000)
    version_http = models.CharField("Version de http", max_length=50)
    code_http = models.CharField("Codigo http", max_length=200)
    size_transfered = models.IntegerField("Tamanno de transf")
    count_requests_transferred = models.CharField("Cant de transferencia", max_length=1000)


class LogsSquid(models.Model):
    time_stamp = models.CharField("Time Stamp", max_length=100, default=1627704012)
    date_time = models.DateTimeField("Fecha")
    time_request = models.IntegerField("Duracion de consulta")
    ip_client = models.GenericIPAddressField("Ip cliente")
    cache_result_code = models.CharField("Codigo de cache", max_length=50)
    size_transfered = models.IntegerField("Tamanno de transf")
    http_method = models.CharField("Metodo http", max_length=50)
    url = models.CharField("Url", max_length=10000)
    user_name = models.CharField("Usuario", max_length=200)
    request_server_name = models.CharField("Nombre servidor", max_length=200)
    content_type = models.CharField("Tipo de contenido", max_length=100)


class CategoryBlackListDomain(models.Model):
    name = models.CharField("Categoria", max_length=100)

    def __str__(self):
        return self.name.upper()


# The parameter of search in logs squid
class SearchParameterSquid(models.Model):
    step_slice = models.IntegerField("Paso Slice")
    start_slice = models.IntegerField("Inicio Slice")
    end_slice = models.IntegerField("Fin Slice")
    multiplier_slice = models.IntegerField("Multiplicador Slice")
    category_black_list = models.ForeignKey(
        CategoryBlackListDomain,
        on_delete=models.CASCADE,
        default=None
    )
    date_start = models.DateField("Fecha Inicial")
    date_end = models.DateField("Fecha Final")
    user = models.CharField("Usuario", max_length=50, default=None, blank=True)


# Store the search made in logsSquid
class LogsSquidTmp(models.Model):
    parameter_search = models.OneToOneField(
        SearchParameterSquid,
        on_delete=models.CASCADE,
        primary_key=True,
        default=None
    )
    log_squid = models.ForeignKey(
        LogsSquid,
        on_delete=models.CASCADE,
        default=None
    )


class BlackListDomain(models.Model):
    fecha_entrada = models.DateTimeField("Fecha entrada")
    domain = models.CharField("Dominio", max_length=1000)
    category = models.ForeignKey(CategoryBlackListDomain, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category) + ": " + self.domain


class Entity(models.Model):
    name = models.CharField("Nombre", max_length=200)

    ueb = "UEB"
    dir = "Dir"


    classificationEntity = [
        (ueb, "UEB"),
        (dir, "Direccion")
    ]
    typeEntity = models.CharField("Clasificacion", max_length=10, choices=classificationEntity, default=ueb)

    def __str__(self):
        return self.typeEntity + " - " + self.name


class User(models.Model):
    cell = models.IntegerField(unique=True)
    name = models.CharField("Nombre", max_length=200)
    lastName1 = models.CharField("Primer Apellido", max_length=200)
    lastName2 = models.CharField("Segundo Apellido", max_length=200)
    mail = models.EmailField(primary_key=True)
    planeData = models.IntegerField("Plan de Datos (MB)")  # en mb

    nacional = 'nacional'
    internacional = 'internacional'
    correo = 'correo'

    defaultSocial = 'Ninguno'

    serviceNavcell = [
        (internacional, 'Internancional'),
        (correo, 'correo')
    ]
    serviceMail = [
        (nacional, 'Nacional'),
        (internacional, 'Internancional'),
    ]
    serviceNavPc = [
        (nacional, 'Nacional'),
        (internacional, 'Internancional'),
    ]

    # service_Type_Mail = [('Nacional', 'Nacional'), ('Internancional', 'Internancional')]
    # service_Type_Nav_PC = [('Nacional', 'Nacional'), ('Internancional', 'Internancional')]
    # service_Type_Nav_Cell = [('Correo', 'Correo'), ('Internancional', 'Internancional')]

    serviceTypeMail = models.CharField("Tipo de servicio Mail", choices=serviceMail, max_length=15, default=nacional)
    serviceTypeNavPC = models.CharField("Tipo de servicio Nav PC", choices=serviceNavPc, max_length=15, default=nacional)
    serviceTypeNavCell = models.CharField("Tipo de servicio Nav Cell", choices=serviceNavcell, max_length=15, default=internacional)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    # socialNetwork = models.CharField("Red social", max_length=2000, default=defaultSocial)
    root = models.BooleanField("Permiso Admin", default=False)
    quickAnswer = models.BooleanField("Grup. Respueta Rapida", default=False)

    def __str__(self):
        return self.name + " " + self.lastName1 + " " + self.lastName2


# Store the temp part from the slice
class SliceTmp(models.Model):
    start = models.IntegerField("Slice inicio")
    end = models.IntegerField("Slice fin")
    step = models.IntegerField("Slice paso")
    multiplier = models.IntegerField("Multiplicador ")

    def __str__(self):
        return "incio:" + str(self.start) + " - " + "fin:" + str(self.end) + "paso:" + str(self.step)


class SocialNetwork(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    id_social_network = models.CharField("Id Red Social", max_length=500)
    name = models.CharField("Nombre de red social", max_length=100)
    description = models.CharField("Descripcion", max_length=300)


