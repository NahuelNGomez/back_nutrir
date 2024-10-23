from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('(?P<id_p>.+)/departamentos/(?P<id_d>.+)/gobiernos_locales/(?P<id_gl>.+)/localidades/$', views.Localidad_ID_GLDeptoProvinciaview.as_view(), name='LocalidadGobernoLocaldepartamentoProvincia')
]
