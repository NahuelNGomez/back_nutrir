from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.ServicioComedorViewList.as_view(), name="servicio_comedor"),

]