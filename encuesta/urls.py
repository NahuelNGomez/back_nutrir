from django.urls import path, include, re_path
from . import views

#Ver si es asi por parte o todo junto el json

#r^(?P<date>\d{4}-\d{2}-\d{2})
urlpatterns = [
    #re_path(r'^incompletas/(?P<id_c>.+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.EncuestasAdeudadasViewList.as_view(), name='encuestas_incompletas'),  # Endpoint para ver una encuesta
    #re_path('incompletas/(?P<id_c>.+)/$', views.EncuestasAdeudadasViewList.as_view(), name='encuestas_incompletas'),  # Endpoint para ver una encuesta
	re_path('no_se_sirvio/$', views.NoSeSirvioEncuestasView.as_view(), name='encuesta-no-se-sirvio'),  # Endpoint para definir que una comida no se sirvio
    re_path(r'^incompletas_dia/(?P<id_c>.+)/(?P<fecha>\d{4}-\d{2}-\d{2})/$', views.EncuestasAdeudadasDiaViewList.as_view(), name='encuestas_incompletas'),  # Endpoint para ver una encuesta           ),
    re_path(r'^incompletas/(?P<id_c>.+)/(?P<fecha>\d{4}-\d{2}-\d{2})/$', views.EncuestasAdeudadasViewList.as_view(), name='encuestas_incompletas'),  # Endpoint para ver una encuesta           ),
#    re_path('(?P<id_e>.+)/comidas/$', views.ComidaEncuestaViewList.as_view(), name='encuesta-comida'),  # Endpoint para obtener las comidas de una encuesta
    #re_path('comidas_encuesta/(?P<id_ce>.+)/alimentos/$', views.AlimentoComidaEncuestaViewList.as_view(), name='encuesta-comida-alimento'), #Endpoint para obtener los alimentos de una comida de una encuesta
    re_path('(?P<id_e>.+)/$', views.EncuestaViewList.as_view(), name='encuesta'),  # Endpoint para ver una encuesta
    re_path('$', views.EncuestasViewList.as_view(), name='encuestas'),   # Endpoint para obtener todas las encuestas y agregar una
]
