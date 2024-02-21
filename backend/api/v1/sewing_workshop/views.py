from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.workshop.models import SewingWorkshop
from .serializers import SewingWorkshopSerializer
from utils.customer_logger import logger


class SewingWorkshopViewSet(viewsets.ModelViewSet):
    queryset = SewingWorkshop.objects.all()
    serializer_class = SewingWorkshopSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        method="get",
        operation_description="Получение списка цехов.",
        operation_summary="Список цехов",
        operation_id="list_sewing_workshop",
        tags=["Цех"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, method=["get"])
    def list(self, request):
        serializer = SewingWorkshopSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление данных швейного цеха.",
        operation_summary="Обновление данных цехов",
        operation_id="update_sewing_workshop",
        tags=["Цех"],
        responses={
            200: openapi.Response(description="OK - Данные цеха успешно обновлены"),
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
            return Response(serializer.data)

        except Http404 as ht:
            logger.warning(
                f"Цех не найден",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Цех не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            logger.error(
                f"Ошибка при обновлении цеха",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="delete",
        operation_description="Soft delete.",
        operation_summary="Удалить цех",
        operation_id="delete_sewing_workshop",
        tags=["Цех"],
        responses={
            204: openapi.Response(description="No Content - Цех успешно удален"),
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
                {"message": "Цех удален"}, status=status.HTTP_204_NO_CONTENT
            )
        except Http404 as ht:
            logger.warning(
                f"Цех не найден",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(
                {"Сообщение": "Цех не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(
                f"Ошибка при удалении цеха",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
