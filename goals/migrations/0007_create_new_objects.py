# Generated by Django 4.2.3 on 2023-07-24 19:29

from django.db import migrations, transaction
from django.utils import timezone


def create_new_objects(apps, schema_editor) -> None:
    User = apps.get_model('core', 'User')
    Board = apps.get_model('goals', 'Board')
    BoardParticipant = apps.get_model('goals', 'BoardParticipant')
    GoalCategory = apps.get_model('goals', 'GoalCategory')
    now = timezone.now()

    with transaction.atomic():
        for user in User.objects.all():
            new_board = Board.objects.create(title='Мои цели', created=now, updated=now)
            BoardParticipant.objects.create(board=new_board, user=user, role=1, created=now, updated=now)
            GoalCategory.objects.filter(user=user).update(board=new_board)


class Migration(migrations.Migration):
    dependencies = [
        ('goals', '0006_board_alter_goal_description_goalcategory_board_and_more'),
    ]

    operations = [
        migrations.RunPython(create_new_objects, migrations.RunPython.noop),
    ]
