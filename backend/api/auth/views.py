from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.auth.serializers import RegisterSerializer
from api.auth.verify import twilio_send, twilio_check
from apps.accounts.forms import VerifyForm
from apps.accounts.models import CustomUser
from utils.phone_normalize import normalize_phone_number
from utils.customer_logger import logger


class RegisterView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Создание нового пользователя.",
        operation_summary="Создание нового пользователя",
        operation_id="register_user",
        tags=["Регистрация(register)"],
        responses={
            201: openapi.Response(description="OK - Регистрация прошла успешно."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                validated_data = serializer.validated_data
                validated_data.pop("password2")
                user_workshop = (
                    None
                    if request.user.is_anonymous
                    else request.user.sewing_workshop_id
                )
                user = CustomUser(
                    sewing_workshop_id=user_workshop,
                    **validated_data,
                )
                user.set_password(validated_data.get("password"))
                user.save()
                # twilio_send(user.phone_number)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as ex:
                # todo Добавить позже логирование
                # logger.error(f"User creation failed: {e}")
                logger.error(
                    f"Клиент не найден",
                    extra={
                        "Exception": ex,
                        "Class": f"{self.__class__.__name__}.{self.action}",
                    },
                )
                return Response(
                    data={"error": f"User creation failed: {str(ex)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify(self, request, *args, **kwargs):
        form = VerifyForm(data=request.data)
        if form.is_valid():
            code = form.cleaned_data.get("code")
            if twilio_check(request.user.phone_number, code):
                request.user.is_verified = True
                request.user.save()
                return Response(
                    {"detail": "User successfully verified"}, status=status.HTTP_200_OK
                )
        return Response(
            {"detail": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST
        )

    def resend_verify(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=request.user.pk)
        if user:
            try:
                # Assume twilio_send is a function that sends a verification code via Twilio
                twilio_send(user.phone_number)
                return Response(
                    {"detail": "Verification code resent successfully"},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"detail": f"Failed to resend verification code: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"detail": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserAuthenticationView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Авторизация пользователя для получения токена.",
        operation_summary="Авторизация пользователя для получения токена",
        operation_id="login_user",
        tags=["Вход(login)"],
        responses={
            200: openapi.Response(
                description="OK - Авторизация пользователя прошла успешно."
            ),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    def login(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]

        try:
            phone_number = normalize_phone_number(phone_number)
            user = CustomUser.objects.get(phone_number=phone_number)

        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Такого пользователя не существует")

        if user is None:
            raise AuthenticationFailed("Такого пользователя не существует")

        if not user.check_password(password):
            raise AuthenticationFailed("Не правильный пароль")

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return Response(
            data={
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="Выход для удаления токена.",
        operation_summary="Выход для удаления токена",
        operation_id="logout_user",
        tags=["Выход(logout)"],
        responses={
            201: openapi.Response(
                description="OK - Выход пользователя прошла успешно."
            ),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def logout(self, request):
        try:
            if "refresh_token" in request.data:
                refresh_token = request.data["refresh_token"]
                if refresh_token:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                return Response("Вы вышли из учетной записи", status=status.HTTP_200_OK)
            else:
                return Response(
                    "Отсутствует refresh_token", status=status.HTTP_400_BAD_REQUEST
                )
            refresh_token = request.data["refresh_token"]
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response("Вы вышли из учетной записи", status=status.HTTP_200_OK)

        except TokenError:
            raise AuthenticationFailed("Не правильный токен")
