from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.warehouse.models.warehouse import Warehouse
from .warehouse_serializers import WarehouseSerializer
from utils.customer_logger import logger


class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        sewing_workshop = self.request.user.sewing_workshop
        if sewing_workshop:
                return Warehouse.objects.filter(
                is_delete=False, sewing_workshop=sewing_workshop
            )
        raise ValidationError({"Сообщение": "Пользователь не привязан ни к одному цеху"})

    @swagger_auto_schema(
        method="get",
        operation_description="Получение информации о складах",
        operation_summary="получить информацию о складе",
        operation_id="retrieve_warehouse",
        tags=["Склад"],
        responses={
            200: openapi.Response(description="OK - Склад успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Склад не найден"),
        },
    )
    @action(detail=True, methods=["get"])
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            logger.error(f"Склад не найден", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"message": "Склад не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        
    @swagger_auto_schema(
        method="delete",
        operation_description="Soft delete.",
        operation_summary="Удалить Склад",
        operation_id="delete_warehouse",
        tags=["Склад"],
        responses={
            204: openapi.Response(description="No Content - Склад успешно удален"),
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
                {"message": "Склад удалён"}, 
                status=status.HTTP_204_NO_CONTENT
                )
        except Http404 as ht:
            logger.warning(f"Склад не найден", extra={"Exception": ht, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": "Склад не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(f"Ошибка при удалении склада", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )  

