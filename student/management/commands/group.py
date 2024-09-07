from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from student.models import Students, ExamMarksTemplateAdd, UpdateStudent, StudentsStdMultiList, StudentsUpdatesHistory, SchoolStudent  # Import your models
from payment.models import fee_type  # Import your FeeTypes model

class Command(BaseCommand):
    help = 'Creates StudentPermission, ExamPermission, StudentUpdateYearStd, StudentUpdateHistory, and FeeTypesPermission groups and assigns permissions'

    def handle(self, *args, **options):
        self.create_student_permission_group()
        self.create_exam_permission_group()
        self.create_student_update_year_std_group()
        self.create_fee_types_permission_group()
        self.create_school_student_permission_group()
        self.create_student_update_history_permission_group()

    def create_student_permission_group(self):
        group, created = Group.objects.get_or_create(name='StudentPermission')

        permissions = [
            'add_students',
            'view_students',
            'change_students',
            'delete_students',
        ]

        content_type = ContentType.objects.get_for_model(Students)

        for permission_codename in permissions:
            permission = Permission.objects.get(
                codename=permission_codename,
                content_type=content_type,
            )
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully set up StudentPermission group and permissions'))

    def create_exam_permission_group(self):
        group, created = Group.objects.get_or_create(name='ExamPermission')

        permissions = [
            'add_exammarkstemplateadd',
            'view_exammarkstemplateadd',
            'change_exammarkstemplateadd',
            'delete_exammarkstemplateadd',
        ]

        content_type = ContentType.objects.get_for_model(ExamMarksTemplateAdd)

        for permission_codename in permissions:
            permission = Permission.objects.get(
                codename=permission_codename,
                content_type=content_type,
            )
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully set up ExamPermission group and permissions'))

    def create_student_update_year_std_group(self):
        group, created = Group.objects.get_or_create(name='StudentUpdateYearStd')

        permissions = [
            'view_updatestudent',
            'add_updatestudent',
            'change_updatestudent',
            'delete_updatestudent',
            'view_studentsstdmultilist',
            'add_studentsstdmultilist',
            'change_studentsstdmultilist',
            'delete_studentsstdmultilist',
        ]

        content_types = [
            ContentType.objects.get_for_model(UpdateStudent),
            ContentType.objects.get_for_model(StudentsStdMultiList),
        ]

        for content_type in content_types:
            for permission_codename in permissions:
                try:
                    permission = Permission.objects.get(
                        codename=permission_codename,
                        content_type=content_type,
                    )
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permission {permission_codename} does not exist for {content_type.model}'))

        self.stdout.write(self.style.SUCCESS('Successfully set up StudentUpdateYearStd group and permissions'))

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
    
    
    
    def create_school_student_permission_group(self):
        group, created = Group.objects.get_or_create(name='SchoolStudentPermission')

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
                
   
    def create_student_update_history_permission_group(self):
        group, created = Group.objects.get_or_create(name='StudentUpdateHistoryPermission')

        # Define custom permissions based on URL patterns
        custom_permissions = [
            ('can_view_student_update_history', 'Can view student update history'),
            ('can_delete_student_update_history', 'Can delete student update history'),
        ]

        content_type = ContentType.objects.get_for_model(StudentsUpdatesHistory)

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

        self.stdout.write(self.style.SUCCESS('Successfully set up StudentUpdateHistoryPermission group and custom permissions'))             