from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('(?P<id_p>.+)/departamentos/(?P<id_d>.+)/gobiernos_locales/$', views.GobiernoLocalIDDeptoProvinciaview.as_view(), name='GobernoLocaldepartamentoProvincia') #Ver todos los departamentos segun 1 provincia
]

