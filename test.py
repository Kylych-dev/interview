# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC3974ecb027cb43b698b54e72baeba37e"
auth_token = "d3681ccc5597d77204f8d59a432a5cd9"
verify_sid = "VA975e5782fcd668fb9fb57fe09ea9b3b0"
verified_number = "+996703355550"

client = Client(account_sid, auth_token)

verification = client.verify.v2.services(verify_sid) \
  .verifications \
  .create(to=verified_number, channel="sms")
print(verification.status)

otp_code = input("Please enter the OTP:")

verification_check = client.verify.v2.services(verify_sid) \
  .verification_checks \
  .create(to=verified_number, code=otp_code)
print(verification_check.status)