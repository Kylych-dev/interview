from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from utils.customer_logger import logger
from apps.client.models import Client
from apps.accounts.permissions import OwnerPermission, DirectorPermission
from .serializers import ClientSerializer


class ClientModelViewSet(viewsets.ModelViewSet):
    """
    Вместо определения queryset, используется метод get_queryset(), чтобы дополнительно
    настроить запрос к объектам Client, чтобы загрузить данные о складе.
    """

    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticated,]
    permission_classes = [
        permissions.AllowAny,
    ]

    def get_queryset(self):
        sewing_workshop = self.request.user.sewing_workshop
        if sewing_workshop and sewing_workshop.warehouse:
            warehouse = sewing_workshop.warehouse
            return Client.objects.filter(is_delete=False, warehouse=warehouse)

        raise ValidationError(
            {"Сообщение": "Пользователь не привязан ни к одному цеху"}
        )

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [DirectorPermission()]
        return [OwnerPermission()]

    @swagger_auto_schema(
        method="get",
        operation_description="Список клиентов.",
        operation_id="list_clients",
        operation_summary="Список клиентов",
        tags=["Клиент"],
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
        method="put",
        operation_description="Обновление данных клиента",
        operation_id="update_clients",
        operation_summary="Обновление клиента",
        tags=["Клиент"],
        responses={
            200: openapi.Response(description="OK - Список готовых продуктов"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        try:
            client = self.get_object()
            serializer = self.get_serializer(client, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        except Http404 as ht:
            logger.error(
                f"Клиент не найден",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Клиент не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            logger.error(
                f"Ошибка при обновлении клиента",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="post",
        operation_description="Создание нового клиента.",
        operation_id="create_client",
        operation_summary="Создание клиента",
        tags=["Клиент"],
        responses={
            201: openapi.Response(description="Created - Клиент создан успешно"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializer.save(warehouse=self.request.user.sewing_workshop.warehouse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(
                f"Ошибка при создании клиента",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="delete",
        operation_description="Удаление клиента.",
        operation_summary="Удаление клиента",
        operation_id="client-delete",
        tags=["Клиент"],
        responses={
            204: openapi.Response(description="No Content - Клиент успешно удален"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.is_delete = True
            instance.save()
            return Response(
                {"message": "Клиент удалён"}, status=status.HTTP_204_NO_CONTENT
            )
        except Http404 as ht:
            logger.warning(
                f"Клиент не найден",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Клиент не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(
                f"Ошибка при удалении клиента",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
