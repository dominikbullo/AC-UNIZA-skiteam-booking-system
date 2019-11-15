from django.urls import path, include

urlpatterns = [
    # Login via browser
    path("", include('allauth.urls')),

    # Login via browsable api
    path("api-auth/", include("rest_framework.urls")),

    # Login via REST
    path("api/rest-auth/", include("rest_auth.urls")),

    # Registration via REST
    path("api/rest-auth/signup/", include("rest_auth.registration.urls")),

    # url(r'^api-token-auth/', obtain_auth_token)
]
