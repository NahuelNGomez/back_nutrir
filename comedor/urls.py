from django.urls import path, include, re_path
from . import views
from .views import ProvinciaAutoComplete,DepartamentoAutoComplete, GobiernoLocalAutoComplete,LocalidadAutoComplete

urlpatterns = [
    re_path('responsable/$', views.ComedorUsuarioViewList.as_view(), name='comedor-usuario'), # Endpoint para obtener los comedores de un responsable
    re_path('provincia/autocomplete', ProvinciaAutoComplete.as_view() , name="provincia-autocomplete"),
    re_path('departamento/autocomplete', DepartamentoAutoComplete.as_view() ,name="departamento-autocomplete"),
    re_path('gobiernoLocal/autocomplete', GobiernoLocalAutoComplete.as_view() , name="gobiernoLocal-autocomplete"),
    re_path('localidad/autocomplete', LocalidadAutoComplete.as_view() ,name="localidad-autocomplete"),
	re_path('funcionamiento/$', views.FuncionamientoPostViewList.as_view(), name='comedor-funcionamiento-post'),
    re_path('(?P<id>.+)/funcionamiento/$', views.FuncionamientoComedorViewList.as_view(), name='comedor-funcionamiento'),  # Endpoint para obtener el funcionamiento de un comedor
    re_path('(?P<id>.+)/$', views.ComedorViewList.as_view(), name='comedor'),  # Endpoint para obtener un comedor
    re_path('$', views.ComedoresViewList.as_view(), name='comedores'),   # Endpoint para obtener todos los comedores
]
