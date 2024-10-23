from django.urls import path, include, re_path
from .views import RacionesMesViewList, RacionesSemanaViewList, ComidasMesViewList, ComidasSemanaViewList

urlpatterns = [
	re_path('racion_mes/(?P<comedor>.+)/$', RacionesMesViewList.as_view(), name='racion-mes'),
	re_path('racion_semana/(?P<comedor>.+)/$', RacionesSemanaViewList.as_view(), name='racion-semana'),
	re_path('comida_mes/(?P<comedor>.+)/$', ComidasMesViewList.as_view(), name='comida-mes'),
	re_path('comida_semana/(?P<comedor>.+)/$', ComidasSemanaViewList.as_view(), name='comida-semana'),
]
