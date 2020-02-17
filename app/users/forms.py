from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from allauth.account.forms import LoginForm, SignupForm

from users.models import User


class FullNameRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(FullNameRequiredMixin, self).__init__(*args, **kwargs)
        # make user first and last name field required
        # https: // stackoverflow.com / questions / 41967640 / how - to - make - email - field - required - in -the - django - user - admin / 41969315
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


# TODO validate existing emails ?
class CustomUserCreationForm(FullNameRequiredMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', "email", 'first_name', 'last_name')


class CustomUserChangeForm(FullNameRequiredMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


from allauth.account.forms import SignupForm
from django import forms


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
    is_parent = forms.BooleanField(initial=True, label='Is parent')

    # RES: https://dev.to/gajesh/the-complete-django-allauth-guide-la3
    # TODO doesn't go there, probabbly need custom signup view
    # https: // wsvincent.com / django - allauth - tutorial - custom - user - model /
    def signup(self, request, user):
        # user.first_name = self.cleaned_data['first_name']
        user.first_name = self.cleaned_data['first_name'] + "dominikjesuoper123"
        user.last_name = self.cleaned_data['last_name']
        user.is_parent = self.cleaned_data['is_parent']
        # Could by from form, good for now
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', "email", 'first_name', 'last_name', "is_parent")
# #
# # class CustomLoginForm(SignupForm):
# #     pass
