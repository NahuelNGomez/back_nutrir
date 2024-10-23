from django.urls import path, include, re_path
from . import views

urlpatterns = [
	re_path('servicio/(?P<servicio>[^/]+)/$', views.ComidaServicioView.as_view(), name='comida-servicio'),
	re_path('(?P<id_c>.+)/$', views.ComidaAlimentoView.as_view(), name='comida-alimento'),  # Endpoint para ver la informacion de una comida y la de sus alimentos
	re_path('$', views.ComidaViewList.as_view(), name="comida"),
]
