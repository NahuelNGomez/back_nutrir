from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.ProvinciaViewList.as_view()),
]
