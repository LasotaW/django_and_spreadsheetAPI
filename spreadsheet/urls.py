from django.urls import path
from spreadsheet import views

app_name = 'spreadsheet'
urlpatterns = [
    path('', views.index, name='index'),
]
