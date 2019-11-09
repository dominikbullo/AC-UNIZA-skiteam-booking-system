from django_registration.forms import RegistrationForm
from users.models import User


# from allauth.account.forms import SignupForm
# from django import forms

# # from https://dev.to/gajesh/the-complete-django-allauth-guide-la3
# class CustomSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=30, label='First Name')
#     last_name = forms.CharField(max_length=30, label='Last Name')
#
#     class Meta:
#         model = User
#
#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
#         return user


class CustomUserCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
