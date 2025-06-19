# tel_raqam_code/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, VerifyCodeSerializer
from .models import User
from django.conf import settings
from tel_raqam_code.utils import verify
import logging
import vonage  # Asl kutubxona



logger = logging.getLogger(__name__)

# Vonage Client va Verify obyekti bitta joyda
client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
verify_client = vonage.Verify(client)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            try:
                # 🔽 Vonage orqali SMS yuborish shu yerda bo‘ladi
                response = verify.start_verification(
                    number=phone_number,
                    brand=settings.VONAGE_BRAND_NAME
                )

                if response["status"] == "0":
                    # Foydalanuvchini yaratish yoki olish
                    user, created = User.objects.get_or_create(
                        phone_number=phone_number,
                        defaults={'is_verified': False}
                    )
                    user.request_id = response["request_id"]
                    user.save()

                    return Response({
                        "message": "Tasdiqlash kodi yuborildi",
                        "request_id": response["request_id"]
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({
                        "error": response.get("error_text", "Noma'lum xato")
                    }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({
                    "error": f"Xatolik yuz berdi: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        logger.debug(f"Verify request data: {request.data}")
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(phone_number=phone_number)
                if not user.request_id:
                    return Response({
                        "error": "Tasdiqlash jarayoni boshlanmagan"
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Kodni tekshirish
                check_response = verify_client.check(user.request_id, code=code)

                logger.debug(f"Vonage check response: {check_response}")
                if check_response["status"] == "0":
                    user.is_verified = True
                    user.save()
                    return Response({
                        "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz!"
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "error": check_response.get("error_text", "Noto'g'ri kod")
                    }, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response({
                    "error": "Foydalanuvchi topilmadi"
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Vonage xatosi: {str(e)}")
                return Response({
                    "error": f"Vonage sozlamalarida xato: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
