from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal, GoalCategory


class FSM:
    def __init__(self):
        self.send_message: callable = TgClient().send_message
        self.create_list: list[callable] = [
            self.get_category,
            self.get_title,
            self.get_description,
        ]
        self.users: dict[int, self.UserState] = {}
        self.indent = '\n   '

    def __getitem__(self, item):
        return self.users.get(item)

    def start_create(self, message: Message, user: TgUser):
        categories = self.indent.join(
            GoalCategory.objects.all()
            .filter(user=user.user)
            .values_list('title', flat=True)
        )
        self.send_message(
            message.chat.id,
            f'Создание цели:\n'
            f'Ваши категории:\n   {categories}\n'
            f'Введите название категории',
        )
        self.users[message.chat.id] = self.UserState(user, self.create_list)
        return True

    def get_category(self, message: Message, user: TgUser):
        try:
            goal_category = GoalCategory.objects.get(
                title=message.text, user=user.user
            )
        except GoalCategory.DoesNotExist:
            self.send_message(
                message.chat.id, f'Категория "{message.text}" не найдена'
            )
            return None
        self.send_message(
            message.chat.id,
            f'Категория "{message.text}"\n' f'Введите название цели',
        )
        return {"category": goal_category}

    def get_title(self, message: Message, user: TgUser):
        if not message.text:
            self.send_message(message.chat.id, 'Введите название цели')
            return None
        self.send_message(
            message.chat.id, f'Цель "{message.text}"\n' f'Введите описание'
        )
        return {"title": message.text}

    def get_description(self, message: Message, user: TgUser):
        self.send_message(message.chat.id, f'Описание "{message.text}"\n')
        return {"description": message.text}

    class UserState:
        def __init__(self, user: TgUser, steps: list[callable]):
            self.send_message = TgClient().send_message
            self.user = user
            self.steps = iter(steps)
            self.step = next(self.steps)
            self.items = {}

        def __call__(self, *args, **kwargs):
            if item := self.step(*args, **kwargs):
                self.items.update(item)
                try:
                    self.step = next(self.steps)
                except StopIteration:
                    goal = Goal.objects.create(
                        user=self.user.user, **self.items
                    )
                    self.send_message(
                        self.user.chat_id, f'Цель "{goal.title}" создана!'
                    )
                    return True


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FSM = FSM()
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
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=message.chat.id,
            defaults={'username': message.chat.username},
        )
        if created:
            self._bot.send_message(
                message.chat.id, f'Здравствуйте {tg_user.username}!'
            )
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self._bot.send_message(
                message.chat.id,
                f'Ваш код подтверждения: {tg_user.verification_code}',
            )
        else:
            self.handle_auth_user(tg_user, message)

    def handle_auth_user(self, tg_user: TgUser, message: Message):
        if message.text.startswith('/'):
            match message.text:
                case '/goals':
                    text = (
                        Goal.objects.all()
                        .exclude(status=4)
                        .values_list("title", 'due_date', "description")
                    )
                    text = [
                        f'{item[0]}\n{item[1] or "Нет времени"}\n{item[2]}'
                        for item in text
                    ]
                    text = '\n'.join(text)
                    self._bot.send_message(
                        message.chat.id, f'Список целей:\n{text}'
                    )
                case '/create':
                    self.FSM.start_create(message, tg_user)
                case '/cancel':
                    del self.FSM[message.chat.id]
                    self._bot.send_message(
                        message.chat.id, 'Операция отменена'
                    )
        else:
            if not (state := self.FSM[message.chat.id]):
                self._bot.send_message(message.chat.id, f'Лилка')
            else:
                if state(message, tg_user):
                    del self.FSM[message.chat.id]
