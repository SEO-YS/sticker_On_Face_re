from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from datos.views import base_views as dv

app_name = 'stickers'

urlpatterns = [
    path('bat/',views.bat , name='bat'),

    # path('seoul_pop/', views.seoul_pop, name='seoul_pop'),
]