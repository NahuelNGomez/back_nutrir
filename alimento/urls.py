from django.urls import path, re_path
from . import views
from .views import AlimentoSARAAutoComplete

urlpatterns = [
    path('', views.AlimentoViewList.as_view(), name="alimento"),  # Captura solo la raíz
    path('get_alimento_sara/<int:alimento_id>/', views.get_alimento_sara, name='get_alimento_sara'), 
    path('alimento_sara/autocomplete/', AlimentoSARAAutoComplete.as_view(), name='alimento_sara_autocomplete'),
    re_path('$', views.UnidadesViewList.as_view(), name="unidad"),# Nueva ruta para obtener el alimento de SARA
]