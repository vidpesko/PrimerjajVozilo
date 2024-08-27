from rest_framework.views import APIView
from rest_framework.authtoken import views
from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from api_auth.serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Override create method to also return auth token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create new user in database
        data = serializer.validated_data
        data_exclude_vehicles = {key: value for key, value in data.items() if key != "vehicles"}
        created_user = User.objects.create_user(**data_exclude_vehicles)
        headers = self.get_success_headers(serializer.data)

        # Change data before returning Response
        token, created = Token.objects.get_or_create(user=created_user)
        data["token"] = token.key

        return Response(data, status=201, headers=headers)


# LEGACY CODE - using obtain_auth_token view instead
class UserLoginView(APIView):
    def post(self, request):
        try:
            user = authenticate(username=request.data["username"], password=request.data["password"])
        except KeyError:
            return Response({"error": "Credentials were not provided"}, status=401)

        # If user is authenticated
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "invalid Credentials"}, status=401)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
