from django.apps import AppConfig
from django.core.management import call_command

class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'

    def ready(self):
        # Run the command to ensure the StudentPermission group exists
        # call_command('group')
        pass