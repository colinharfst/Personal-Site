from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('judge/', views.judge, name='judge'),
    path('chess/', views.chess, name='chess'),
    path('math/', views.math, name='math'),
]