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
class ShiftsViewTests(TestCase):
    def setUp(self):
        # Create a test employer user
        self.employer_user = CustomUser.objects.create_user(
            email="test_employer@gmail.com", password="employerpassword", is_employer=True
        )
        self.employer = Employer.objects.create(id=self.employer_user.id)

        # Create a test nurse user
        self.nurse_user = CustomUser.objects.create_user(
            email="test_nurse@gmail.com", password="nursepassword", is_nurse=True
        )

        # Create a test admin user
        self.admin_user = CustomUser.objects.create_superuser(
            email="test_admin@gmail.com", password="adminpassword"
        )

        # Create some test shifts
        self.shift1 = Shift.objects.create(
            employer=self.employer,
            start_time="2022-01-01T12:00:00Z",
            end_time="2022-01-01T16:00:00Z",
            role="RN",
            status="PUBLISHED",
        )
        self.shift2 = Shift.objects.create(
            employer=self.employer,
            start_time="2022-01-01T12:00:00Z",
            end_time="2022-01-01T16:00:00Z",
            role="RN",
            status="UNPUBLISHED",
        )

    def test_employer_can_see_published_shifts(self):
        # Log in as the employer user
        self.client.login(email="test_employer@gmail.com", password="employerpassword")

        # Request the shifts page
        response = self.client.get(reverse("shifts"))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200, follow=True)

        # Check that the employer user can see the published shift
        self.assertContains(response, self.shift1.role)

        # Check that the employer user cannot see the unpublished shift
        self.assertNotContains(response, self.shift2.role)

    def test_nurse_can_see_published_shifts(self):
        # Log in as the nurse user
        self.client.login(email="test_nurse@gmail.com", password="nursepassword")

        # Request the shifts page
        response = self.client.get(reverse("shifts"))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200, follow=True)

        # Check that the nurse user can see the published shift
        self.assertContains(response, self.shift1.role)

        # Check that the nurse user cannot see the unpublished shift
        self.assertNotContains(response, self.shift2.role)

    def test_admin_can_see_all_shifts(self):
        # Log in as the admin user
        self.client.login(email="test_admin@gmail.com", password="adminpassword"