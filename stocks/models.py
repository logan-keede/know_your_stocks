from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.
class User(AbstractUser):
    """ 
    Student_ID is self Generating from the given email 
    """

    # email = models.EmailField(("email address"), unique=True)
    # REQUIRED_FIELDS = []
    objects = UserManager()
    dhan_access = models.CharField(max_length=300, blank=True)
    dhan_client = models.CharField(max_length=300, blank=True)