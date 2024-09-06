from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from payment.models import fee_type
from student.models import SchoolStudent  # Import your SchoolStudent model

class Command(BaseCommand):
    help = 'Creates FeeTypesPermission, FeeStudentPermission groups and assigns custom permissions'

    def handle(self, *args, **options):
        self.create_fee_types_permission_group()
        self.create_fee_student_permission_group()

    def create_fee_types_permission_group(self):
        group, created = Group.objects.get_or_create(name='FeeTypesPermission')

        # Define custom permissions based on URL patterns
        custom_permissions = [
            ('can_add_fee_type', 'Can add fee type'),
            ('can_view_fee_types', 'Can view fee types'),
            ('can_view_fee_type_details', 'Can view fee type details'),
            ('can_edit_fee_type', 'Can edit fee type'),
            ('can_delete_fee_type', 'Can delete fee type'),
            ('can_view_fee_type_add_details', 'Can view fee type add details'),
            ('can_assign_student_fee', 'Can assign student fee'),
            ('can_update_student_fee_types', 'Can update student fee types'),  # New permission
        ]

        content_type = ContentType.objects.get_for_model(fee_type)

        for codename, name in custom_permissions:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type,
            )
            group.permissions.add(permission)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created permission: {name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Added existing permission: {name}'))

        self.stdout.write(self.style.SUCCESS('Successfully set up FeeTypesPermission group and custom permissions'))

    def create_fee_student_permission_group(self):
        group, created = Group.objects.get_or_create(name='FeeStudentPermission')

        # Define custom permissions based on URL patterns
        custom_permissions = [
            ('can_view_school_students', 'Can view school students'),
            ('can_view_school_student_details', 'Can view school student details'),
            ('can_view_school_student_names', 'Can view school student names'),
            ('can_add_school_student', 'Can add school student'),
            ('can_edit_school_student', 'Can edit school student'),
        ]

        content_type = ContentType.objects.get_for_model(SchoolStudent)

        for codename, name in custom_permissions:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type,
            )
            group.permissions.add(permission)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created permission: {name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Added existing permission: {name}'))

        self.stdout.write(self.style.SUCCESS('Successfully set up FeeStudentPermission group and custom permissions'))