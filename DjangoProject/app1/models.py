from django.db import models
import re
from datetime import date


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        first_name = postData.get('first_name')
        last_name = postData.get('last_name')
        email = postData.get('email')
        password = postData.get('password')
        confirm_password = postData.get('confirm_password')
        birthday = postData.get('birthday')
        name_regex = re.compile(r'^[A-Za-z]+$')
        email_regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        if len(first_name) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if not name_regex.match(first_name):
            errors['first_name_letters'] = "First name must contain letters only"
        if len(last_name) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not name_regex.match(last_name):
            errors['last_name_letters'] = "Last name must contain letters only"
        if not email_regex.match(email):
            errors['email'] = "Email must be valid"
        if User.objects.filter(email=email).exists():
            errors['email_exists'] = "Email already exists"
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if password != confirm_password:
            errors['confirm_password'] = "Password and confirm password must match"
        if birthday:
            birth_date = date.fromisoformat(birthday)
            if birth_date >= date.today():
                errors['birthday_past'] = "Birthday must be in the past"
            age = date.today().year - birth_date.year
            if (date.today().month, date.today().day) < (birth_date.month, birth_date.day):
                age -= 1
            if age < 13:
                errors['age'] = "User must be at least 13 years old"
        return errors
    def login_validator(self, postData):
        errors = {}
        email = postData.get('email')
        password = postData.get('password')
        if len(email) == 0:
            errors['email'] = "Email is required"
        if len(password) == 0:
            errors['password'] = "Password is required"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class User(models.Model):
    game_name = models.CharField(max_length=45)
    genre = models.CharField(max_length=100)
    release_date=models.IntegerField()
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
def create_games(game_name,genre,release_date,description):
    User.objects.create(
        game_name=game_name,
        genre=genre,
        release_date=release_date,
        description=description,
    )