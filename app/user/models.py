from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Concat
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Value


class User(AbstractUser):
    CUSTOMER = 'CR'
    EMPLOYEE = 'EM'
    USER_TYPE = {
        CUSTOMER: 'Customer',
        EMPLOYEE: 'Employee',
    }
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    surname = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    type = models.CharField(max_length=2, choices=USER_TYPE, default=EMPLOYEE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'surname', 'phone', 'username']
