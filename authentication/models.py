from django.db import models
from wagtail.fields import RichTextField
# Create your models here.
from django.contrib.auth.models import AbstractUser
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class Gender(models.Model):
    type = models.CharField(max_length=500, null=True, blank= True)

    def __str__(self):
        return f'{self.type}'

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='First Name', max_length=255, null=True, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=255, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = RichTextField(null=True, blank=True)
    role = models.CharField(max_length=500, null=True, blank=True)
    company = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True, null=True)
    country = models.CharField(verbose_name='country', max_length=255, null=True, blank=True)
    region = models.CharField(verbose_name='region', max_length=255, null=True, blank=True)
    city = models.CharField(verbose_name='country', max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.email}'