from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, Http404,HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q,Count
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from datetime import timedelta
from django.utils import timezone

from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ExamMarks
from django.views import View
from django.http import HttpResponse
from datetime import datetime
from datetime import datetime

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics,status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 

from django.core import serializers
from .models import Students,SchoolStudent,UpdateStudent,StudentsUpdateList,StudentsStdMultiList,StudentsUpdatesHistory,ExamMarksTemplateAdd
from .serializers import StudentsSerializer,ExamSerializer,ExamGetSerializer,ExamPatchSerializer,StudentUpdateHistoricalSerializer,StudentUpdateStdYearSerializer,StudentUpdatedSerializer,ExamMarksTemplateAddSerializer

from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication

class StudentAdd(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        students = Students.objects.all()
        serialized_data = StudentsSerializer(students, many=True)
        return JsonResponse({"message": "Students Get Successfully", "data": serialized_data.data}, status=200)
    
    
# api for exam marks get

class ExamMarksGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        exam = ExamMarks.objects.all()
        serialized_data = ExamGetSerializer(exam, many=True)
        return JsonResponse({"message": "Students Marks Get Successfully", "data": serialized_data.data}, status=200)
    
    
# Single Exammarks get api by id

class ExamMarksGetId(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            exam = ExamMarks.objects.get(pk=pk)
            serialized_data = ExamGetSerializer(exam)
            return JsonResponse({"message": "Student Mark retrieved successfully", "data": serialized_data.data}, status=200)
        except ExamMarks.DoesNotExist:
            return JsonResponse({"message": "Student Mark not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=500)
    
# update api for exammarks

class ExamMarksUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        try:
            exam = ExamMarks.objects.get(pk=pk)
            serializer = ExamPatchSerializer(instance=exam, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Exam mark updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ExamMarks.DoesNotExist:
            return JsonResponse({"message": "Exam mark not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
# add Api for exammarks

class ExamMarksAdd(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = ExamPatchSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Exam mark created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# upload file of xcel data post api for exammarks

class ExamMarksUploadFileAdd(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    FIELD_NAME_MAPPING = {
        "student": ["student", "Student", "stUdent", "stuDent"],
        "date": ["date", "Date", "daTe"],
        "subject": ["subject", "Subject", "subjecTect", "subJect"],
        "standard": ["standard", "Standard", "stanDard"],
        "total_marks": ["total_marks", "Total Marks", "Total_Marks", "totalMarks"],
        "marks": ["marks", "Marks", "markS"]
    }

    def get_student_id(self, student_name, standard):
        try:
            first_name, last_name = student_name.split(" ", 1)
            standard = "13" if str(standard).lower() == "balvatika" else standard
            
            formats_to_try = [
                (first_name.upper(), last_name.upper()),
                (first_name.lower(), last_name.lower()),
                (first_name.capitalize(), last_name.capitalize()),
                (first_name.title(), last_name.title()),
                (first_name, last_name)
            ]

            for fn, ln in formats_to_try:
                try:
                    student = Students.objects.get(first_name=fn, last_name=ln, standard=standard)
                    return student.id
                except ObjectDoesNotExist:
                    continue

            return None
        except (ObjectDoesNotExist, ValueError):
            return None

    def normalize_keys(self, data):
        normalized_data = {}
        for key, value in data.items():
            found = False
            for field, variations in self.FIELD_NAME_MAPPING.items():
                if key.lower().replace(" ", "_") in [v.lower().replace(" ", "_") for v in variations]:
                    normalized_data[field] = value
                    found = True
                    break
            if not found:
                normalized_data[key.lower().replace(" ", "_")] = value  # Default case
        return normalized_data

    def post(self, request):
        try:
            exam_marks = request.data
            if not isinstance(exam_marks, list):
                return JsonResponse({"message": "Invalid data format, expected a list"}, status=status.HTTP_400_BAD_REQUEST)

            errors = []
            created_data = []

            for exam_mark in exam_marks:
                exam_mark = self.normalize_keys(exam_mark)

                standard = exam_mark.get("standard")
                student_id = self.get_student_id(exam_mark.get("student"), standard)

                if student_id is None:
                    errors.append({"student": [f"Student '{exam_mark.get('student')}' with standard '{standard}' not found."]})
                    continue

                transformed_exam_mark = {
                    "student": student_id,
                    "std": "13" if str(standard).lower() == "balvatika" else standard,
                    "sub": exam_mark.get("subject"),
                    "marks": exam_mark.get("marks"),
                    "total_marks": exam_mark.get("total_marks"),
                    "date": exam_mark.get("date"),
                }

                serializer = ExamPatchSerializer(data=transformed_exam_mark)
                if serializer.is_valid():
                    serializer.save()
                    created_data.append(serializer.data)
                else:
                    transformed_errors = {}
                    for field, error_list in serializer.errors.items():
                        transformed_field = field.lower().replace(' ', '_')
                        transformed_errors[transformed_field] = error_list
                    errors.append(transformed_errors)

            if errors:
                return JsonResponse({"message": "Some entries failed to save", "errors": errors, "created_data": created_data}, status=status.HTTP_207_MULTI_STATUS)

            return JsonResponse({"message": "All exam marks created successfully", "data": created_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# delete for exammarks api

class ExamMarksDelete(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            fee = ExamMarks.objects.get(pk=pk)
        except ExamMarks.DoesNotExist:
            return JsonResponse({"message": "Fee-Type Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        fee.delete()
        return JsonResponse({"message": "Fee-Type Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



# Student uppdate historical get api

class StudentUpdateHistoricalGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        students = StudentsUpdatesHistory.objects.all()
        serialized_data = StudentUpdateHistoricalSerializer(students, many=True)
        return JsonResponse({"message": "Student Update Historical Get Successfully", "data": serialized_data.data}, status=200)

# Student uppdate historical Delete api

class StudentUpdateHistoricalDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            student = Students.objects.get(pk=pk)
            data = request.data
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
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            student = Students.objects.get(pk=pk)
            student.delete()
            return JsonResponse({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Students.DoesNotExist:
            return JsonResponse({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            
            
# student update year and std get api of template

class StudentUpdateStdYearGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        template = UpdateStudent.objects.all()
        serialized_data = StudentUpdateStdYearSerializer(template, many=True)
        return JsonResponse({"message": "Students Standard And Year Template Get Successfully", "data": serialized_data.data}, status=200)

# student update year and std Post api of template

class StudentUpdateStdYearPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = StudentUpdateStdYearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Student update template created successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# post API for add students on StudentsStdMultilist
class StudentsAddYearAndstdFromurl(APIView):
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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



# Examtemplate get api
class ExamMarksTemplateAddGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        exam = ExamMarksTemplateAdd.objects.all()
        serialized_data = ExamMarksTemplateAddSerializer(exam, many=True)
        return JsonResponse({"message": "ExamTemplate list Get Successfully", "data": serialized_data.data}, status=200)


# Examtemplate patch api
class ExamMarksTemplateAddUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    