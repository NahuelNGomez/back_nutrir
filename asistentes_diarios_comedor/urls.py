from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.AsistentesDiariosComedorViewList.as_view(), name="asistentes_diarios_comedor"),

]