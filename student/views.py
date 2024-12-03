from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
import json
import datetime
from datetime import datetime
from datetime import datetime

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,BasePermission

from .models import Students,UpdateStudent,StudentsStdMultiList,StudentsUpdatesHistory,ExamMarksTemplateAdd,ExamMarkAssingData
from .serializers import StudentsSerializer,StudentUpdateHistoricalSerializer,StudentUpdateStdYearSerializer,StudentUpdatedSerializer,ExamMarksTemplateAddSerializer,ExamMarksAssignSerializer,ExamMarkAssingDataSerializer

from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group,Permission
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

# single user get api of each permiton
from django.contrib.auth.models import User, Group, Permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

import pandas as pd

from io import BytesIO

from django.utils.timezone import make_naive, get_default_timezone
from datetime import date

from django.http import HttpResponse

from standard.models import AcademicYear,standard_master

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db import models  # Add this import
import pandas as pd
import re

class UserPermissionsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get user's permissions (both from groups and direct assignments)
        user_permissions = user.user_permissions.all() | Permission.objects.filter(group__user=user)
        user_permission_ids = set(user_permissions.values_list('id', flat=True))

        # Get all groups and their permissions
        groups = Group.objects.all()
        group_permissions = []

        for group in groups:
            group_perms = group.permissions.all()
            if group_perms:  # Only include groups with permissions
                group_data = {
                    'id': group.id,
                    'name': group.name,
                    'permissions': [
                        {
                            'id': perm.id,
                            'name': perm.name,
                            'assigned': perm.id in user_permission_ids
                        }
                        for perm in group_perms
                    ]
                }
                group_permissions.append(group_data)

        return Response({
            "user_permissions": group_permissions
        }, status=status.HTTP_200_OK)

# assing each permiton api of user
class AssignPermissionsToUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        permission_ids = request.data.get('permissions', [])
        print(permission_ids,user)
        
        if not isinstance(permission_ids, list):
            return Response({"error": "permissions must be a list of IDs"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            permissions = Permission.objects.filter(id__in=permission_ids)
            user.user_permissions.set(permissions)
        except ValueError:
            return Response({"error": "Invalid permission IDs"}, status=status.HTTP_400_BAD_REQUEST)

        # Get updated permissions
        updated_permissions = user.get_all_permissions()

        return Response({
            "message": f"Permissions assigned to user {user.username}",
            "user_permissions": list(updated_permissions),
        }, status=status.HTTP_200_OK)


#  group permiton get api for single user
class GroupListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        all_groups = Group.objects.all()
        user_groups = user.groups.all()

        group_data = [
            {
                'id': group.id,
                'name': group.name,
                'assigned': group in user_groups
            }
            for group in all_groups
        ]

        return Response(group_data)


# user group permition assing api 
class AssignGroupsToUserAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        group_ids = request.data.get('group_ids', [])
        
        if not isinstance(group_ids, list):
            return Response({"error": "group_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        user.groups.clear()  # Remove all existing groups
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.add(*groups)

        # Get updated group information
        all_groups = Group.objects.all()
        user_groups = user.groups.all()

        group_data = [
            {
                'id': group.id,
                'name': group.name,
                'assigned': group in user_groups
            }
            for group in all_groups
        ]

        return Response({
            "message": f"Groups assigned to user {user.username}",
            "groups": group_data
        }, status=status.HTTP_200_OK)

class UserCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        
        if role:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class ChangePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, user_id):
        # Check if the authenticated user is an admin
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to change other users' passwords.")
        
        user = get_object_or_404(User, id=user_id)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        print(f"Changing password for user ID: {user_id}")
        print(f"Old password: {old_password}, New password: {new_password}")

        if not old_password or not new_password:
            return Response({'error': 'Both old and new passwords are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': f'Password changed successfully for user {user.username}'}, status=status.HTTP_200_OK)

class UserDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request, user_id=None):
        if user_id is None:
            # If no user_id is provided, return the authenticated user's details
            user = request.user
        else:
            # If a user_id is provided, check if the authenticated user is an admin
            if not request.user.is_staff:
                raise PermissionDenied("You do not have permission to view other users' details.")
            user = get_object_or_404(User, id=user_id)

        last_login = user.last_login.isoformat() if user.last_login else None
        groups = user.groups.values_list('name', flat=True)

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'last_login': last_login,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined.isoformat(),
            'roles': list(groups),
        }
        return Response(data, status=status.HTTP_200_OK)


class UserListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]  # Restrict to admin users


    def get(self, request):
        users = User.objects.all()
        user_data = []
        for user in users:
            last_login = user.last_login.isoformat() if user.last_login else None
            groups = user.groups.values_list('name', flat=True)
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_login': last_login,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined.isoformat(),
                'roles': list(groups),
            })
        return Response(user_data, status=status.HTTP_200_OK)

class UserDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]  # Restrict to admin users

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Prevent deleting the current user
        if user == request.user:
            return Response({"error": "You cannot delete your own account."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Optional: Add any additional checks or logging here
        
        user.delete()
        return Response({"message": f"User {user.username} has been deleted."}, status=status.HTTP_200_OK)


# import for bulk-impor for gr
def convert_to_string(value):
    if isinstance(value, (int, float)):
        return str(int(value))
    elif isinstance(value, str):
        return re.sub(r'[^\d]', '', value)
    return value

@method_decorator(csrf_exempt, name='dispatch')
class BulkImportStudent(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        # Get current academic year
        current_academic_year = AcademicYear.objects.filter(is_current=True).first()
        if not current_academic_year:
            return Response({"error": "No current academic year set"}, status=400)

        df = pd.read_excel(file, engine='openpyxl')
        df = df.where(pd.notnull(df), None)
        
        students_to_create = []
        students_to_update = []
        errors = []

        def parse_date(date_string):
            if pd.isna(date_string) or date_string is None:
                return None
            if isinstance(date_string, (date, datetime)):
                return date_string
            try:
                return datetime.strptime(str(date_string), "%Y-%m-%d").date()
            except ValueError:
                return None

        required_fields = [f.name for f in Students._meta.fields if not f.blank and not f.null and f.name not in ['id', 'created_at', 'updated_at', 'academic_year']]
        excel_fields = set(df.columns)

        # Check if all required fields are in the Excel file
        missing_fields = set(required_fields) - excel_fields
        if missing_fields:
            return Response({"error": f"Missing required fields in Excel: {', '.join(missing_fields)}"}, status=400)

        with transaction.atomic():
            for index, row in df.iterrows():
                if row.isnull().all():
                    break  # Stop processing if we encounter an empty row

                try:
                    student_data = {}
                    record_errors = []

                    # Handle academic year
                    academic_year_value = row.get('Academic_Year')
                    if academic_year_value and not pd.isna(academic_year_value):
                        try:
                            academic_year = AcademicYear.objects.get(year=academic_year_value)
                            student_data['academic_year'] = academic_year
                        except AcademicYear.DoesNotExist:
                            record_errors.append(f"Invalid academic year: {academic_year_value}")
                    else:
                        # Use current academic year if not specified
                        student_data['academic_year'] = current_academic_year

                    # Check if the required fields are present and not empty
                    for field in required_fields:
                        value = row.get(field)
                        if value is None or pd.isna(value) or (isinstance(value, str) and value.strip() == ''):
                            record_errors.append(f"Missing required field: {field}")

                    # If there are errors in required fields, skip this row
                    if record_errors:
                        errors.append({
                            "grno": row.get('grno', f"Row {index + 2}"),
                            "errors": record_errors
                        })
                        continue

                    for field in Students._meta.fields:
                        if field.name in ['id', 'created_at', 'updated_at', 'academic_year']:
                            continue
                        
                        value = row.get(field.name)
                        
                        if value is None or pd.isna(value):
                            if field.has_default():
                                value = field.get_default()
                            elif not field.blank and not field.null:
                                record_errors.append(f"Missing required field: {field.name}")
                                continue
                            else:
                                continue  # Skip non-required fields with no value
                        
                        if isinstance(field, models.DateField):
                            value = parse_date(value)
                            if value is None and field.name in required_fields:
                                record_errors.append(f"Invalid date for {field.name}")
                        elif isinstance(field, models.IntegerField):
                            try:
                                value = int(value)
                            except (ValueError, TypeError):
                                if field.name in required_fields:
                                    record_errors.append(f"Invalid integer for {field.name}")
                                value = None
                        elif field.name in ['udise_no', 'aadhar_no']:
                            value = convert_to_string(value)
                        
                        student_data[field.name] = value

                    if record_errors:
                        errors.append({
                            "grno": student_data.get('grno', f"Row {index + 2}"),
                            "errors": record_errors
                        })
                        continue

                    # Check for existing student by ID, GRNO, or name combination
                    existing_student = None
                    if 'id' in row and not pd.isna(row['id']):
                        existing_student = Students.objects.filter(id=row['id']).first()
                    if not existing_student:
                        existing_student = Students.objects.filter(
                            grno=student_data['grno'],
                            academic_year=student_data['academic_year']
                        ).first()
                    if not existing_student:
                        existing_student = Students.objects.filter(
                            first_name=student_data['first_name'],
                            last_name=student_data['last_name'],
                            academic_year=student_data['academic_year']
                        ).first()

                    if existing_student:
                        # Update existing record
                        for key, value in student_data.items():
                            setattr(existing_student, key, value)
                        students_to_update.append(existing_student)
                    else:
                        # Create new record
                        student = Students(**student_data)
                        students_to_create.append(student)

                except Exception as e:
                    errors.append({
                        "grno": student_data.get('grno', f"Row {index + 2}"),
                        "errors": [f"Unexpected error: {str(e)}"]
                    })

            if errors:
                return Response({"errors": errors}, status=400)

            try:
                # Bulk create new records
                Students.objects.bulk_create(students_to_create)
                
                # Bulk update existing records
                if students_to_update:
                    Students.objects.bulk_update(
                        students_to_update,
                        fields=[f.name for f in Students._meta.fields if f.name not in ['id', 'created_at', 'updated_at']]
                    )
                
                return Response({
                    "message": f"Successfully imported {len(students_to_create)} new records and updated {len(students_to_update)} existing records.",
                    "created": len(students_to_create),
                    "updated": len(students_to_update)
                }, status=200)
            except IntegrityError as e:
                return Response({"error": f"Database integrity error: {str(e)}"}, status=400)
            except Exception as e:
                return Response({"error": f"Unexpected error: {str(e)}"}, status=500)


# Export of Excel file for gr
class ExportGeneralRegisterToExcel(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Get school_type from query parameters
            school_type = request.GET.get('school_type')
            
            current_academic_year = AcademicYear.objects.filter(is_current=True).first()
            if not current_academic_year:
                return Response({"error": "No current academic year set"}, status=400)
            
            # Start with base queryset
            queryset = Students.objects.filter(
                academic_year=current_academic_year
            ).select_related('academic_year')
            
            # Filter by school_type if provided
            if school_type:
                queryset = queryset.filter(
                    standard__in=standard_master.objects.filter(
                        school_type=school_type,
                        is_active=True
                    ).values_list('name', flat=True)
                )
            
            # Modify the values query to include academic year
            data = list(queryset.values(
                'id',
                'grno',
                'first_name',
                'last_name',
                'middle_name',
                'mother_name',
                'gender',
                'birth_date',
                'birth_place',
                'mobile_no',
                'address',
                'city',
                'district',
                'standard',
                'section',
                'academic_year__year',  # Include academic year
                'last_school',
                'admission_std',
                'admission_date',
                'left_school_std',
                'left_school_date',
                'religion',
                'category',
                'caste',
                'udise_no',
                'aadhar_no',
                'account_no',
                'name_on_passbook',
                'bank_name',
                'ifsc_code',
                'bank_address',
                'reason',
                'note',
                'assesment',
                'progress',
                'status'
            ))

            def convert_to_naive(value):
                if isinstance(value, datetime):
                    return make_naive(value, get_default_timezone())
                elif isinstance(value, date):
                    return value
                return value

            # Process the data
            for item in data:
                # Remove unwanted fields
                for field in ['student_img', 'created_at', 'updated_at']:
                    item.pop(field, None)
                
                # Convert dates
                for field in ['birth_date', 'admission_date', 'left_school_date']:
                    if item.get(field) is not None:
                        item[field] = convert_to_naive(item[field])
                
                # Rename academic_year__year to academic_year for better column header
                if 'academic_year__year' in item:
                    item['academic_Year'] = item.pop('academic_year__year')

            df = pd.DataFrame(data)
                        
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                sheet_name = f'General Register ({current_academic_year.year})'
                if school_type:
                    sheet_name = f'{school_type} {sheet_name}'
                df.to_excel(
                    writer, 
                    index=False, 
                    sheet_name=sheet_name
                )

            filename = f'general_register_{current_academic_year.year}'
            if school_type:
                filename = f'{school_type.lower()}_{filename}'
            
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
            response.write(output.getvalue())

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=500)



# permission for student for group
class HasStudentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(f'student.{view.required_permission}')

class StudentAdd(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentPermission]
    required_permission = 'can_add_student'
    
    def post(self, request):
        try:
            data = request.data.copy()
            
            # Handle the image field
            if 'student_img' in request.FILES:
                data['student_img'] = request.FILES['student_img']
            elif 'student_img' in data:
                if data['student_img'] == 'null' or data['student_img'] == '':
                    data['student_img'] = None
            
            serializer = StudentsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# all students get api

class StudentGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentPermission]
    required_permission = 'can_view_students'

    def get(self, request):
        # Get query parameters
        school_type = request.GET.get('school_type')
        
        # Get current academic year
        current_academic_year = AcademicYear.objects.filter(is_current=True).first()
        
        # Start with base queryset
        queryset = Students.objects.filter(academic_year=current_academic_year)
        
        # If school_type is provided, filter students based on their standard's school_type
        if school_type:
            queryset = queryset.filter(
                standard__in=standard_master.objects.filter(
                    school_type=school_type,
                    is_active=True
                ).values_list('name', flat=True)
            )

        # Get values list data
        students = queryset.values(
            'id',
            'grno',
            'student_img',
            'last_name',
            'first_name',
            'middle_name',
            'mother_name',
            'gender',
            'birth_date',
            'birth_place',
            'mobile_no',
            'address',
            'city',
            'district',
            'standard',
            'section',
            'academic_year__year', 
            'last_school',
            'admission_std',
            'admission_date',
            'left_school_std',
            'left_school_date',
            'religion',
            'category',
            'caste',
            'udise_no',
            'aadhar_no',
            'account_no',
            'name_on_passbook',
            'bank_name',
            'ifsc_code',
            'bank_address',
            'reason',
            'note',
            'assesment',
            'progress',
            'status'
        ).order_by('id')
        
        return JsonResponse({
            "message": "Students Get Successfully", 
            "data": list(students),
        }, status=200)
         
# permission for student update history for Group
class HasStudentUpdateHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(f'student.{view.required_permission}')

# Student uppdate historical get api

class StudentUpdateHistoricalGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdateHistoryPermission]  # Required for DjangoModelPermissions
    required_permission = 'can_view_student_update_history'


    def get(self, request):
        
        students = StudentsUpdatesHistory.objects.all()
        serialized_data = StudentUpdateHistoricalSerializer(students, many=True)
        return JsonResponse({"message": "Student Update Historical Get Successfully", "data": serialized_data.data}, status=200)

# Student uppdate historical Delete api

class StudentUpdateHistoricalDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdateHistoryPermission]  # Required for DjangoModelPermissions
    required_permission = 'can_delete_student_update_history'

    
    def delete(self, request, pk):
        try:
            student = StudentsUpdatesHistory.objects.get(pk=pk)
        except StudentsUpdatesHistory.DoesNotExist:
            return JsonResponse({"message": "Student Update Historical not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        student.delete()
        return JsonResponse({"message": "Student Update Historical deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    
# Single student get api by id

class StudentGetId(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentPermission]
    required_permission = 'can_view_student_details'

    def get(self, request, pk):
        try:
            student = Students.objects.get(pk=pk)
            serialized_data = StudentsSerializer(student)
            return JsonResponse({"message": "Student retrieved successfully", "data": serialized_data.data}, status=200)
        except Students.DoesNotExist:
            return JsonResponse({"message": "Student not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=500)


# update api for student

class StudentUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentPermission]
    required_permission = 'can_edit_student'

    def patch(self, request, pk):
        try:
            student = Students.objects.get(pk=pk)
            data = request.data.copy()
            
            # Handle the image field
            if 'student_img' in request.FILES:
                # New image uploaded - delete old image if exists
                if student.student_img:
                    student.student_img.delete(save=False)
                data['student_img'] = request.FILES['student_img']
            elif 'student_img' in data:
                if data['student_img'] == 'null' or data['student_img'] == '':
                    # User wants to remove the image
                    if student.student_img:
                        student.student_img.delete(save=False)
                    data['student_img'] = None
                else:
                    # No new image uploaded - keep existing image
                    data.pop('student_img')
            
            serializer = StudentsSerializer(student, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Students.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# update for student api

class StudentDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentPermission]
    required_permission = 'can_delete_student'

    def delete(self, request, pk):
        try:
            student = Students.objects.get(pk=pk)
            student.delete()
            return JsonResponse({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Students.DoesNotExist:
            return JsonResponse({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            
            
# permission for student update year and std for group
class HasStudentUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(f'student.{view.required_permission}')                        
# student update year and std get api of template

class StudentUpdateStdYearGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdatePermission]
    required_permission = 'can_view_student_update'
    def get(self, request):
        
        template = UpdateStudent.objects.all()
        serialized_data = StudentUpdateStdYearSerializer(template, many=True)
        return JsonResponse({"message": "Students Standard And Year Template Get Successfully", "data": serialized_data.data}, status=200)

# student update year and std Post api of template

class StudentUpdateStdYearPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdatePermission]
    required_permission = 'can_add_student_update'

    def post(self, request):
        serializer = StudentUpdateStdYearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Student update template created successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# post API for add students on StudentsStdMultilist
class StudentsAddYearAndstdFromurl(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdatePermission]
    required_permission = 'can_add_year_std_multilist'

    def post(self, request):
        data = request.data
        standard = data.get('standard')
        year = data.get('year')

        if standard is None or year is None:
            return JsonResponse({'error': 'Both standard and year are required'}, status=status.HTTP_400_BAD_REQUEST)
        # Perform filtering on the Student model
        filtered_students = Students.objects.filter(standard=standard, admission_date=year)

        for student in filtered_students:
            # Check if a record with the same grno already exists
            existing_record = StudentsStdMultiList.objects.filter(grno=student.grno).exists()

            if not existing_record:
                # Insert new record if it doesn't already exist
                StudentsStdMultiList.objects.create(
                    grno=student.grno,
                    first_name=student.first_name,
                    last_name=student.last_name,
                    standard=student.standard,
                    year=student.admission_date
                )

        return JsonResponse({'message': 'Filtered students updated successfully'}, status=status.HTTP_200_OK)


# get api for seleted or not seleted

class StudentSletedOrNotSeletedGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdatePermission]
    required_permission = 'can_view_selected_unselected_students'


    def get(self, request, standard, year):
        # Check if records exist in StudentsStdMultiList for the provided standard and year
        existing_records = StudentsStdMultiList.objects.filter(standard=standard, year=year)
        
        if not existing_records.exists():
            # Retrieve data from the Students model if no records exist in StudentsStdMultiList
            students_data = Students.objects.filter(standard=standard, admission_date=year)
            if students_data.exists():
                # Create new records in StudentsStdMultiList for each student
                for student in students_data:
                    StudentsStdMultiList.objects.create(
                        grno=student.grno,
                        first_name=student.first_name,
                        last_name=student.last_name,
                        standard=student.standard,
                        year=student.admission_date
                    )
            else:
                return JsonResponse({'error': 'Student Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Serialize the data
            serialized_data = StudentUpdatedSerializer(students_data, many=True)
            
            # Return the serialized data in the response
            return JsonResponse({"message": "Students added to StudentsStdMultiList successfully", "data": serialized_data.data}, status=200)
        
        # Remove duplicates based on grno, year, and standard, keeping only one
        duplicates = (
            StudentsStdMultiList.objects
            .values('grno', 'year', 'standard')
            .annotate(count=Count('id'))
            .order_by()
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            grno = duplicate['grno']
            year = duplicate['year']
            standard = duplicate['standard']
            
            entries = StudentsStdMultiList.objects.filter(grno=grno, year=year, standard=standard)
            
            # Keep the first entry and delete the rest
            for entry in entries[1:]:
                entry.delete()

        # If records already exist in StudentsStdMultiList, return them
        serialized_data = StudentUpdatedSerializer(existing_records, many=True)
        return JsonResponse({"message": "Students retrieved from StudentsStdMultiList successfully", "data": serialized_data.data}, status=200)


class StudentsSelectedPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdatePermission]
    required_permission = 'can_select_students'


    def post(self, request):
        data = json.loads(request.body)
        selected_grnos = data.get('selectedGRNOs', [])
        print(selected_grnos)
        now = datetime.now()
        week_name = now.strftime('%a')
        formatted_date_time = now.strftime('%Y-%m-%d %H:%M')
        date_time_with_week_name = f"{formatted_date_time} {week_name}"

        for grno in selected_grnos:
            student_list = StudentsStdMultiList.objects.filter(grno=grno)
            students = Students.objects.filter(grno=grno)

            for student in student_list:
                for student1 in students:
                    if student1.admission_date == student.year and student.standard == "13":
                        existing_record = StudentsUpdatesHistory.objects.filter(
                            name=student1.first_name,
                            year=student1.admission_date,
                            standard=student1.standard
                        ).first()
                        if existing_record:
                            existing_record.note = student1.note
                            existing_record.update_date = date_time_with_week_name
                            existing_record.save()
                        else:
                            StudentsUpdatesHistory.objects.create(
                                name=student1.first_name,
                                year=student1.admission_date,
                                standard=student1.standard,
                                note=student1.note,
                                update_date=date_time_with_week_name,
                            )
                        student.is_active = True
                        student.save()
                        student1.standard = 1
                        student1.admission_date = int(student1.admission_date) + 1
                        student1.save()
                    else:
                        if student1.admission_date == student.year and student1.standard == student.standard:
                            if not student.is_active:
                                existing_record = StudentsUpdatesHistory.objects.filter(
                                    name=student1.first_name,
                                    year=student1.admission_date,
                                    standard=student1.standard
                                ).first()
                                if existing_record:
                                    existing_record.note = student1.note
                                    existing_record.update_date = date_time_with_week_name
                                    existing_record.save()
                                else:
                                    StudentsUpdatesHistory.objects.create(
                                        name=student1.first_name,
                                        year=student1.admission_date,
                                        standard=student1.standard,
                                        note=student1.note,
                                        update_date=date_time_with_week_name,
                                    )
                            student.is_active = True
                            student.save()
                            student1.standard = int(student1.standard) + 1
                            student1.admission_date = int(student1.admission_date) + 1
                            student1.save()

        return JsonResponse({'message': 'Selected students updated successfully'}, status=200)


# post api for UnSeleted STudent 
class StudentsUnselectedPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasStudentUpdatePermission]
    required_permission = 'can_unselect_students'


    def post(self, request):
        data = json.loads(request.body)
        unselected_grnos = data.get('selectedGRNOs', [])
        # print(unselected_grnos,"Reupdate")
        for grno in unselected_grnos:
            
            student1 = Students.objects.get(grno=grno)
            if student1.standard == "1":
                print("1 yes")
                student = StudentsStdMultiList.objects.get(grno=grno,year=int(student1.admission_date)-1,standard=13)
                
                print(student.year,"oky")
                StudentsStdMultiList.objects.filter(grno=student.grno, year__gt=student.year,standard__gt=student.standard).delete()
                
                if  student.is_active == True:
                    now = datetime.now()
                    week_name = now.strftime('%a')
                    formatted_date_time = now.strftime('%Y-%m-%d %H:%M')
                    date_time_with_week_name = f"{formatted_date_time} {week_name}"
                    existing_record = StudentsUpdatesHistory.objects.filter(
                    name=student1.first_name,
                    year=student1.admission_date,
                    standard=student1.standard
                    ).first()
                    if existing_record:
                        # Update existing record
                        existing_record.note = student1.note
                        existing_record.update_date = date_time_with_week_name
                        existing_record.save()
                    else:
                        # Create new record
                        StudentsUpdatesHistory.objects.create(
                            name=student1.first_name,
                            year=student1.admission_date,
                            standard=student1.standard,
                            note=student1.note,
                            update_date=date_time_with_week_name,
                        )
                student1.standard = 13
                student1.admission_date = int(student1.admission_date) - 1
                student1.save()
                    
                    # Set student as inactive
                student.is_active = False
                student.save()

            else:
                print("1 not")
                student = StudentsStdMultiList.objects.get(grno=grno,year=int(student1.admission_date)-1,standard=int(student1.standard)-1)
                
                print(student.year,"oky")
                StudentsStdMultiList.objects.filter(grno=student.grno, year__gt=student.year,standard__gt=student.standard).delete()
                
                if  student.is_active == True:
                    now = datetime.now()
                    week_name = now.strftime('%a')
                    formatted_date_time = now.strftime('%Y-%m-%d %H:%M')
                    date_time_with_week_name = f"{formatted_date_time} {week_name}"
                    existing_record = StudentsUpdatesHistory.objects.filter(
                    name=student1.first_name,
                    year=student1.admission_date,
                    standard=student1.standard
                    ).first()
                    if existing_record:
                        # Update existing record
                        existing_record.note = student1.note
                        existing_record.update_date = date_time_with_week_name
                        existing_record.save()
                    else:
                        # Create new record
                        StudentsUpdatesHistory.objects.create(
                            name=student1.first_name,
                            year=student1.admission_date,
                            standard=student1.standard,
                            note=student1.note,
                            update_date=date_time_with_week_name,
                        )
                student1.standard = student.standard
                student1.admission_date = student.year
                student1.save()
                    
                    # Set student as inactive
                student.is_active = False
                student.save()
                    
            
        return JsonResponse({'message': 'Students updated successfully'}, status=200)

# permission for exam for group
class HasExamPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(f'student.{view.required_permission}')

# Examtemplate get api
class ExamMarksTemplateAddGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasExamPermission]
    required_permission = 'can_view_exam_template'
    
    def get(self, request):
        # Get school_type from query parameters
        school_type = request.GET.get('school_type')
        
        # Start with base queryset
        queryset = ExamMarksTemplateAdd.objects.all()
        
        # Filter by school_type if provided
        if school_type:
            queryset = queryset.filter(
                standard__in=standard_master.objects.filter(
                    school_type=school_type,
                    is_active=True
                ).values_list('name', flat=True)
            )
        
        serialized_data = ExamMarksTemplateAddSerializer(queryset, many=True)
        return JsonResponse({
            "message": "ExamTemplate list Get Successfully", 
            "data": serialized_data.data
        }, status=200)


# Examtemplate patch api
class ExamMarksTemplateAddUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasExamPermission]
    required_permission = 'can_edit_exam_template'
    
    def patch(self, request, pk):
        try:
            exam = ExamMarksTemplateAdd.objects.get(pk=pk)
        except ExamMarksTemplateAdd.DoesNotExist:
            return JsonResponse({"message": "ExamTemplate not found"}, status=404)

        data = request.data
        serializer = ExamMarksTemplateAddSerializer(exam, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "ExamTemplate updated successfully", "data": serializer.data}, status=200)
        return JsonResponse({"message": "Invalid data", "errors": serializer.errors}, status=400)
    
    
# ExamTemplate get api for get by id 
class ExamMarksTemplateGetId(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasExamPermission]
    required_permission = 'can_view_exam_template'

    def get(self, request, pk):
        try:
            exam = ExamMarksTemplateAdd.objects.get(pk=pk)
            serialized_data = ExamMarksTemplateAddSerializer(exam)
            return JsonResponse({"message": "Exam Template retrieved successfully", "data": serialized_data.data}, status=200)
        except ExamMarksTemplateAdd.DoesNotExist:
            return JsonResponse({"message": "Exam Template not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=500)

# ExamTemplate POst api  

class ExamMarksTemplateAddAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasExamPermission]
    required_permission = 'can_add_exam_template'

    def post(self, request):
        try:
            data = request.data
            serializer = ExamMarksTemplateAddSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 

# ExamTemplate delete api  
class ExamMarksTemplateDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasExamPermission]
    required_permission = 'can_delete_exam_template'
    
    def delete(self, request, pk):
        try:
            exam = ExamMarksTemplateAdd.objects.get(pk=pk)
            exam_data = ExamMarkAssingData.objects.filter(ids=exam.id)
            # Delete all matching ExamMarkAssingData objects
            exam_data.delete()
        except ExamMarksTemplateAdd.DoesNotExist:
            return JsonResponse({"message": "Exam Template Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        exam.delete()
        return JsonResponse({"message": "Exam Template Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


# exam template assing mark api

class ExamMarksAssignAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasExamPermission]
    required_permission = 'can_assign_exam_marks'

    def get(self, request, standard, pk):
        exam_template = get_object_or_404(ExamMarksTemplateAdd, id=pk)
        students = Students.objects.filter(standard=standard,academic_year=AcademicYear.objects.filter(is_current=True).first())
        
        exam_template_data = ExamMarksTemplateAddSerializer(exam_template).data
        students_data = StudentsSerializer(students, many=True).data

        data = {
            'exam_template': exam_template_data,
            'students': students_data,
            'standard': standard,
        }
        return JsonResponse({"message": "Data retrieved successfully", "data": data}, status=200)

    def post(self, request, standard, pk):
        exam_template = get_object_or_404(ExamMarksTemplateAdd, id=pk)
        students = Students.objects.filter(standard=standard)
        
        serializer = ExamMarksAssignSerializer(data=request.data)
        if serializer.is_valid():
            for student in students:
                mark = serializer.validated_data['marks'].get(str(student.id))
                if mark is not None:
                    # Check if the entry already exists for this student and exam_template
                    existing_entry = ExamMarkAssingData.objects.filter(
                        ids=exam_template.id,
                        standard=standard,
                        student=student,
                    ).exists()
                    
                    if not existing_entry:
                        # Create new entry only if it doesn't already exist
                        ExamMarkAssingData.objects.create(
                            ids=exam_template.id,
                            standard=standard,
                            total_marks=exam_template.total_marks,
                            subject=exam_template.subject,
                            date=exam_template.date,
                            note=exam_template.note,
                            student=student,
                            gender=student.gender,
                            mark=mark,
                        )
            
            return JsonResponse({"message": "Exam marks assigned successfully"}, status=201)
        
        return JsonResponse({"message": "Invalid data", "errors": serializer.errors}, status=400)    
    
    
# exam template get api for assing students marks

class ExamMarksViewAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasExamPermission]
    required_permission = 'can_view_exam_marks'


    def get(self, request, standard, pk):
        exam_template = get_object_or_404(ExamMarksTemplateAdd, id=pk)
        exam_marks = ExamMarkAssingData.objects.filter(
            ids=pk,
            standard=standard,
            date=exam_template.date,
            total_marks=exam_template.total_marks,
            subject=exam_template.subject,
            student__academic_year=AcademicYear.objects.filter(is_current=True).first()
        )
        
        exam_template_data = ExamMarksTemplateAddSerializer(exam_template).data
        exam_marks_data = ExamMarkAssingDataSerializer(exam_marks, many=True).data

        data = {
            'exam_template': exam_template_data,
            'exam_marks': exam_marks_data,
        }
        return JsonResponse({"message": "Data retrieved successfully", "data": data}, status=200) 
    
    
# Exam Assing mark Update 
class ExamAssingUpdateMarkAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasExamPermission]
    required_permission = 'can_update_exam_marks'
    
    def patch(self, request, *args, **kwargs):
        exam_template_id = request.data.get('exam_template_id')
        standard = request.data.get('standard')
        mark_id = request.data.get('mark_id')
        new_mark_value = request.data.get('new_mark_value')

        if not all([exam_template_id, standard, mark_id, new_mark_value]):
            return JsonResponse({'error': 'exam_template_id, standard, mark_id and new_mark_value are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_mark_value = int(new_mark_value)
        except ValueError:
            return JsonResponse({'error': 'new_mark_value must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mark_instance = ExamMarkAssingData.objects.get(ids=exam_template_id, standard=standard, student_id=mark_id)
            mark_instance.mark = new_mark_value
            mark_instance.save()
            return JsonResponse({'success': True}, status=status.HTTP_200_OK)
        except ExamMarkAssingData.DoesNotExist:
            return JsonResponse({'error': 'No matching record found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        exam_template_id = request.query_params.get('exam_template_id')
        standard = request.query_params.get('standard')

        if not all([exam_template_id, standard]):
            return JsonResponse({'error': 'exam_template_id and standard are required'}, status=status.HTTP_400_BAD_REQUEST)

        marks = ExamMarkAssingData.objects.filter(ids=exam_template_id, standard=standard)
        data = [
            {
                'id': mark.id,
                'student_id': mark.student.id,
                'mark': mark.mark,
                'subject': mark.subject,
                'total_marks': mark.total_marks,
                'date': mark.date,
                'note': mark.note,
            }
            for mark in marks
        ]

        return JsonResponse({'data': data}, status=status.HTTP_200_OK)