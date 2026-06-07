from django.urls import path
from . import views

# REQUIRED configuration token mapping for isolating multi-app namespace environments
app_name = 'app1'  

urlpatterns = [
    path('', views.index, name='index'),
]