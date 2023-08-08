from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from bot.models import TgUser


class TgUserVerifyView(APIView):
    def patch(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                verification_code = request.data.get('verification_code')
                tg_user = TgUser.objects.get(verification_code=verification_code)
                tg_user.update_verification_code(drop=True)
                tg_user.user = request.user
                tg_user.save()
                return JsonResponse(
                    status=200,
                    data={
                        'tg_id': tg_user.chat_id,
                        'username': tg_user.username,
                        'user_id': tg_user.user.id,
                    },
                )
            except TgUser.DoesNotExist:
                return JsonResponse(status=403, data={'detail': 'Неверный код'})
