from django.contrib.auth import get_user_model
from simple_mail.mailer import BaseSimpleMail, simple_mailer


class WelcomeMail(BaseSimpleMail):
    email_key = "welcome"

    def set_context(self, user_id, welcome_link):
        user = get_user_model().objects.get(id=user_id)
        self.context = {"user": user, "welcome_link": welcome_link}

    def set_test_context(self):
        user_id = get_user_model().objects.order_by("?").first().id
        self.set_context(user_id, "http://my-webiste.com/my-path")


simple_mailer.register(WelcomeMail)
