from django.contrib import admin
from .models import DaneArkusza
    
class AdmSite(admin.ModelAdmin):
    list_display = ['Imie', 'Nazwisko', 'Email', 'Numer_telefonu', 'Adres']

admin.site.register(DaneArkusza, AdmSite)