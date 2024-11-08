from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics

from student.models import STATUS_CHOICES, Students
from student.serializers import StudentsSerializer
from .models import standard_master,AcademicYear
from .serializers import StandardMasterSerializer,AcademicYearSerializer

from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import BasePermission


class CountStudents(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        std = {"13":0,"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0}

        data = Students.objects.filter(status=STATUS_CHOICES[0][0]).values_list("standard").all()
        for i in data:
            std[str(i[0])] += 1
            # print(i)

        finalResponse = {
            "message": "Student Count Successfully",
            "data": std
        }
        return JsonResponse(finalResponse, safe=False, status=200)

# permission for standard report for Group
class HasStandardReportPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(f'standard.{view.required_permission}')
    
    
# api for perticuler standard student data
class StandardsGetData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasStandardReportPermission]
    required_permission = 'can_view_standards_data'

    def get(self, request, pk):
        try:
            # Filter students by standard
            students = Students.objects.filter(standard=pk,academic_year=AcademicYear.objects.filter(is_current=True).first())
            # Serialize the queryset
            serialized_data = StudentsSerializer(students, many=True)
            # Return serialized data as JSON response
            return JsonResponse({"message": "Students retrieved successfully", "data": serialized_data.data}, status=200)
        except Exception as e:
            # Handle exceptions
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=500)

        
class StandardsNo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,HasStandardReportPermission]
    required_permission = 'can_view_standards_count'

    def get(self, request):
        try:
            standard_counts = {
                "13": {"boys_count": 0, "girls_count": 0},
                "1": {"boys_count": 0, "girls_count": 0},
                "2": {"boys_count": 0, "girls_count": 0},
                "3": {"boys_count": 0, "girls_count": 0},
                "4": {"boys_count": 0, "girls_count": 0},
                "5": {"boys_count": 0, "girls_count": 0},
                "6": {"boys_count": 0, "girls_count": 0},
                "7": {"boys_count": 0, "girls_count": 0},
                "8": {"boys_count": 0, "girls_count": 0},
                "9": {"boys_count": 0, "girls_count": 0},
                "10": {"boys_count": 0, "girls_count": 0},
                "11": {"boys_count": 0, "girls_count": 0},
                "12": {"boys_count": 0, "girls_count": 0}
            }

            students = Students.objects.filter(academic_year=AcademicYear.objects.filter(is_current=True).first())

            boys_count = 0
            girls_count = 0
            total_count = 0
            for student in students:
                if student.gender == "કુમાર":
                    boys_count += 1
                else:
                    girls_count += 1
                standard_counts[student.standard]["boys_count"] += 1 if student.gender == "કુમાર" else 0
                standard_counts[student.standard]["girls_count"] += 1 if student.gender == "કન્યા" else 0
                total_count += 1

            response_data = {
                "message": "Standards Get Successfully",
                "data": {
                    "standards": [
                        {"standard": std, "boys_count": count["boys_count"], "girls_count": count["girls_count"]}
                        for std, count in standard_counts.items()
                    ],
                    "total_boys": boys_count,
                    "total_girls": girls_count,
                    "total_students": total_count
                }
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=500)
        
        
class StandardMasterListCreateView(generics.ListCreateAPIView):
    queryset = standard_master.objects.all()
    serializer_class = StandardMasterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class StandardMasterRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = standard_master.objects.all()
    serializer_class = StandardMasterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    
    

class AcademicYearListCreateView(generics.ListCreateAPIView):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class AcademicYearRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    