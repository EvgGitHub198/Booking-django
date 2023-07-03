from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer, TokenObtainPairSerializer


@extend_schema(
    request=UserSerializer,
    responses={201: UserSerializer},
    description="Register a new user",
    tags=["Users"],
)
class RegisterView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Register a new user",
        tags=["Users"],
    )
    def post(self, request):
        """
        Register a new user.

        This endpoint allows users to register by providing their username, email, and password.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=TokenObtainPairSerializer,
    responses={200: TokenObtainPairSerializer},
    description="Obtain a new token pair",
    tags=["Authentication"],
)
class TokenObtainPairView(APIView):
    @extend_schema(
        request=TokenObtainPairSerializer,
        responses={200: TokenObtainPairSerializer},
        description="Obtain a new token pair",
        tags=["Authentication"],
    )
    def post(self, request):
        """
        Obtain a new token pair.

        This endpoint allows users to obtain a new token pair by providing their email and password.
        """
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data["email"])
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
