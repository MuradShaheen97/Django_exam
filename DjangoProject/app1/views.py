from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User, Game, Favorite


# ==========================
# Home Page
# ==========================
def index(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')

    return render(request, 'htmls/index.html')


# ==========================
# Register
# ==========================
def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)

        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')

        user = User.objects.add_user(request.POST)

        request.session['user_id'] = user.id
        request.session['user_name'] = f"{user.first_name} {user.last_name}"

        return redirect('/dashboard')

    return redirect('/')


# ==========================
# Login
# ==========================
def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)

        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')

        user = User.objects.get(email=request.POST['login_email'])

        request.session['user_id'] = user.id
        request.session['user_name'] = f"{user.first_name} {user.last_name}"

        return redirect('/dashboard')

    return redirect('/')


# ==========================
# Logout
# ==========================
def logout(request):
    request.session.flush()
    return redirect('/')


# ==========================
# Dashboard
# ==========================
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'games': Game.objects.all_games()
    }

    return render(request, 'htmls/dashboard.html', context)


# ==========================
# Create Game
# ==========================
def create_game(request):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == "POST":
        errors = Game.objects.game_validator(request.POST)

        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/dashboard')

        Game.objects.add_game(request.POST, request.session['user_id'])

    return redirect('/dashboard')


# ==========================
# Game Info Page
# ==========================
def game_info(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'game': Game.objects.get_game(id)
    }

    return render(request, 'htmls/game_info.html', context)


# ==========================
# Edit Game Page
# ==========================
def edit_game(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    game = Game.objects.get_game(id)

    if game.created_by.id != request.session['user_id']:
        return redirect('/dashboard')

    context = {
        'game': game
    }

    return render(request, 'htmls/edit_game.html', context)


# ==========================
# Update Game
# ==========================
def update_game(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    game = Game.objects.get_game(id)

    if game.created_by.id != request.session['user_id']:
        return redirect('/dashboard')

    if request.method == "POST":
        errors = Game.objects.game_validator(request.POST)

        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect(f'/edit/game/{id}')

        Game.objects.update_game(id, request.POST)

    return redirect(f'/game/{id}')


# ==========================
# Delete Game
# ==========================
def delete_game(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    game = Game.objects.get_game(id)

    if game.created_by.id == request.session['user_id']:
        Game.objects.delete_game(id)

    return redirect('/dashboard')


# ==========================
# Add Favorite
# ==========================
def add_favorite(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    game = Game.objects.get_game(id)

    if game.created_by.id == request.session['user_id']:
        return redirect(f'/game/{id}')

    rate = request.POST.get('rate', 1)

    Favorite.objects.add_fav(
        request.session['user_id'],
        id,
        rate
    )

    return redirect(f'/game/{id}')


# ==========================
# Rate Game
# ==========================
def rate_game(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    game = Game.objects.get_game(id)

    if game.created_by.id == request.session['user_id']:
        return redirect(f'/game/{id}')

    rate = request.POST.get('rate')

    if rate:
        Favorite.objects.add_fav(
            request.session['user_id'],
            id,
            rate
        )

    return redirect(f'/game/{id}')


# ==========================
# Remove Favorite
# ==========================
def remove_favorite(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    Favorite.objects.delete_fav(
        request.session['user_id'],
        id
    )

    return redirect(f'/game/{id}')


# ==========================
# Profile Page
# ==========================
def profile(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get_user(id),
        'favorites': Favorite.objects.get_favorites_for_user(id)
    }

    return render(request, 'htmls/profile.html', context)