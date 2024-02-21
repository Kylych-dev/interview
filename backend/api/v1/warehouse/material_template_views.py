from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.warehouse.models.material import MaterialTemplate
from .material_template_serializers import MaterialTemplateSerializer
from utils.customer_logger import logger


class MaterialTemplateViewSet(viewsets.ModelViewSet):
    queryset = MaterialTemplate.objects.all()
    serializer_class = MaterialTemplateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        method="get",
        operation_description="Получить список сырья.",
        operation_summary="Получить список сырья",
        operation_id="list_material",
        tags=["Сырьё(material_template)"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
        },
    )
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновить данные сырья.",
        operation_summary="Обновить данные сырья",
        operation_id="update_material",
        tags=["Сырьё(material_template)"],
        responses={
            200: openapi.Response(description="OK - Данные успешно обновлены"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", True)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Http404 as ht:
            logger.warning(f"Сырьё не найдено", extra={"Exception": ht, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": "Сырьё не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            logger.error(f"Ошибка при обновлении сырья", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        method="post",
        operation_description="Создать сырьё.",
        operation_summary="Получить список сырья",
        operation_id="create_material",
        tags=["Сырьё(material_template)"],
        responses={
            201: openapi.Response(description="OK - Сырьё успешно создано"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(f"Ошибка при создании сырья", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
                {"Сообщение": str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @swagger_auto_schema(
        method="delete",
        operation_description="Soft delete.",
        operation_summary="Удалить сырьё",
        operation_id="delete_material",
        tags=["Сырьё(material_template)"],
        responses={
            204: openapi.Response(description="No Content - Сырьё успешно удалено"),
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
                    {"message": "Сырьё удалено"}, 
                    status=status.HTTP_204_NO_CONTENT
                    )
        except Http404 as ht:
            logger.warning(f"Сырьё не найдено", extra={"Exception": ht, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
            {"Сообщение": "Сырьё не найдено"},
            status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(f"Ошибка при удалении сырья", extra={"Exception": ex, "Class": f"{self.__class__.__name__}.{self.action}"})
            return Response(
            {"Сообщение": str(ex)},
            status=status.HTTP_400_BAD_REQUEST
            )
