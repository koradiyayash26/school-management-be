# Generated by Django 5.1.3 on 2024-12-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_delete_blockeduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='deleted_by_receiver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='deleted_by_sender',
            field=models.BooleanField(default=False),
        ),
    ]
