from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.accounts.models.user_entry_check import UserEntryCheck
from .serializers import UserEntryCheckSerializer
from utils.customer_logger import logger




class UserEntryCheckModelViewSet(viewsets.ModelViewSet):
    queryset = UserEntryCheck.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = UserEntryCheckSerializer

    @swagger_auto_schema(
        method="get",
        operation_description="Список явки сотрудников",
        operation_id="list_entry_check",
        operation_summary="Список явки персонала",
        tags=["Пользователь(User)"],
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Bad Request"),
        },
    )
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="post",
        operation_description="Создание явки сотрудника",
        operation_id="create_entry_check",
        operation_summary="Создание явки сотрудника",
        tags=["Пользователь(User)"],
        responses={
            201: openapi.Response(description="Created - Явка сотрудника создано успешно"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(
                f"Ошибка при создании явки сотрудника",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
