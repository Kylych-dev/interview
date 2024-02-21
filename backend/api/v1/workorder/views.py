from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework import serializers

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.fabrication.models import Fabrication
from .serializers import FabricationSerializer
from utils.customer_logger import logger


class FabricationViewSet(viewsets.ModelViewSet):
    queryset = Fabrication.objects.prefetch_related("product")
    serializer_class = FabricationSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @swagger_auto_schema(
        method="get",
        operation_description="Список производства.",
        operation_summary="Получить список производств",
        operation_id="list_fabrication",
        tags=["Производство"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["get"])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление данных производства.",
        operation_summary="Обновление данных производства",
        operation_id="udpate_fabrication",
        tags=["Производство"],
        responses={
            200: openapi.Response(
                description="OK - Данные производства успешно обновлены"
            ),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404 as ht:
            logger.warning(
                f"Производство не найдено",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Производство не найдено"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            logger.error(
                f"Ошибка при обновлении производства",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        method="post",
        operation_description="Создание производства",
        operation_summary="Создание производства",
        operation_id="create_fabriction",
        tags=["Производство"],
        responses={
            201: openapi.Response(description="Created - Производство успешно создано"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(
                f"Ошибка при создании производства",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": str(ex)},
                status=serializers.ValidationError("Illegal parameters"),
            )

    @swagger_auto_schema(
        method="delete",
        operation_description="Удаление производства",
        operation_summary="Удалить производство",
        operation_id="delete_fabrication",
        tags=["Производство"],
        responses={
            204: openapi.Response(
                description="No Content - производство успешно удалено"
            ),
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
                {"message": "Производство удалено"}, status=status.HTTP_204_NO_CONTENT
            )
        except Http404 as ht:
            logger.warning(
                f"Производство не найдено",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Производство не найдено"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            logger.error(
                f"Ошибка при удалении производства",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
