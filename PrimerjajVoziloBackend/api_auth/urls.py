from rest_framework.authtoken import views

from django.urls import path

from api_auth.views import UserList, UserDetail, UserRegistrationView


urlpatterns = [
    # User authentication

    # List users & get user detail
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
    # Login & register
    path("get-token/", views.obtain_auth_token),
    path("register/", UserRegistrationView.as_view()),
]
