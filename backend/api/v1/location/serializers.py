from rest_framework import serializers
from apps.accounts.models.user_entry_check import UserEntryCheck


class UserEntryCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntryCheck
        fields = [
            'id', 
            'user',
            'entry_time',
            'exit_time',
        ]

    def save(self, **kwargs):
        user = kwargs['user']
        if user.is_anonymous:
            raise ValueError("Пользователь еще не авторизовался")

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance
