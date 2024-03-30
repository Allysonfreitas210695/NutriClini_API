from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Nutritionist

class NutritionistAdmin(admin.ModelAdmin):
    list_display = ['id','fullName', 'cpf', 'email', 'phone']
    search_fields = ['fullName', 'cpf', 'email', 'phone']

admin.site.register(Nutritionist, NutritionistAdmin)