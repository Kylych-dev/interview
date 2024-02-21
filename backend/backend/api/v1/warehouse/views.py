from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions, serializers


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from apps.product.models import Product
from .serializers import ProductSerializer
from utils.customer_logger import logger


# todo: переделать  продукт везде перенсти и поменять поля
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related(
        "warehouse", "product_category", "cut"
    )
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @swagger_auto_schema(
        method="get",
        operation_description="Получить список готовых продуктов",
        operation_summary="Получение списка готовых продуктов",
        operation_id="list_products",
        tags=["Готовые_Продукты"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=False, method=["get"])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление данных продукта",
        operation_summary="Обновление данных продукта",
        operation_id="update_products",
        tags=["Готовые_Продукты"],
        responses={
            200: openapi.Response(description="OK - Объект успешно обновлен"),
            400: openapi.Response(
                description="Bad Request - Неверный запрос или некорректные данные"
            ),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(
                f"Ошибка при обновлении готового продукта",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method="post",
        operation_description="Создание готовых продуктов",
        operation_summary="Создание готовых продуктов",
        operation_id="create_product",
        tags=["Готовые_Продукты"],
        responses={
            201: openapi.Response(description="Created - Новый продукт успешно создан"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(
                f"Ошибка при создании готового продукта",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="delete",
        operation_description="Удаление элемента клиента.",
        operation_summary="Удаление элемента клиента",
        operation_id="delete_product",
        tags=["Готовые_Продукты"],
        responses={
            204: openapi.Response(
                description="No Content - Готовый_Продукт успешно удален"
            ),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        try:
            instance = self.get_queryset()
            instance.is_delete = True
            instance.save()
            return Response(
                {"message": "Готовый_Продукт удалён"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.error(
                f"Ошибка при удалении готового продукта",
                extra={
                    "Exception": e,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response({"Сообщение": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class ProductTemplateViewSet(viewsets.ModelViewSet):
#     queryset = ProductTemplate.objects.all()
#     serializer_class = ProductTemplateSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     @swagger_auto_schema(
#         method="get",
#         operation_description="Получение списка образцов продукта",
#         operation_summary="Получить список образцов продукта",
#         operation_id="list_product-template",
#         tags=["Образец Продукта"],
#         responses={
#             200: openapi.Response(description="OK - Список успешно получен"),
#             400: openapi.Response(description="Bad Request - Неверный запрос"),
#             401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
#             404: openapi.Response(description="Not Found - Ресурс не найден"),
#         },
#     )
#     @action(detail=False, methods=["get"])
#     def list(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.get_queryset(), many=True)
#         return Response(serializer.data)
#
#     @swagger_auto_schema(
#         method="post",
#         operation_description="Создание Образца Продукта",
#         operation_summary="Создание Образца Продукта",
#         operation_id="create_product-template",
#         tags=["Образец Продукта"],
#         responses={
#             201: openapi.Response(
#                 description="Created - Новый образец продукта успешно создан"
#             ),
#             400: openapi.Response(description="Bad Request - Неверный запрос"),
#             401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
#         },
#     )
#     @action(detail=True, methods=["post"])
#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as ex:
#             logger.error(
#                 f"Ошибка при создании образца продукта",
#                 extra={
#                     "Exception": ex,
#                     "Class": f"{self.__class__.__name__}.{self.action}",
#                 },
#             )
#             return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
#
#     @swagger_auto_schema(
#         method="put",
#         operation_description="Обновление данных образца продукта",
#         operation_summary="Обновление данных образца продукта",
#         operation_id="update_product-template",
#         tags=["Образец Продукта"],
#         responses={
#             200: openapi.Response(
#                 description="OK - Данные образца продукта успешно обновлены"
#             ),
#             400: openapi.Response(description="Bad Request - Неверный запрос"),
#             401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
#             404: openapi.Response(description="Not Found - Ресурс не найден"),
#         },
#     )
#     @action(detail=True, methods=["put"])
#     def update(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(self.get_object(), data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         except Http404 as ht:
#             logger.warning(
#                 f"Образец продукта не найден",
#                 extra={
#                     "Exception": ht,
#                     "Class": f"{self.__class__.__name__}.{self.action}",
#                 },
#             )
#             return Response(
#                 {"Сообщение": "Образуц продукта не найден"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except Exception as ex:
#             logger.error(
#                 f"Ошибка при обновлении образца продукта",
#                 extra={
#                     "Exception": ex,
#                     "Class": f"{self.__class__.__name__}.{self.action}",
#                 },
#             )
#             return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
#
#     @swagger_auto_schema(
#         method="delete",
#         operation_description="Удаление элемента образца продукта.",
#         operation_summary="Удаление элемента образца продукта",
#         operation_id="delete_product_template",
#         tags=["Образец Продукта"],
#         responses={
#             204: openapi.Response(
#                 description="No Content - Образец Продукта успешно удален"
#             ),
#             400: openapi.Response(description="Bad Request - Неверный запрос"),
#             401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
#             404: openapi.Response(description="Not Found - Ресурс не найден"),
#         },
#     )
#     @action(detail=True, methods=["delete"])
#     def delete(self, request, pk=None):
#         try:
#             instance = self.get_queryset()
#             instance.is_delete = True
#             instance.save()
#             return Response(
#                 {"message": "Образец продукта удалён"},
#                 status=status.HTTP_204_NO_CONTENT,
#             )
#         except Http404 as ht:
#             logger.warning(
#                 f"Образец продукта не найден",
#                 extra={
#                     "Exception": ht,
#                     "Class": f"{self.__class__.__name__}.{self.action}",
#                 },
#             )
#             return Response(
#                 {"Сообщение": "Образец продукта не найден"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except Exception as ex:
#             logger.error(
#                 f"Ошибка при удалении образца продукта",
#                 extra={
#                     "Exception": ex,
#                     "Class": f"{self.__class__.__name__}.{self.action}",
#                 },
#             )
#             return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
