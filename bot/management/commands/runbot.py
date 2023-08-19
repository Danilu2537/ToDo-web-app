from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal, GoalCategory

send_message = TgClient().send_message


class FSM:
    """
    Finite State Machine
    """

    def __init__(self):
        self.create_list: list[callable] = [
            self.get_category,
            self.get_title,
            self.get_description,
        ]
        self.users: dict[int, self.UserState] = {}
        self.indent = '\n   '

    def __getitem__(self, item):
        return self.users.get(item)

    def drop(self, id: int):
        del self.users[id]

    def start_create(self, message: Message, user: TgUser):
        categories = self.indent.join(
            GoalCategory.objects.filter(user=user.user).values_list('title', flat=True)
        )
        message_text = (
            'Создание цели:\n'
            f'Ваши категории:\n   {categories}\n'
            'Введите название категории'
        )
        send_message(message.chat.id, message_text)
        self.users[message.chat.id] = self.UserState(user, self.create_list)
        return True

    def get_category(self, message: Message, user: TgUser):
        goal_category = GoalCategory.objects.filter(
            title=message.text, user=user.user
        ).first()
        if not goal_category:
            send_message(message.chat.id, f'Категория "{message.text}" не найдена')
            return None
        send_message(
            message.chat.id, f'Категория "{message.text}"\nВведите название цели'
        )
        return {'category': goal_category}

    def get_title(self, message: Message, user: TgUser):
        if not message.text:
            send_message(message.chat.id, 'Введите название цели')
            return None
        send_message(message.chat.id, f'Цель "{message.text}"')
        send_message(message.chat.id, 'Введите описание')
        return {'title': message.text}

    def get_description(self, message: Message, user: TgUser):
        send_message(message.chat.id, f'Описание "{message.text}"\n')
        return {'description': message.text}

    class UserState:
        """
        User state for FSM
        """

        def __init__(self, user: TgUser, steps: list[callable]):
            self.user = user
            self.items = {}
            self.steps = iter(steps)
            self.step = next(self.steps)

    def __call__(self, *args, **kwargs):
        # Call the step function with the given arguments
        item = self.step(*args, **kwargs)

        # Update the items dictionary with the returned item
        self.items.update(item)

        try:
            # Get the next step function from the steps iterator
            self.step = next(self.steps)
        except StopIteration:
            # Create a new goal object with the user and items
            goal = Goal.objects.create(user=self.user.user, **self.items)

            # Send a message to the user with the created goal's title
            send_message(self.user.chat_id, f'Цель "{goal.title}" создана!')

            # Return True to indicate successful completion
            return True


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bot = TgClient()
        self.FSM = FSM()

    def handle(self, *args, **options):
        # Initialize offset to keep track of the last update ID processed
        offset = 0

        # Print a success message indicating that the bot has started
        self.stdout.write(self.style.SUCCESS('Bot started'))

        # Continue running the bot indefinitely
        while True:
            # Get updates from the bot with the offset and allowed update types
            updates = self._bot.get_updates(offset=offset, allowed_updates=['message'])

            # Process each update
            for update in updates.result:
                # Update the offset to the ID of the next update to be processed
                offset = max(offset, update.update_id + 1)

                # Handle the message contained in the update
                self.handle_message(update.message)

    def handle_message(self, message: Message):
        """
        Handle incoming messages from the user.

        Args:
            message (Message): The incoming message object.

        Returns:
            None
        """
        # Get or create a TgUser object based on the message chat ID
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=message.chat.id, defaults={'username': message.chat.username}
        )

        # If a new user is created, send a welcome message
        if created:
            send_message(message.chat.id, f'Здравствуйте {tg_user.username}!')

        # If the user is not verified, update the verification code and send it to user
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            send_message(
                message.chat.id, f'Ваш код подтверждения: {tg_user.verification_code}'
            )

        # If the user is already verified, handle the authenticated user
        else:
            self.handle_auth_user(tg_user, message)

    def handle_auth_user(self, tg_user: TgUser, message: Message):
        if message.text.startswith('/'):
            match message.text:
                case '/start':
                    send_message(
                        message.chat.id,
                        'Список команд:\n'
                        '  /goals - список целей\n'
                        '  /create - создать цель\n'
                        '  /cancel - отменить операцию',
                    )
                case '/goals':
                    text = (
                        Goal.objects.all()
                        .exclude(status=4)
                        .values_list('title', 'due_date', 'description')
                    )
                    text = [
                        f'{item[0]}\n  '
                        f'{item[1].strftime("%d.%m.%Y") if item[1] else "Нет времени"}'
                        f'\n  {item[2] or "Нет описания"}'
                        for item in text
                    ]
                    text = '\n'.join(text)
                    send_message(message.chat.id, f'Список целей:\n{text}')
                case '/create':
                    self.FSM.start_create(message, tg_user)
                case '/cancel':
                    if self.FSM[message.chat.id]:
                        self.FSM.drop(message.chat.id)
                        send_message(message.chat.id, 'Операция отменена')
                    else:
                        send_message(message.chat.id, 'Нечего отменять')
                case _:
                    send_message(message.chat.id, 'Неизвестная команда')

        else:
            if not (state := self.FSM[message.chat.id]):
                send_message(message.chat.id, 'Напишите команду /create чтобы начать.')
            else:
                if state(message, tg_user):
                    self.FSM.drop(message.chat.id)
