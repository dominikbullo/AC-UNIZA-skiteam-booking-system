from django.contrib.auth import get_user_model


def custom_create_user(**params):
    # TODO create user with same method as in login
    return get_user_model().objects.create_user(**params)
