from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import *

#python3 manage.py test core

class TestUrls(SimpleTestCase):
	

	def test_index_url_resolves(self):
		url = reverse('index')
		print(resolve(url))
		self.assertEquals(resolve(url).func, index)

	def test_login_url_resolves(self):
		url = reverse('login')
		print(resolve(url))
		self.assertEquals(resolve(url).func, login_view)#view name

	def test_logout_url_resolves(self):
		url = reverse('logout')
		print(resolve(url))
		self.assertEquals(resolve(url).func, logout_view)

	def test_password_change_resolves(self):
		url = reverse('password_change')
		print(resolve(url))
		self.assertEquals(resolve(url).func, password_change)

	def test_password_reset_resolves(self):
		url = reverse('password_reset')
		print(resolve(url))
		self.assertEquals(resolve(url).func, password_reset_view)


	def test_password_reset_request_resolves(self):
		url = reverse('password_reset_request')
		print(resolve(url))
		self.assertEquals(resolve(url).func, password_reset_request)
    
	def test_passwordResetConfirm_resolves(self):
		url = reverse('password_reset_confirm',args=['<uidb64>','<token>']) 
		
		print(resolve(url))
		self.assertEquals(resolve(url).func, passwordResetConfirm)#view name
    
	def test_profile_resolves(self):
		url = reverse('profile',args=['<id>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, profile)


	def test_shifts_url_resolves(self):
		url = reverse('shifts')
		print(resolve(url))
		self.assertEquals(resolve(url).func, shifts)

	def test_create_shift_url_resolves(self):
		url = reverse('create_shift')
		print(resolve(url))
		self.assertEquals(resolve(url).func, createShift)

	def test_shift_detail_url_resolves(self):
		url = reverse('shift_detail',args=['<int:shift_id>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, shift_detail)

	def test_update_shift_url_resolves(self):
		url = reverse('update_shift',args=['<str:pk>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, updateShift)

	def test_delete_shift_url_resolves(self):
		url = reverse('delete_shift',args=['<str:pk>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, deleteShift)

	def test_reserve_shift_url_resolves(self):
		url = reverse('reserve_shift',args=['<str:pk>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, reserve_shift)

	def test_search_resolves(self):
		url = reverse('search')
		print(resolve(url))
		self.assertEquals(resolve(url).func, search)

	def test_reserved_shifts_url_resolves(self):
		url = reverse('reserved_shifts',args=['<id>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, reserved_shifts)

	def test_shifts_done_url_resolves(self):
		url = reverse('shifts_done',args=['<id>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, shifts_done)

	def test_nurse_url_resolves(self):
		url = reverse('nurse',args=['<id>'])
		print(resolve(url))
		self.assertEquals(resolve(url).func, nurse)

	def test_export_csv_resolves(self):
		url = reverse('export_csv')
		print(resolve(url))
		self.assertEquals(resolve(url).func,export_csv)

	def test_chart_resolves(self):
		url = reverse('chart')
		print(resolve(url))
		self.assertEquals(resolve(url).func,chart)


