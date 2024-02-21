from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.order.models import Order
from api.v1.order.serializers import OrderSerializer
from utils.customer_logger import logger


class OrderModelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        sewing_workshop = self.request.user.sewing_workshop
        if sewing_workshop and sewing_workshop.warehouse:
            warehouse = sewing_workshop.warehouse
            return Order.objects.filter(warehouse=warehouse).select_related("client")
        raise ValidationError(
            {"Сообщение": "Пользователь не привязан ни к одному цеху"}
        )

    @swagger_auto_schema(
        method="get",
        operation_description="Получение списка заказов.",
        operation_summary="Список заказов",
        operation_id="list_order",
        tags=["Заказ"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            201: openapi.Response(description="Created - Новый элемент успешно создан"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        method="post",
        operation_description="Создание заказа.",
        operation_summary="Создание заказа",
        operation_id="create_order",
        tags=["Заказ"],
        responses={
            201: openapi.Response(description="Created - Новый элемент успешно создан"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            warehouse = self.request.user.sewing_workshop.warehouse
            serializer.save(warehouse=warehouse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(
                f"Ошибка при создании заказа",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление заказа.",
        operation_summary="Обновление заказа",
        operation_id="update_order",
        tags=["Заказ"],
        responses={
            200: openapi.Response(description="OK - Обновление заказа"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            serializer = OrderSerializer(order, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404 as ht:
            logger.warning(
                f"Заказ не найден",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.format(
                f"Ошибка при обновлении заказа",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="delete",
        operation_description="Soft delete.",
        operation_summary="Удалить заказ",
        operation_id="delete_order",
        tags=["Заказ"],
        responses={
            204: openapi.Response(description="No Content -  Заказ успешно удален"),
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
                {"message": "Заказ удален"}, status=status.HTTP_204_NO_CONTENT
            )
        except Http404 as ht:
            logger.warning(
                f"Заказ не найден",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(
                f"Ошибка при удалении заказа",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
