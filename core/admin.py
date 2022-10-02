from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

#from .forms import CustomUserCreationForm, CustomUserChangeForm


from .models import CustomUser,Nurse, Employer,AddressBook



class CustomUserCreationForm(forms.ModelForm):

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
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

    list_display = ('email', 'is_staff', 'is_active','is_nurse','is_employer','is_superuser')
    list_filter = ('email', 'is_staff', 'is_active','is_nurse','is_employer','is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_nurse','is_employer')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class AddressBookAdmin(admin.ModelAdmin):
    list_display = ('street','alt_line','postcode','city','state')
    list_filter = ('postcode', 'city')

class NurseAdmin(BaseUserAdmin):

  
    list_display = ('email','role','experience','city','phone')
    list_filter = ('role', 'experience','city', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_nurse', 'is_rn','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','phone','role','experience','street','postcode','city')}
        ),
    )
    search_fields = ('email','experience','city','role')
    ordering = ('email',)



class EmployerAdmin(BaseUserAdmin):

    list_display = ('email','org_name','city','phone','email')
    name__iexact='company'
    list_filter = ('org_name','city', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_employer', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','phone','org_name','street','postcode','city')}
        ),
    )
    search_fields = ('org_name','city')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Nurse, NurseAdmin)
#admin.site.register(AddressBook, AddressBookAdmin)
admin.site.register(Employer, EmployerAdmin)



