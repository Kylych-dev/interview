from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN
)
verify = client.verify.services(
    settings.TWILIO_VERIFY_SID
)


def twilio_send(phone):
    verify.verifications.create(to=phone, channel='sms')


def twilio_check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'
