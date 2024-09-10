from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from student.models import Students, ExamMarksTemplateAdd, UpdateStudent, StudentsStdMultiList, StudentsUpdatesHistory, SchoolStudent  # Import your models
from payment.models import fee_type  # Import your FeeTypes model
from payment.models import Receipt,ReceiptDetail,student_fees
class Command(BaseCommand):
    help = 'Creates StudentPermission, ExamPermission, StudentUpdateYearStd, StudentUpdateHistory, and FeeTypesPermission groups and assigns permissions'

    def handle(self, *args, **options):
        self.create_student_permission_group()
        self.create_exam_permission_group()
        self.create_student_update_year_std_group()
        self.create_fee_types_permission_group()
        self.create_school_student_permission_group()
        self.create_student_update_history_permission_group()
        self.create_payments_permission_group()

    def create_student_permission_group(self):
        group, created = Group.objects.get_or_create(name='StudentPermission')

        custom_permissions = [
            ('can_add_student', 'Can add student'),
            ('can_view_students', 'Can view students'),
            ('can_view_student_details', 'Can view student details'),
            ('can_edit_student', 'Can edit student'),
            ('can_delete_student', 'Can delete student'),
        ]

        content_type = ContentType.objects.get_for_model(Students)

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

        self.stdout.write(self.style.SUCCESS('Successfully set up StudentPermission group and custom permissions'))

    def create_exam_permission_group(self):
        group, created = Group.objects.get_or_create(name='ExamPermission')

        custom_permissions = [
            ('can_view_exam_template', 'Can view exam template'),
            ('can_add_exam_template', 'Can add exam template'),
            ('can_edit_exam_template', 'Can edit exam template'),
            ('can_delete_exam_template', 'Can delete exam template'),
            ('can_assign_exam_marks', 'Can assign exam marks'),
            ('can_view_exam_marks', 'Can view exam marks'),
            ('can_update_exam_marks', 'Can update exam marks'),
        ]

        content_type = ContentType.objects.get_for_model(ExamMarksTemplateAdd)

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

        self.stdout.write(self.style.SUCCESS('Successfully set up ExamPermission group and custom permissions'))

    def create_student_update_year_std_group(self):
        group, created = Group.objects.get_or_create(name='StudentUpdateYearStd')

        custom_permissions = [
            ('can_view_student_update', 'Can view student update'),
            ('can_add_student_update', 'Can add student update'),
            ('can_select_students', 'Can select students'),
            ('can_unselect_students', 'Can unselect students'),
            ('can_view_selected_unselected_students', 'Can view selected and unselected students'),
            ('can_add_year_std_multilist', 'Can add year and standard to multilist'),
        ]

        content_type = ContentType.objects.get_for_model(UpdateStudent)

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

        self.stdout.write(self.style.SUCCESS('Successfully set up StudentUpdateYearStd group and custom permissions'))


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
    
    
    def create_payments_permission_group(self):
        group, created = Group.objects.get_or_create(name='PaymentsPermission')

        # Define custom permissions based on URL patterns
        custom_permissions = [
            ('can_view_payment_list', 'Can view payment list'),
            ('can_view_receipt_details', 'Can view receipt details'),
            ('can_view_payment_details', 'Can view payment details'),
            ('can_delete_payment', 'Can delete payment'),
            ('can_view_student_fees', 'Can view student fees'),
            ('can_collect_payment', 'Can collect payment'),
            ('can_view_students', 'Can view students'),
        ]

        models = [Receipt, ReceiptDetail, student_fees, Students]

        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            for codename, name in custom_permissions:
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    name=name,
                    content_type=content_type,
                )
                group.permissions.add(permission)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created permission: {name} for {model.__name__}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Added existing permission: {name} for {model.__name__}'))

        self.stdout.write(self.style.SUCCESS('Successfully set up PaymentsPermission group and custom permissions'))