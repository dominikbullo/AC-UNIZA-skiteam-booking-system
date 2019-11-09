from django_registration.forms import RegistrationForm

from .models import User


class CustomUserCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = ('email',)
