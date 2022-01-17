from django.contrib import admin

# Register your models here.
from .models import LogsSquid
from .models import LogsKerio
from .models import Entity
from .models import User
from .models import BlackListDomain
from .models import SliceTmp , CategoryBlackListDomain, LogsSquidTmp

admin.site.register(LogsSquid)
admin.site.register(LogsSquidTmp)
admin.site.register(LogsKerio)
admin.site.register(Entity)
admin.site.register(User)
admin.site.register(BlackListDomain)
admin.site.register(SliceTmp)
admin.site.register(CategoryBlackListDomain)