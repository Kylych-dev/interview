from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q

from apps.accounts.models import CustomUser
from apps.client.models import Client


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return

        user = None
        # Проверяем, является ли username номером телефона или ИНН
        try:
            user = CustomUser.objects.get(
                Q(phone_number=username) | Q(inn=username)
            )
        except CustomUser.DoesNotExist:
            pass

        # Если не найден пользователь, попробуем поискать среди клиентов
        if not user:
            try:
                user = Client.objects.get(
                    Q(phone_number=username) | Q(email=username)
                )
            except Client.DoesNotExist:
                pass

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    def get_user_by_username(self, username):
        try:
            return CustomUser.objects.get(
                Q(phone_number=username) | Q(inn=username)
            )
        except CustomUser.DoesNotExist:
            return None
