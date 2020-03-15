from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView

from users.api.views import FacebookLogin, ConfirmEmailView

urlpatterns = [
    path("", include('rest_auth.urls')),
    path("register/", include('rest_auth.registration.urls')),
    
    # RES: https://gist.github.com/iMerica/a6a7efd80d49d6de82c7928140676957
    url(r'registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
        name='account_confirm_email'),

    # Social
    path('facebook/', FacebookLogin.as_view(), name='fb_login'),
    # path('google/', GoogleLogin.as_view(), name='goggle_login')
]
