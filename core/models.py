
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
import datetime
from datetime import datetime, timedelta
# Create your models here.



class AddressBook(models.Model):
	phone = PhoneNumberField(blank=True, help_text='Contact phone number',null=True)

	street = models.CharField(max_length=64,blank=False)
	alt_line = models.CharField(max_length=64, blank=True)
	postcode= models.CharField(max_length=5,
	  validators=[RegexValidator('^[0-9]{5}$', _('Invalid postal code'))],
    blank=False)
	city = models.CharField(max_length=64, blank=False)
	state = models.CharField(max_length=64,blank=True)
	country = models.CharField(max_length=64, default="Suomi")
	#user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="address_book_user")

	class Meta:
		abstract = True

	def __str__(self):
		return self.city


class CustomUserManager(BaseUserManager):
	"""
	Custom user model manager where email is the unique identifiers
	for authentication instead of usernames.
	"""

	def create_user(self, email, password, last_login=datetime.now(),date_joined=datetime.now(), **extra_fields):
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


	def create_superuser(self, email, password, last_login=datetime.now(),date_joined=datetime.now(),**extra_fields):
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

	def has_perm(self, perm, obj=None):
		return self.is_staff


class Nurse(CustomUser,AddressBook):

	ROLES= (
		('Sh', 'RN'),
		('Lh', 'PN'),
		('HA', 'AS'), 

	)
	EXPERIENCES= (
		(0, '<5'),
		(1, '<10'),
		(2, '>=10'), 

	)
	bank_account_name=models.CharField(max_length=30, blank=True, null=True)
	bank_account_number=models.CharField(max_length=20, blank=True, null=True)
	role = models.CharField(max_length=2, choices=ROLES,blank=False)
	experience=models.IntegerField(choices=EXPERIENCES,blank=False)
	is_rn= models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Nurse'


class Employer(CustomUser,AddressBook):
	
	org_name=models.CharField(max_length=64)
	bank_account_name=models.CharField(max_length=30, blank=True, null=True)
	bank_account_number=models.CharField(max_length=20, blank=True, null=True)

	class Meta:
		verbose_name = 'Employer'
	



#class Shift()

