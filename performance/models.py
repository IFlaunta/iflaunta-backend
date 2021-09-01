from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):
    username = None     # https://docs.djangoproject.com/en/3.2/topics/db/models/#field-name-hiding-is-not-permitted
    user_id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

class Question(models.Model):
    question_id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.TextField()   # Comma Separated words
    question_grade = models.CharField(max_length=50, default="0")   # Any weightage
    tags = models.TextField()   # Comma Separated words
