"""django_nutrir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dj_rest_auth.views import PasswordChangeView
from django.contrib import admin
from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from django.conf.urls.static import static

#from django.conf.urls.defaults import *




urlpatterns = [
    #path(r'^admin/reporte/$', 'django_nutrir.admin_views.reporte'),
    path('admin/', admin.site.urls),
    path('provincia/', include('provincia.urls')),
    path('departamento/', include('departamento.urls')),
    path('gobierno_local/', include('gobierno_local.urls')),
    path('localidad/', include('localidad.urls')),
    path('actividad_complementaria_comedor/', include('actividad_complementaria_comedor.urls')),
    path('asistentes_diarios_comedor/', include('asistentes_diarios_comedor.urls')),
    path('cantidad_trabajadores_comedor/', include('cantidad_trabajadores_comedor.urls')),
    path('comedor/', include('comedor.urls')),
    path('fuente_agua_comedor/', include('fuente_agua_comedor.urls')),
    path('genero/', include('genero.urls')),
    path('organizacion/', include('organizacion.urls')),
    path('responsable_organizacion/', include('responsable_organizacion.urls')),
    path('servicio_comedor/', include('servicio_comedor.urls')),
    path('tipo_energia_comedor/', include('tipo_energia_comedor.urls')),
    path('tipo_organizacion/', include('tipo_organizacion.urls')),
    path('alimento/', include('alimento.urls')),
    path('comida/', include('comida.urls')),
    path('encuesta/', include('encuesta.urls')),
	path('reporte/', include('reporte.urls')),
    #LOGIN USUARIO
    path('user/', include('allauth.urls')),
    path('user/sesion/', include('dj_rest_auth.urls')), #Login, logout
	path(
	  'user/password_reset/',
	  PasswordResetView.as_view(),
	  name='password_reset',
	),
	path(
	  'user/password_reset_confirm/<uidb64>/<token>/',
	  PasswordResetConfirmView.as_view(),
	  name='password_reset_confirm',
	),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)


#admin.autodiscover()
#admin.site.enable_nav_sidebar = False
