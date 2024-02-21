from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.v1.wallet.serializers import EmployeeWalletSerializer
from apps.wallet.models import EmployeeWallet, Transaction
from utils.customer_logger import logger


class EmployeeWalletViewSet(viewsets.ModelViewSet):
    queryset = (
        EmployeeWallet.objects.select_related("user")
        .prefetch_related("transactions")
        .all()
    )
    serializer_class = EmployeeWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        method="get",
        operation_description="Кошелёк пользователя.",
        operation_summary="Кошелёк пользователя.",
        operation_id="employee_wallet",
        tags=["Кошелек пользователя"],
        responses={
            200: openapi.Response(description="OK - Кошелёк"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Кошелёк не найден"),
        },
    )
    @action(detail=True, methods=["get"])
    def employee_wallet(self, request, *args, **kwargs):
        try:
            wallet = self.queryset.get(user__id=self.request.user.pk)
            serializer = EmployeeWalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployeeWallet.DoesNotExist as ht:
            logger.warning(
                f"Кошелек сотрудника не существует",
                extra={
                    "Exception": ht,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method="post",
        operation_description="Кошелёк пользователя.",
        operation_summary="Кошелёк пользователя.",
        operation_id="subtract_balance",
        tags=["Кошелек пользователя"],
        responses={
            200: openapi.Response(description="OK - Кошелёк"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Кошелёк не найден"),
        },
    )
    @action(detail=True, methods=["post"])
    def subtract_balance(self, request, *args, **kwargs):
        amount = self.request.data.get("amount")
        description = self.request.data.get("description")
        amount = int(amount) * -1

        try:
            user = self.request.user
            wallet = self.queryset.get(user=user)

            if user.role not in {"director", "technologist"}:
                logger.warning(
                    f"Неправильный ввод",
                    extra={
                        "Exception": "У Пользователя не прав",
                        "Class": f"{self.__class__.__name__}.{self.action}",
                    },
                )
                return Response(
                    data="У Пользователя нет прав для выдачи / добавления денег",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if amount >= 0:
                logger.warning(
                    f"Неправильный ввод",
                    extra={
                        "Exception": "Сумма должна быть отрицательной",
                        "Class": f"{self.__class__.__name__}.{self.action}",
                    },
                )
                return Response(
                    data="Сумма должна быть отрицательной",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                description = (
                    description
                    if description
                    else f"Выплата заработной платы для пользователя {user} в сумме {amount}, {kwargs['pk']} {self.__class__.__name__}"
                )
                t = Transaction.objects.create(
                    wallet=wallet, amount=amount, description=description
                )
                t.subtract_wallet_balance()

            serializer = EmployeeWalletSerializer(wallet)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(
                f"Ошибка кошелёк не найден",
                extra={
                    "Exception": ex,
                    "Class": f"{self.__class__.__name__}.{self.action}",
                },
            )
            return Response(f"Ошибка: {ex}", status=status.HTTP_404_NOT_FOUND)
