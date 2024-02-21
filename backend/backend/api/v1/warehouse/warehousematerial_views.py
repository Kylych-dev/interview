from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.warehouse.models.warehouse import WarehouseMaterial
from .warehousematerial_serializers import WarehouseMaterialSerializer
from utils.customer_logger import logger


class WarehouseMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseMaterialSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        sewing_workshop = self.request.user.sewing_workshop
        if sewing_workshop and sewing_workshop.warehouse:
            warehouse = sewing_workshop.warehouse
            return WarehouseMaterial.objects.filter(
                is_delete=False, warehouse=warehouse
            )
        raise ValidationError({"Сообщение": "Пользователь не привязан ни к одному цеху"})

    @swagger_auto_schema(
        method="get",
        operation_description="Получить список сырья на складе",
        operation_summary="Получить список сырья на складе",
        operation_id="list_warehousematerial",
        tags=["Сырьё на складе"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Объект не найден"),
        },
    )
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление данных сырья на складе",
        operation_summary="Обновление данных сырья на складе",
        operation_id="update_warehousematerial",
        tags=["Сырьё на складе"],
        responses={
            200: openapi.Response(description="OK - Данные цеха успешно обновлены"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Объект не найден"),
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
        except Exception as ex:
            logger.error(f"Ошибка при обновлении сырья на складе", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)}, 
                status=status.HTTP_400_BAD_REQUEST
                )

    @swagger_auto_schema(
        method="post",
        operation_description="Создание сырья на складе",
        operation_summary="Создание сырья на складе",
        operation_id="create_warehousematerial",
        tags=["Сырьё на складе"],
        responses={
            201: openapi.Response(description="Created - Новое сырье на складе успешно создано"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
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
            logger.error(f"Ошибка при создании сырья на складе", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)}, 
                status=status.HTTP_400_BAD_REQUEST
                )
    
    @swagger_auto_schema(
        method="delete",
        operation_description="Soft delete.",
        operation_summary="Удаление сырья на складе",
        operation_id="delete_warehousematerial",
        tags=["Сырьё на складе"],
        responses={
            204: openapi.Response(description="No Content - Сырьё на складе успешно удален"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Объект не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.is_delete = True
            instance.save()
            return Response(
                {"message": "Сырьё на складе удалено"}, 
                status=status.HTTP_204_NO_CONTENT
                )
        except Http404 as ht:
            logger.warning(f"Сырьё на складе не найдено", extra={"Exception": ht, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": "Сырьё на складе не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(f"Ошибка при удалении сырья на складе", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            ) 
