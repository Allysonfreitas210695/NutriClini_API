
# Register your models here.
from django.contrib import admin
from .models import CodigoReset

class CodigoAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'codigo']


admin.site.register(CodigoReset, CodigoAdmin)
