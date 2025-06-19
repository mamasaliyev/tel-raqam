import vonage
from django.conf import settings

client = vonage.Client(
    key="e7fc3bf0",  # Siz bergan API key
    secret="7Z82p2w7aPXH0He8"  # Siz bergan API secret
)

verify = vonage.Verify(client)

def send_verification_code(phone_number, brand=None):
    if brand is None:
        brand = settings.VONAGE_BRAND_NAME
    return verify.start_verification(number=phone_number, brand=brand)


def check_verification_code(request_id, code):
    return verify.check(request_id, code=code)
