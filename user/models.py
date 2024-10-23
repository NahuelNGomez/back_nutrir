from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from genero.models import Genero
from django_nutrir.validaciones import validar_cuil

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, genero=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, genero=genero, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            genero=None,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.admin = True
        user.save()
        return user

class UsuarioPersonalizado(AbstractUser, PermissionsMixin):

    # Campos personalizados
    cuil = models.CharField(max_length=40, unique=True, validators=[validar_cuil])
    cambio_contrasenia = models.BooleanField(default=False, editable=True)
    genero = models.ForeignKey(Genero, models.CASCADE, null=True)
    picture = models.ImageField()
    email = models.EmailField('Email', unique=True)
    telefono = models.CharField('Telefono', max_length=50)

    USERNAME_FIELD = 'email'
    username = None
    objects = UserManager()
    REQUIRED_FIELDS = ['cuil', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email}"