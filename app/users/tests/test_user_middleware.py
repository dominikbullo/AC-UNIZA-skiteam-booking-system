from django.conf import settings
from django.test import TestCase

from re import compile


class RedirectionsTest(TestCase):
    def test_redirect_to_login(self):
        addresses_to_redirect = [
            "anything",
            "dashboard",
            "login",
            "register",
        ]
        for address in addresses_to_redirect:
            response = self.client.get("/" + address + "/")

            self.assertEqual(response.status_code, 302)
            login_url = settings.LOGIN_URL + "?next=/" + address + "/"
            self.assertEqual(response['Location'], login_url)

    # def process_request(self, request):
    #     assert hasattr(request, 'user')
    #     if not request.user.is_authenticated:
    #         path = request.path_info.lstrip('/')
    #         if not any(m.match(path) for m in EXEMPT_URLS):
    #             path = request.get_full_path()
    #             return redirect_to_login(path, settings.LOGIN_URL, REDIRECT_FIELD_NAME)

    def test_public_adresses(self):
        TEST_ADRESSES = [
            # "account/login",
            # "account/signup",
            # "account/confirm-email",
            # "account/password/reset"
        ]

        for address in TEST_ADRESSES:
            response = self.client.get("/" + address + "/")
            # print(address)
            self.assertEqual(response.status_code, 200)

# TODO Middleware tests
# If redirect everything to LOGIN_URL
# After login redirect
# Unverified emails
# check public urls /account/ and so on.. for reg/log/reset pass
# http://localhost:8000/account/aSDasdasd -> not redirect to login -> bcs its public address
