from django_registration.forms import RegistrationForm

from users.models import CustomUser


class CustomUserCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = ('email',)
