from django.urls import path, include, re_path
from . import views

urlpatterns = [
      re_path('(?P<id>.+)/departamentos/$', views.DepartamentoIDProvinciaview.as_view(), name='departamentoProvincia') #Ver todos los departamentos segun 1 provincia
]
