# Generated by Django 4.2.3 on 2023-07-24 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0008_alter_goalcategory_board'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardparticipant',
            name='title',
        ),
    ]
