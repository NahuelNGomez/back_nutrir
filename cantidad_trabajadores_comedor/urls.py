from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.CantidadTrabajadoresComedorViewList.as_view(), name="cantidad_trabajadores_comedor"),

]