
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    #def create_nurse...
    #def create_employer...

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=250, default="lala", blank=False)
	last_name = models.CharField(max_length=250, default="land", blank=False)
	email = models.EmailField(('email address'), unique=True)
	is_nurse = models.BooleanField(default=False)
	is_employer = models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(default=timezone.now)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()
	
	def __str__(self):
		return self.email


class AddressBook(models.Model):

    street = models.CharField(max_length=64)
    alt_line = models.CharField(max_length=64)
    postcode= models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="address_book_user")
    
    class Meta:
    	verbose_name = 'Address'
    

class Nurse(CustomUser):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="nurse_user")
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')

    ROLES= (
        ('Sh', 'Reigstered Nurse'),
        ('Lh', 'Practical Nurse'),
        ('HA', 'Assistant'), 

    )
    EXPERIENCES= (
        (0, 'Less than five years'),
        (1, 'Less than ten years'),
        (2, 'More than ten years'), 

    )
    role = models.CharField(max_length=2, choices=ROLES,blank=False)
    experience=models.IntegerField(choices=EXPERIENCES,blank=False)
    class Meta:
    	verbose_name = 'Nurse'


class Employer(CustomUser):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="employer_user")
	phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')
	org_name=models.CharField(max_length=64)

	class Meta:
		verbose_name = 'Employer'
	

