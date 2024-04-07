from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Food, Meal, MealPlan, Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id','fullName', 'cpf', 'email', 'phone']
    search_fields = ['fullName', 'cpf', 'email', 'phone']

admin.site.register(Patient, PatientAdmin)

class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'descricao', 'observation', 'status']
    search_fields = ['name', 'descricao', 'status']

admin.site.register(MealPlan, MealPlanAdmin)

class MealAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'time', 'observation']
    search_fields = ['name', 'time']

admin.site.register(Meal, MealAdmin)

class FoodAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'measure', 'quantity']
    search_fields = ['name', 'measure', 'quantity']

admin.site.register(Food, FoodAdmin)