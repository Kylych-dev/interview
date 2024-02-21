from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.cut.models import Cut
from api.v1.cut.serializers import CutSerializer
from utils.customer_logger import logger


class CutModelViewSet(viewsets.ModelViewSet):
    serializer_class = CutSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # return Cut.objects.all().select_related("order")
        return Cut.objects.filter(is_delete=False).select_related("order")

    @swagger_auto_schema(
        method="get",
        operation_description="Получение списка элементов кроя.",
        operation_summary="Список элементов кроя",
        operation_id="list_cut",
        tags=["Крой"],
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
        operation_description="Создание нового элемента кроя.",
        operation_summary="Создание элемента кроя",
        operation_id="create_cut",
        tags=["Крой"],
        responses={
            201: openapi.Response(description="Created - Элемент успешно создан"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as ex:
            logger.error(f"Ошибка при создании кроя", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление данных элемента кроя.",
        operation_summary="Обновление элемента кроя",
        operation_id="update_cut",
        tags=["Крой"],
        responses={
            200: openapi.Response(description="OK - Элемент успешно обновлен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        try:
            cut = self.get_object()
            serializer = CutSerializer(cut, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            logger.error(f"Ошибка при обновлени кроя", extra={"Exception": {status.HTTP_400_BAD_REQUEST}, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Http404 as ht:
            logger.warning(f"Крой не найден", extra={"Exception": ht, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": "Крой не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(f"Ошибка при обновлении кроя", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
        

    @swagger_auto_schema(
        method="delete",
        operation_description="Удаление элемента кроя.",
        operation_summary="Удаление элемента кроя",
        operation_id="delete_cut",
        tags=["Крой"],
        responses={
            204: openapi.Response(description="No Content - производство успешно удалено"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        try:
            instance = self.get_queryset()
            instance.delete = True 
            instance.save()
            return Response(
                {"message": "Крой помечен как удаленный"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404 as ht:
            logger.warning(f"Крой не найден", extra={"Exception": ht, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": "Крой не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(f"Ошибка при удалении кроя", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
