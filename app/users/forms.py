from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from allauth.account.forms import LoginForm, SignupForm

from app import settings
from users.models import User


class FullNameRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(FullNameRequiredMixin, self).__init__(*args, **kwargs)
        # make user first and last name field required
        # https: // stackoverflow.com / questions / 41967640 / how - to - make - email - field - required - in -the - django - user - admin / 41969315


class CustomUserCreationForm(FullNameRequiredMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', "email", 'first_name', 'last_name')


class CustomUserChangeForm(FullNameRequiredMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

#
# class CustomLoginForm(SignupForm):
#     pass
