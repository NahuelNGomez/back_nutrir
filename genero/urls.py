from django.urls import path, include, re_path
from . import views

urlpatterns = [
     re_path('$', views.GeneroViewList.as_view(), name="generos"),

]