import factory.django


class CreateGoalRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')
