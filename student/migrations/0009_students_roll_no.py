# Generated by Django 5.1.3 on 2025-01-15 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_alter_studentupdatestdacademichistory_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='roll_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
