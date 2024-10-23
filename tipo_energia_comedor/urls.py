from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.TipoEnergiaComedorViewList.as_view(), name="tipo_energia_comedor"),

]