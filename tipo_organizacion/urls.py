from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.TipoOrganizacionViewList.as_view(), name="tipo_organizacion"),

]