from django.urls import path
from . import views

# REQUIRED configuration token mapping for isolating multi-app namespace environments
app_name = 'app1'  

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('user/', views.user_view, name='user'),
    path('user', views.user_view, name='user'),
    path('create_game', views.create_game, name='create_game'),
]
