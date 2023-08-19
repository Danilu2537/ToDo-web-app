import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import DateTimeField

from goals.models import Board


@pytest.mark.django_db()
class TestBoardListView:
    url = reverse('goals:list-board')

    def test_auth_requred(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Учетные данные не были предоставлены.'}

    def test_list(self, auth_client, board_participant_factory):
        boards = [
            board_participant.board
            for board_participant in board_participant_factory.create_batch(
                5, user=auth_client.user
            )
        ]
        response = auth_client.get(self.url)
        response_data = sorted(response.json(), key=lambda board: board['id'])
        assert response.status_code == status.HTTP_200_OK
        assert response_data == sorted(
            [_serialize_response(board) for board in boards],
            key=lambda board: board['id'],
        )


def _serialize_response(board):
    return {
        'id': board.id,
        'title': board.title,
        'created': DateTimeField().to_representation(board.created),
        'updated': DateTimeField().to_representation(board.updated),
    }


@pytest.mark.django_db()
class TestBoardCreateView:
    url = reverse('goals:create-board')

    def test_auth_requred(self, client):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Учетные данные не были предоставлены.'}

    def test_no_data(self, auth_client):
        response = auth_client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'title': ['Обязательное поле.']}

    @pytest.mark.usefixtures('board_participant')
    def test_create(self, auth_client):
        data = {'title': 'test'}
        response = auth_client.post(self.url, data=data)
        board = Board.objects.get(title='test')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == _serialize_response(board)


@pytest.mark.django_db()
class TestBoardRetrieveUpdateDestroyView:
    def test_auth_required(self, client, board):
        url = reverse('goals:detail-board', args=(board.id,))
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures('board_participant')
    def test_retrieve_board(self, auth_client, board):
        url = reverse('goals:detail-board', args=(board.id,))
        board.user = auth_client.user
        response = auth_client.get(url)
        response_data = response.json()
        del response_data['participants']
        assert response.status_code == status.HTTP_200_OK
        assert response_data == _serialize_response(board)

    @pytest.mark.usefixtures('board_participant')
    def test_delete_board(self, auth_client, board):
        url = reverse('goals:detail-board', args=(board.id,))
        board.user = auth_client.user
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Board.objects.get(id=board.id).is_deleted is True
