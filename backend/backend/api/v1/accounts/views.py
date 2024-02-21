from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.accounts.models.role_status import UserRole
from apps.accounts.models.models import CustomUser
from .serializers import CustomUserSerializer, UserRoleSerializer
from utils.customer_logger import logger


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.select_related("sewing_workshop", "role").all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]  # todo: change for permission

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        if self.request.query_params.get("get_my_sewing_workshop"):
            qs = qs.filter(sewing_workshop_id=self.request.user.sewing_workshop_id)
        return qs

    @swagger_auto_schema(
        method="get",
        operation_description="Получить список пользователей.",
        operation_summary="Получить список пользователей",
        operation_id="list_users",
        tags=["Пользователь(User)"],
        responses={
            200: openapi.Response(
                description="OK - Список пользователей получено успешно."
            ),
            401: openapi.Response(description="Ошибка аутентификации"),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        method="get",
        operation_description="Получить профиль пользователя",
        operation_summary="Получить профиль пользователя",
        operation_id="user_detail",
        tags=["Пользователь(User)"],
        responses={
            200: openapi.Response(description="OK - Профиль пользователя получено."),
            401: openapi.Response(description="Ошибка аутентификации"),
            400: openapi.Response(description="Bad Request - Invalid Input"),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    @action(detail=True, methods=["get"])
    def user_detail(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(phone_number=kwargs.get("phone_number"))
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # except Http404 as ht:
        #     logger.warning(f"Пользователь не найден", extra={"Exception": f"{ex}", "error_code": f"{__class__.__name__}.{self.action}"})
        #     return Response(
        #         {"Сообщение": "Пользователь не найден"},
        #         status=status.HTTP_404_NOT_FOUND
        #     )
        except CustomUser.DoesNotExist as ex:
            logger.warning(
                f"Объект не найден",
                extra={
                    "Exception": f"{ex}",
                    "Class": f"{__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(
                f"Ошибка при обработке запроса",
                extra={
                    "Exception": f"{ex}",
                    "Class": f"{__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновить данные пользователя.",
        operation_summary="Обновить данные пользователя.",
        operation_id="update_detail",
        tags=["Пользователь(User)"],
        responses={
            200: openapi.Response(
                description="OK - Профиль пользователя обновлено успешно."
            ),
            401: openapi.Response(description="Ошибка аутентификации"),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update_detail(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(phone_number=kwargs.get("phone_number"))
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist as ex:
            logger.warning(
                f"При изменении пользователь не найден",
                extra={
                    "Exception": ex,
                    "error_code": f"{__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "При изменении пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        method="get",
        operation_description="Получить профиль.",
        operation_summary="Получить профиль.",
        operation_id="user_profile",
        tags=["Пользователь(User)"],
        responses={
            200: openapi.Response(
                description="OK - Профиль пользователя получено успешно."
            ),
            401: openapi.Response(description="Ошибка аутентификации"),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    @action(detail=True, methods=["get"])
    def user_profile(self, request, *args, **kwargs):
        try:
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404 as ht:
            logger.warning(
                f"Объект не найден",
                extra={
                    "Exception": f"{ht}",
                    "error_code": f"{__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND
            )


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        method="get",
        operation_description="Получить список ролей.",
        operation_summary="Получить список ролей",
        operation_id="list_roles",
        tags=["Роли"],
        responses={
            200: openapi.Response(
                description="OK - Список ролей получено успешно."
            ),
            401: openapi.Response(description="Ошибка при получении ролей"),
            404: openapi.Response(description="Not Found - Роль не найден"),
        },
    )
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
