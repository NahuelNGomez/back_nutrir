from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.ActividadComplementariaComedorViewList.as_view(), name="actividad_complementaria_comedor"),

]