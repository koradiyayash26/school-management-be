from django.db.models import F, Sum
from django.http import JsonResponse
from rest_framework import status
# from weasyprint import HTML
from rest_framework.views import APIView

from student.models import Students,SchoolStudent


from payment.models import (ReceiptDetail,
                            student_fees)


from .serializers import SchoolStudentSerializer,SchoolStudentDetailSerializer,SchoolStudentPostSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

class HasFeeStudentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(f'school.{view.required_permission}')

# get api for school student
class SchoolStudentGet(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, HasFeeStudentPermission]
    required_permission = 'can_view_fee_student'
    def get(self, request):
        
        school_student = SchoolStudent.objects.all()
        serialized_data = SchoolStudentSerializer(school_student, many=True)
        return JsonResponse({"message": "School Students Get Successfully", "data": serialized_data.data}, status=200)

# get api for student name

class SchoolStudentNamesGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasFeeStudentPermission]
    required_permission = 'can_view_fee_student'

    def get(self, request):
        
        school_student = Students.objects.all()
        serialized_data = SchoolStudentDetailSerializer(school_student, many=True)
        return JsonResponse({"message": "School Students Name Get Successfully", "data": serialized_data.data}, status=200)

# get by id api for school student 

class SchoolStudentByIdGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasFeeStudentPermission]
    required_permission = 'can_view_fee_student'


    def get(self, request, pk):
        try:
            school_student = SchoolStudent.objects.get(pk=pk)
        except SchoolStudent.DoesNotExist:
            return JsonResponse({"error": "School Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = SchoolStudentSerializer(school_student)
        return JsonResponse({"message": "School Student Retrieved Successfully", "data": serialized_data.data}, status=status.HTTP_200_OK)

#  post api for school student

class SchoolStudentPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasFeeStudentPermission]
    required_permission = 'can_view_fee_student'


    def post(self, request):
        serializer = SchoolStudentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "School Student Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# patch api for school student

class SchoolStudentPatch(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasFeeStudentPermission]
    required_permission = 'can_view_fee_student'


    def patch(self, request, pk):
        try:
            school_student = SchoolStudent.objects.get(pk=pk)
        except SchoolStudent.DoesNotExist:
            return JsonResponse({"error": "School Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SchoolStudentPostSerializer(school_student, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "School Student Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# get api by single student of report standard 

class ReportStandardGetAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, std):
        try:
            # Get assigned students
            assigned_students = student_fees.objects.filter(
                student__standard=F('standard__name'), 
                standard_id=std, 
                is_assigned=True
            ).values(
                'student_id', 
                'student__first_name', 
                'student__last_name', 
                'student__middle_name', 
                'student__standard', 
                'student__grno', 
                'student__city'
            ).annotate(total=Sum('fee_type__amount')).order_by()

            # Get fee type IDs
            fee_types_id_list = student_fees.objects.filter(
                standard_id=std, 
                is_assigned=True
            ).values_list('fee_type_id', flat=True)

            # Get paid students
            paid_students = ReceiptDetail.objects.filter(
                fee_type_id__in=fee_types_id_list
            ).values(
                'receipt__student_id'
            ).annotate(
                paid=Sum('amount_paid'), 
                waived=Sum('amount_waived')
            )

            # Annotate assigned students with paid and waived amounts
            for student in assigned_students:
                student['paid'] = 0
                student['waived'] = 0
                for paid_student in paid_students:
                    if student['student_id'] == paid_student['receipt__student_id']:
                        student['paid'] = paid_student['paid']
                        student['waived'] = paid_student['waived']

            # Return the data as a JSON response
            return JsonResponse({"message": "Report Standard data retrieved successfully", "data": list(assigned_students)}, status=200, safe=False)
        except student_fees.DoesNotExist:
            return JsonResponse({"message": "Report Standard data not found for the given standard"}, status=404)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=500)

