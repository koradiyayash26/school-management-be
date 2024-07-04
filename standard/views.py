from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.pagination import PageNumberPagination

from student.models import STATUS_CHOICES, Students
from student.serializers import StudentsSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 

class CountStudents(APIView):
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



# api for perticuler standard student data
class StandardsGetData(APIView):
    def get(self, request, pk):
        try:
            # Filter students by standard
            students = Students.objects.filter(standard=pk)
            # Serialize the queryset
            serialized_data = StudentsSerializer(students, many=True)
            # Return serialized data as JSON response
            return JsonResponse({"message": "Students retrieved successfully", "data": serialized_data.data}, status=200)
        except Exception as e:
            # Handle exceptions
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=500)

        
class StandardsNo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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

            students = Students.objects.all()

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
        
        
