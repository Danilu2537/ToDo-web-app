import factory.django
from django.utils import timezone
from pytest_factoryboy import register

from core.models import User
from goals.choices import Role
from goals.models import Board, BoardParticipant, Goal, GoalCategory, GoalComment


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        return User.objects.create_user(*args, **kwargs)


class DatesFactoryMixin:
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


@register
class BoardFactory(factory.django.DjangoModelFactory, DatesFactoryMixin):
    title = factory.Faker('sentence')

    class Meta:
        skip_postgeneration_save = True
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=Role.owner)


@register
class BoardParticipantFactory(factory.django.DjangoModelFactory, DatesFactoryMixin):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


@register
class GoalCategoryFactory(factory.django.DjangoModelFactory, DatesFactoryMixin):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('catch_phrase')

    class Meta:
        model = GoalCategory


@register
class GoalFactory(factory.django.DjangoModelFactory, DatesFactoryMixin):
    category = factory.SubFactory(GoalCategoryFactory)
    title = factory.Faker('catch_phrase')
    description = factory.Faker('text')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Goal


@register
class GoalCommentFactory(factory.django.DjangoModelFactory, DatesFactoryMixin):
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker('text')

    class Meta:
        model = GoalComment
