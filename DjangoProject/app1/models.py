from django.db import models
from django.core.validators import RegexValidator
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from datetime import date


# =========================
# User Manager
# =========================
class UserManager(models.Manager):

    def register_validator(self, post_data):
        errors = {}

        first_name = post_data.get("first_name", "").strip()
        last_name = post_data.get("last_name", "").strip()
        email = post_data.get("email", "").strip()
        dob = post_data.get("dob", "")
        password = post_data.get("password", "")
        confirm_password = post_data.get("confirm_password", "")

        if len(first_name) < 4:
            errors["first_name"] = "First name must be at least 4 characters."

        if len(last_name) < 4:
            errors["last_name"] = "Last name must be at least 4 characters."

        if not email:
            errors["email"] = "Email is required."

        elif User.objects.filter(email=email).exists():
            errors["email"] = "Email already exists."

        if not dob:
            errors["dob"] = "Date of birth is required."
        else:
            birth_date = date.fromisoformat(dob)
            today = date.today()
            age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )

            if age < 18:
                errors["dob"] = "User must be 18 years or older."

        if len(password) < 8:
            errors["password"] = "Password must be at least 8 characters."

        if password != confirm_password:
            errors["confirm_password"] = "Password and confirm password must match."

        return errors

    def login_validator(self, post_data):
        errors = {}

        email = post_data.get("login_email", "").strip()
        password = post_data.get("login_password", "")

        users = User.objects.filter(email=email)

        if not users:
            errors["login"] = "Invalid email or password."
        else:
            user = users.first()
            if not check_password(password, user.password):
                errors["login"] = "Invalid email or password."

        return errors

    def add_user(self, post_data):
        return User.objects.create(
        first_name=post_data["first_name"],
        last_name=post_data["last_name"],
        email=post_data["email"],
        dob=post_data["dob"],
        password=make_password(post_data["password"]),
        avatar=post_data.get("avatar")
    )

    def get_user(self, user_id):
        return User.objects.get(id=user_id)


# =========================
# Game Manager
# =========================
class GameManager(models.Manager):

    def game_validator(self, post_data):
        errors = {}

        name = post_data.get("name", "").strip()
        genre = post_data.get("genre", "").strip()
        release_date = post_data.get("release_date", "")
        description = post_data.get("description", "").strip()

        if len(name) < 2:
            errors["name"] = "Game name must be at least 2 characters."

        if not genre:
            errors["genre"] = "Genre is required."

        if not release_date:
            errors["release_date"] = "Release date is required."
        else:
            game_date = date.fromisoformat(release_date)
            if game_date > date.today():
                errors["release_date"] = "Release date cannot be in the future."

        if not description:
            errors["description"] = "Description is required."

        return errors

    def add_game(self, post_data, user_id):
        creator = User.objects.get(id=user_id)

        return Game.objects.create(
            name=post_data["name"],
            genre=post_data["genre"],
            release_date=post_data["release_date"],
            description=post_data["description"],
            created_by=creator
        )

    def update_game(self, game_id, post_data):
        game = Game.objects.get(id=game_id)

        game.name = post_data["name"]
        game.genre = post_data["genre"]
        game.release_date = post_data["release_date"]
        game.description = post_data["description"]
        game.save()

        return game

    def delete_game(self, game_id):
        game = Game.objects.get(id=game_id)
        game.delete()

    def get_game(self, game_id):
        return Game.objects.get(id=game_id)

    def all_games(self):
        return Game.objects.all()


# =========================
# Favorite / Rate Manager
# =========================
class FavoriteManager(models.Manager):

    def add_fav(self, user_id, game_id, rate):
        user = User.objects.get(id=user_id)
        game = Game.objects.get(id=game_id)

        fav = Favorite.objects.filter(user=user, game=game)

        if fav.exists():
            fav = fav.first()
            fav.rate = rate
            fav.save()
            return fav

        return Favorite.objects.create(
            user=user,
            game=game,
            rate=rate
        )

    def delete_fav(self, user_id, game_id):
        Favorite.objects.filter(
            user_id=user_id,
            game_id=game_id
        ).delete()

    def get_favorites_for_game(self, game_id):
        return Favorite.objects.filter(game_id=game_id)

    def get_favorites_for_user(self, user_id):
        return Favorite.objects.filter(user_id=user_id)


# =========================
# User Table
# =========================
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    avatar = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================
# Game Table
# =========================
class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.TextField()

    created_by = models.ForeignKey(
        User,
        related_name="games_created",
        on_delete=models.CASCADE
    )

    liked_by = models.ManyToManyField(
        User,
        through="Favorite",
        related_name="favorite_games"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GameManager()

    def __str__(self):
        return self.name


# =========================
# Favorite / Rate Table
# =========================
class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name="favorites",
        on_delete=models.CASCADE
    )

    game = models.ForeignKey(
        Game,
        related_name="favorites",
        on_delete=models.CASCADE
    )

    rate = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FavoriteManager()

    class Meta:
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user} likes {self.game} - Rate {self.rate}"