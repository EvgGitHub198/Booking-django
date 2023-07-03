from drf_spectacular.utils import extend_schema
from users.serializers import UserSerializer


@extend_schema(
    request=UserSerializer,
    responses={201: UserSerializer},
    description="Register a new user",
    tags=["Users"],
)
def register_user(request):
    """
    Register a new user.

    This endpoint allows users to register by providing their username, email, and password.
    """
    pass
