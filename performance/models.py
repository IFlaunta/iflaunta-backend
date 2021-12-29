from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password, **extra_fields
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password, **extra_fields
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None     # https://docs.djangoproject.com/en/3.2/topics/db/models/#field-name-hiding-is-not-permitted
    user_id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    save_video = models.BooleanField(default=False)

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
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    keywords = models.TextField()   # Comma Separated words
    question_grade = models.CharField(max_length=50, default="0")   # Any weightage
    tags = models.TextField()   # Comma Separated words

class Performance(models.Model):
    user = models.ForeignKey(User, related_name="userPerformance", on_delete=models.CASCADE)
    performance_id = models.BigAutoField(primary_key=True, editable=False)
    question = models.ForeignKey(Question, related_name="performanceQuestion", on_delete=models.SET_NULL, null=True)
    concentration = models.IntegerField(default=0)
    eyecontact = models.IntegerField(default=0)
    clarity = models.IntegerField(default=0)
    understanding = models.IntegerField(default=0)
    confidence = models.IntegerField(default=0)
    performance_datetime = models.DateTimeField(auto_now_add=True)
    '''
    Rest Factors will be added later...
    '''

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.performance.user.user_id, filename)

class PerformanceVideo(models.Model):
    video_id = models.BigAutoField(primary_key=True, editable=False)
    performance = models.OneToOneField(Performance, related_name="performanceVideo", on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)      # Storing files to folder with name as user_id