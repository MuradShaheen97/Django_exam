from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'htmls/index.html')




def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash,
            birthday=request.POST['birthday']
        )
        request.session['user_id'] = user.id
        messages.success(request, "Successfully registered")
        return redirect('/success')
    return redirect('/')
def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')
        users = User.objects.filter(email=request.POST['email'])
        if not users:
            messages.error(request, "Invalid email or password")
            return redirect('/')
        user = users[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            messages.success(request, "Successfully logged in")
            return redirect('/success')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/')
    return redirect('/')
def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must login first")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)
def logout(request):
    request.session.clear()
    return redirect('/')
def index(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, "htmls/user.html", context)
def create_game(request):
    game_name=request.POST["game_name"]
    
    genre=request.POST["genre"]
    release_date=request.POST["release_date"]
    
    description=request.POST["description"]
    create_games(game_name,genre,release_date,description,)
    return redirect("/user.html/")

def user_view(request):
    # Your view logic here
    return render(request,"htmls/user.html")
