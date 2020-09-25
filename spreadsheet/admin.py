from django.contrib import admin
from .models import DaneArkusza
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls import include, url
from django.http import HttpResponse, HttpResponseRedirect



@staff_member_required
def getData(request):
    print("\nFUNKCJA DZIAŁA\n")
    DaneArkusza.getDataFromSheet()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

class AdmSite(admin.ModelAdmin):

    def get_urls(self):
        urls = super(AdmSite, self).get_urls()
        my_urls = [
            url(r"^getData/$", getData)
        ]
        return my_urls + urls
    list_display = ['Imie', 'Nazwisko', 'Email', 'Numer_telefonu', 'Adres']
    change_list_template = "admin/changelist.html"

admin.site.register(DaneArkusza, AdmSite)

"""
class AdmSite(admin.ModelAdmin):
    list_display = ['Imie', 'Nazwisko', 'Email', 'Numer_telefonu', 'Adres']
    change_list_template = "admin/changelist.html"

admin.site.register(DaneArkusza, AdmSite)
"""