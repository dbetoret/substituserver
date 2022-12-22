from django.contrib import admin

# Register your models here.

from .models import Centre
admin.site.register(Centre)
from .models import Usuari
admin.site.register(Usuari)
from .models import Espai
admin.site.register(Espai)
from .models import Grup
admin.site.register(Grup)
from .models import Materia
admin.site.register(Materia)
from .models import Franja_horaria
admin.site.register(Franja_horaria)
from .models import Horari
admin.site.register(Horari)
from .models import Absencia
admin.site.register(Absencia)
from .models import Guardia
admin.site.register(Guardia)

