from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.ResponsableOrganizacionViewList.as_view(), name="responsables_organizacion"),

]