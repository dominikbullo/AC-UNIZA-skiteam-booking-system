from django.conf.urls import url
from django.urls import path, include

from users.api.views import FacebookLogin

urlpatterns = [
    path("", include('rest_auth.urls')),
    path("register/", include('rest_auth.registration.urls')),
    # Social
    path('facebook/', FacebookLogin.as_view(), name='fb_login'),
    # path('google/', GoogleLogin.as_view(), name='goggle_login')
]
