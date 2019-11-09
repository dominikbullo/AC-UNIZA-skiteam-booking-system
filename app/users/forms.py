from django_registration.forms import RegistrationForm
from users.models import User


class CustomUserCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
