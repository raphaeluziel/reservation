from django.test import TestCase, Client
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from core.models import *
from django.urls import reverse
from django import forms

from core.views import *
#import forms,CustomUserCreationForm,LoginForm,PasswordResetForm,UserUpdateForm,UpdateShiftForm,CreateShiftForm,ReserveShiftForm

from django.contrib.auth.forms import SetPasswordForm
class BaseTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = CustomUser.objects.create_user(email="test_admin@gmail.com", password="adminpassword", is_staff=True)
        self.employer_user = CustomUser.objects.create_user(email="test_employer@gmail.com", password="employerpassword", is_employer=True)
        self.nurse_user = CustomUser.objects.create_user(email="test_nurse@gmail.com",password="nursepassword", is_nurse=True)


class LoginViewTests(BaseTestCase):

    def test_admin_user(self):
        # Create a client and log in the admin user
        client = Client()
        client.force_login(self.admin_user)

        # Verify that the user is authenticated
        assert self.admin_user.is_authenticated

        # Run the view and verify that it returns a 200 OK response
        response = client.get(reverse('login'))
        assert response.status_code == 200
        self.assertTemplateUsed(response,'login.html')

    def test_employer_user(self):
       # Create a client and log in the employer user
       client = Client()
       client.force_login(self.employer_user)

        # Verify that the user is authenticated
       assert self.employer_user.is_authenticated

       # Run the view and verify that it returns a 200 OK response
       response = client.get(reverse('login'))
       assert response.status_code == 200
       self.assertTemplateUsed(response,'login.html')


    def test_nurse_user(self):
        # Create a client and log in the nurse user
        client = Client()
        client.force_login(self.nurse_user)

        # Verify that the user is authenticated
        assert self.nurse_user.is_authenticated

        # Run the view and verify that it returns a 200 OK response
        response = client.get(reverse('login'))
        assert response.status_code == 200
        self.assertTemplateUsed(response,'login.html')



"""

class Default_Password_Detect_Tests(BaseTestCase):

    def test_login_view(self):
        # Create a client
        client = Client()

        # Test login with default password
        response = self.client.post(reverse("login"), {"email": "test_user@gmail.com", "password": "Monday_123"}, follow=True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('password_change'))


        # Test login with non-default password
        response = client.post(reverse("login"), {"email": "test_user@gmail.com", "password": "adminpassword"}, follow=True)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "shifts.html" )

        # Test login with invalid credentials
        response = client.post(reverse("login"), {"email": "test_user@gmail.com", "password": "invalid"}, follow=True)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "login.html")

"""
from django.test import TestCase, Client
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from core.models import *
from django.urls import reverse
from django import forms

from core.views import *
#import forms,CustomUserCreationForm,LoginForm,PasswordResetForm,UserUpdateForm,UpdateShiftForm,CreateShiftForm,ReserveShiftForm

from django.contrib.auth.forms import SetPasswordForm

class ShiftsViewTests(TestCase):
    def test_shifts_view(self):
        # Create a test user
        newuser = CustomUser.objects.create_user(
            email="testnewuser@gmail.com", password="testpassword", is_employer=True
        )

        # Create an employer instance for the test user
        employer = Employer.objects.create(id=newuser.id)

        # Create some test shifts
        shift1 = Shift.objects.create(
            employer=employer,
            start_time="2022-01-01T08:00:00",
            finish_time="2022-01-01T16:00:00",
            role="RN",
            status="PUBLISHED",
        )
        shift2 = Shift.objects.create(
            employer=employer,
            start_time="2022-01-02T08:00:00",
            finish_time="2022-01-02T16:00:00",
            role="RN",
            status="PUBLISHED",
        )
        shift3 = Shift.objects.create(
            employer=employer,
            start_time="2022-01-03T08:00:00",
            finish_time="2022-01-03T16:00:00",
            role="RN",
            status="PUBLISHED",
        )

        # Create a client
        client = Client()

        # Log in the test user
        client.login(email="testnewuser@gmail.com", password="testpassword")

        # Send a GET request to the shifts view
        response = client.get(reverse("shifts"), follow=True)

        
        # Print the response and the resolved URL
        print("Response:", response)
        print("Resolved URL:", reverse("shifts"))

        # Assert that the response is a redirect to the shifts view
        self.assertRedirects(response, reverse("shifts"))



