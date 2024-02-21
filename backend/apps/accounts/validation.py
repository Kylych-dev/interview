from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class INNValidator(RegexValidator):
    regex = r'^\d{14}$'
    message = _("Enter a valid INN. This value may contain only 14 digits.")
    flags = 0


@deconstructible
class PhoneNumberValidator(RegexValidator):
    """Validates numbers starting with 996, then 12 digits"""
    regex = r'^996\d{9}$'
    message = _("Phone number must start with 996 and contain 12 digits.")
    flags = 0



