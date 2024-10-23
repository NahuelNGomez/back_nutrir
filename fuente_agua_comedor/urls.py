from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.FuenteAguaComedorViewList.as_view(), name="fuente_agua_comedor"),

]