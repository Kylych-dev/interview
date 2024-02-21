def normalize_phone_number(phone_number):
    # Remove non-numeric characters
    phone_number = ''.join(c for c in phone_number if c.isdigit())

    # Remove leading zeros
    phone_number = phone_number.lstrip('0')

    # Add country code if missing
    if not phone_number.startswith('996'):
        phone_number = '996' + phone_number

    return phone_number
