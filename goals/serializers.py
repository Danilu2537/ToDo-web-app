from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied

from core.models import User
from core.serializers import ProfileSerializer
from goals.choices import Role, Status
from goals.models import Board, BoardParticipant, Goal, GoalCategory, GoalComment


class ParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=BoardParticipant.editable_roles)
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        exclude = ('is_deleted',)
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated')
        exclude = ('is_deleted',)


class BoardWithParticipantsSerializer(BoardSerializer):
    participants = ParticipantSerializer(many=True)

    def update(self, instance: Board, validated_data: dict):
        # Get the owner of the board
        owner = self.context['request'].user

        # Get the new participants from the validated data
        new_participants = validated_data.pop('participants')

        # Create a dictionary with the new participants mapped by user id
        new_by_id = {part['user'].id: part for part in new_participants}

        # Get the old participants excluding the owner
        old_participants = instance.participants.exclude(user=owner)

        with transaction.atomic():
            # Loop through the old participants
            for old_participant in old_participants:
                # If the old participant is not in the new participants, delete it
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    # If the role of the old participant is different from the new role,
                    # update the role
                    if (
                        old_participant.role
                        != new_by_id[old_participant.user_id]['role']
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            'role'
                        ]
                        old_participant.save()

                    # Remove the old participant from the new_by_id dictionary
                    new_by_id.pop(old_participant.user_id)

            # Create new board participants for the remaining participants in new_by_id
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part['user'], role=new_part['role']
                )

            # Update the title of the board
            instance.title = validated_data['title']
            instance.save()

        return instance


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_board(self, board: Board) -> Board:
        """
        Function to validate the board.

        Args:
            board (Board): The board object to be validated.

        Returns:
            Board: The validated board object.

        Raises:
            serializers.ValidationError: If the board is deleted.
            PermissionDenied: If the user does not have access to the board.
        """

        # Check if the board is deleted
        if board.is_deleted:
            raise serializers.ValidationError('Доска не найдена')

        # Check if the user has access to the board
        if not BoardParticipant.objects.filter(
            board=board,
            user=self.context['request'].user,
            role__in=[Role.owner, Role.writer],
        ).exists():
            raise PermissionDenied('Нет доступа к этой категории')

        # Return the validated board
        return board

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCategorySerializer(GoalCategoryCreateSerializer):
    user = ProfileSerializer(read_only=True)


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, category: GoalCategory) -> GoalCategory:
        """
        Validates the given category object.

        Args:
            category (GoalCategory): The category object to validate.

        Returns:
            GoalCategory: The validated category object.

        Raises:
            serializers.ValidationError: If the category is deleted.
            PermissionDenied: If the current user does not have access to the category.
        """

        # Check if the category is deleted
        if category.is_deleted:
            raise serializers.ValidationError('Категория не найдена')

        # Check if the current user has access to the category
        if not BoardParticipant.objects.filter(
            board=category.board,
            user=self.context['request'].user,
            role__in=[Role.owner, Role.writer],
        ).exists():
            raise PermissionDenied('Нет доступа к этой категории')

        # Return the validated category object
        return category

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        exclude = ('user',)


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, goal: Goal) -> Goal:
        """
        Validates the given goal and performs necessary checks.

        Args:
            goal (Goal): The goal to validate.

        Returns:
            Goal: The validated goal.

        Raises:
            NotFound: If the goal's status is archived.
            PermissionDenied: If the user doesn't have access to the category board.
        """
        # Check if the goal's status is archived
        if goal.status == Status.archived:
            raise NotFound('Доска не найдена')

        # Check if the user has access to the category board
        board_participant_exists = BoardParticipant.objects.filter(
            board=goal.category.board,
            user=self.context['request'].user,
            role__in=[Role.owner, Role.writer],
        ).exists()

        if not board_participant_exists:
            raise PermissionDenied('Нет доступа к этой категории')

        # Return the validated goal
        return goal

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')
        fields = '__all__'
