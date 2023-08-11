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
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')
        fields = '__all__'


class BoardWithParticipantsSerializer(BoardSerializer):
    participants = ParticipantSerializer(many=True)

    def update(self, instance: Board, validated_data: dict):
        owner = self.context['request'].user
        new_participants = validated_data.pop('participants')
        new_by_id = {part['user'].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                        old_participant.role
                        != new_by_id[old_participant.user_id]['role']
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            'role'
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part['user'], role=new_part['role']
                )

            instance.title = validated_data['title']
            instance.save()

        return instance


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_board(self, board: Board) -> Board:
        if board.is_deleted:
            raise serializers.ValidationError('Доска не найдена')
        if not BoardParticipant.objects.filter(
            board=board,
            user=self.context['request'].user,
            role__in=[Role.owner, Role.writer],
        ).exists():
            raise PermissionDenied('Нет доступа к этой категории')
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
        if category.is_deleted:
            raise serializers.ValidationError('Категория не найдена')
        if not BoardParticipant.objects.filter(
            board=category.board,
            user=self.context['request'].user,
            role__in=[Role.owner, Role.writer],
        ).exists():
            raise PermissionDenied('Нет доступа к этой категории')
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


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, goal: Goal) -> Goal:
        if goal.status == Status.archived:
            raise NotFound('Доска не найдена')
        if not BoardParticipant.objects.filter(
            board=goal.category.board,
            user=self.context['request'].user,
            role__in=[Role.owner, Role.writer],
        ).exists():
            raise PermissionDenied('Нет доступа к этой категории')
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
