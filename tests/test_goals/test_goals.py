import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import DateTimeField

from goals.choices import Role, Status
from goals.models import Goal
from tests.test_goals.factories import CreateGoalRequest


@pytest.mark.django_db()
class TestCreateGoalView:
    url = reverse('goals:create-goal')

    def test_auth_requred(self, client):
        response = client.post(self.url, data={'title': 'test'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_create_if_not_participant(self, auth_client, goal_category):
        data = CreateGoalRequest.build(category=goal_category.id)
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {'detail': 'Нет доступа к этой категории'}

    def test_failed_to_create_board_if_reader(
        self, auth_client, board_participant, goal_category
    ):
        data = CreateGoalRequest.build(category=goal_category.id)
        board_participant.role = Role.reader
        board_participant.save(update_fields=['role'])
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {'detail': 'Нет доступа к этой категории'}

    @pytest.mark.parametrize('role', [Role.owner, Role.writer], ids=['owner', 'writer'])
    def test_have_create_with_roles(
        self, board_participant, auth_client, goal_category, role
    ):
        data = CreateGoalRequest.build(category=goal_category.id)
        board_participant.role = role
        board_participant.user = auth_client.user
        board_participant.save(update_fields=['role', 'user'])
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        new_goal = Goal.objects.get()
        assert response.json() == _serialize_response(new_goal)

    @pytest.mark.usefixtures('board_participant')
    def test_create_goal_on_deleted_category(self, auth_client, goal_category):
        goal_category.is_deleted = True
        goal_category.save(update_fields=['is_deleted'])
        data = CreateGoalRequest.build(category=goal_category.id)
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'category': ['Категория не найдена']}

    @pytest.mark.usefixtures('board_participant')
    def test_create_goal_on_not_existing_category(self, auth_client, goal_category):
        current_id = goal_category.id + 1
        data = CreateGoalRequest.build(category=current_id)
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'category': [
                f'Недопустимый первичный ключ "{current_id}" - объект не существует.'
            ]
        }


@pytest.mark.django_db()
class TestListGoalView:
    url = reverse('goals:list-goal')

    def test_auth_required(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures('board_participant')
    def test_list_goals(self, auth_client, goal_category, goal_factory):
        goal_category.user = auth_client.user
        goals = goal_factory.create_batch(
            5, category=goal_category, user=auth_client.user
        )

        response = auth_client.get(self.url, category__in=goal_category.id)
        response_data = sorted(response.json(), key=lambda goal: goal.get('id'))
        expected_response_data = sorted(
            [_serialize_response(goal) for goal in goals],
            key=lambda goal: goal.get('id'),
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) == 5
        assert response_data == expected_response_data


@pytest.mark.django_db()
class TestRetrieveUpdateDestroyGoalView:
    def test_auth_required(self, client, goal):
        url = reverse('goals:detail-goal', args=(goal.id,))
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures('board_participant')
    def test_retrieve_goal(self, auth_client, goal):
        url = reverse('goals:detail-goal', args=(goal.id,))
        goal.user = auth_client.user
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.usefixtures('board_participant')
    def test_update_goal(self, auth_client, goal):
        url = reverse('goals:detail-goal', args=(goal.id,))
        goal.user = auth_client.user
        data = {'title': 'new title'}
        response = auth_client.patch(url, data=data)
        data.update(
            updated=DateTimeField().to_representation(
                Goal.objects.get(id=goal.id).updated
            )
        )
        response_data = response.json()
        del response_data['user']
        assert response.status_code == status.HTTP_200_OK
        assert response_data == _serialize_response(goal, **data)

    @pytest.mark.usefixtures('board_participant')
    def test_destroy_goal(self, auth_client, goal):
        url = reverse('goals:detail-goal', args=(goal.id,))
        goal.user = auth_client.user
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Goal.objects.get(id=goal.id).status == Status.archived


def _serialize_response(goal: Goal, **kwargs) -> dict:
    data = {
        'id': goal.id,
        'title': goal.title,
        'category': goal.category_id,
        'description': goal.description,
        'created': DateTimeField().to_representation(goal.created),
        'updated': DateTimeField().to_representation(goal.updated),
        'due_date': DateTimeField().to_representation(goal.due_date),
        'status': goal.status,
        'priority': goal.priority,
    }
    return data | kwargs
