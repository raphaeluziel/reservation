from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

#from .forms import CustomUserCreationForm, CustomUserChangeForm


from .models import CustomUser,Nurse, Employer,AddressBook,Shift

import datetime
from datetime import datetime, timedelta



class CustomUserCreationForm(forms.ModelForm):

    """A form for creating new users. Includes all the required
    fields, plus a repeated password.

    Note: at the moment, this form is only meant for creating staff users, 
    for adding other user roles, do it in nurse /employer admin panel. 

    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email','password','is_active','is_staff','is_nurse','is_employer')



class CustomUserAdmin(BaseUserAdmin):

     # The forms to add and change user instances

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('id','email','last_name','is_staff', 'is_active','is_nurse','is_employer','is_superuser','last_login')
    list_filter = ('email', 'is_staff', 'is_active','is_nurse','is_employer','is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','phone','password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class AddressBookAdmin(admin.ModelAdmin):


     list_display = ('id','street','alt_line','postcode','city','state')
     list_filter = ('postcode', 'city')
     fieldsets = (
        (None, {'fields': ('user','street','alt_line','postcode','city','state')}),
    )
     add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user','street', 'alt_line','postcode','city', 'state')}
        )
    )
     search_fields = ('city','postcode')
     ordering = ('city',)

class NurseAdmin(BaseUserAdmin):

    
    list_display = ('id','last_name','role','experience','phone','date_joined')
    list_filter = ('role', 'experience','is_active')

    fieldsets = (
        (None, {'fields': ('email','password','phone')}),#show the fields that could edit in admin panel
        ('Permissions', {'fields': ('is_nurse', 'is_rn','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','password1', 'password2','phone','role','experience','bank_account_name','bank_account_number')}
        ),
    )

    search_fields = ('email','experience','role')
    ordering = ('email',)




class EmployerAdmin(BaseUserAdmin):

    list_display = ('id','email','org_name','phone','date_joined')
    name__iexact='company'
    list_filter = ('org_name','is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_employer', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','password1', 'password2','phone','org_name','bank_account_name','bank_account_number')}
        ),
    )
    search_fields = ('org_name','city')
    ordering = ('email',)



class ShiftAdmin(admin.ModelAdmin):

    list_display=('id','employer','shift_start_date','shift_end_date','pub_date','updated_date')

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('pub_date','role','start_time','finish_time','description')},
        ),
    )
 



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Nurse, NurseAdmin)
admin.site.register(AddressBook, AddressBookAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Shift, ShiftAdmin)



