from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bot = TgClient()

    def handle(self, *args, **options):
        offset = 0
        self.stdout.write(self.style.SUCCESS('Bot started'))
        while True:
            updates = self._bot.get_updates(
                offset=offset, allowed_updates=['message']
            )
            for update in updates.result:
                offset = max(offset, update.update_id + 1)
                self.handle_message(update.message)

    def handle_message(self, message: Message):
        tg_user, _ = TgUser.objects.get_or_create(
            chat_id=message.chat.id,
            defaults={'username': message.chat.username},
        )
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self._bot.send_message(
                message.chat.id,
                f'Ваш код подтверждения: {tg_user.verification_code}',
            )
        else:
            self._bot.send_message(message.chat.id, 'Вы уже подтверждены')

    def handle_auth_user(self, tg_user: TgUser, msg: Message):
        if msg.text.startswith('/'):
            match msg.text:
                case '/goals':
                    ...
                case '/create':
                    ...
                case '/cancel':
                    ...
        else:
            ...
