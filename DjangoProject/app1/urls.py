from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Authentication
    # ==========================
    path('', views.index, name='index'),

    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),


    # ==========================
    # Dashboard
    # ==========================
    path('dashboard', views.dashboard, name='dashboard'),


    # ==========================
    # Games CRUD
    # ==========================
    path('games/create', views.create_game, name='create_game'),

    path('game/<int:id>', views.game_info, name='game_info'),

    path('edit/game/<int:id>', views.edit_game, name='edit_game'),

    path('update/game/<int:id>', views.update_game, name='update_game'),

    path('delete/game/<int:id>', views.delete_game, name='delete_game'),


    # ==========================
    # Favorite & Rating
    # ==========================
    path('game/<int:id>/fav', views.add_favorite, name='add_favorite'),

    path('game/<int:id>/unfav', views.remove_favorite, name='remove_favorite'),

    path('game/<int:id>/rate', views.rate_game, name='rate_game'),


    # ==========================
    # User Profile
    # ==========================
    path('profile/<int:id>', views.profile, name='profile'),

]