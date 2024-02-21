from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where membership_number is the unique identifiers
    for authentication.
    """

    def create_user(self, phone_number, inn=None, password=None, **extra_fields):
        """
        Create and save a User with given membership_number and password.
        """
        user = self.model(
            phone_number=phone_number,
            inn=inn,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, inn=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given membership_number and password.
        """
        user = self.create_user(phone_number, inn, password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user