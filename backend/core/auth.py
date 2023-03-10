from django.conf.urls import url
from django.urls import path, include

from apps.users.api.views import CustomConfirmEmailView
from django.urls import path, include
from . import views as acc_views

urlpatterns = [

    path("", include('rest_auth.urls')),

    # The django-rest-passwordreset urls to request a token and confirm pw-reset
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # overrides register with custom view
    # must be in the front of rest_auth.registration.urls
    # RES: https://github.com/Tivix/django-rest-auth/issues/292
    # RES: https://gist.github.com/iMerica/a6a7efd80d49d6de82c7928140676957
    url(r'^register/account-confirm-email/(?P<key>[-:\w]+)/$', CustomConfirmEmailView.as_view(),
        name='account_confirm_email'),
    path("register/", include('rest_auth.registration.urls')),

    # RES PASSWROD RESET : https://stackoverflow.com/questions/53945056/django-rest-auth-password-reset
    # url(r'^', include('django.contrib.auth.urls')),
]
