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

from payment.views import HasFeeReportPermission
from django.views.generic import TemplateView



class HomePageView(TemplateView):
    template_name = "home.html"  


# permission for school student for Group
class HasSchoolStudentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(f'student.{view.required_permission}')

# get api for school student
class SchoolStudentGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasSchoolStudentPermission]
    required_permission = 'can_view_school_students'
    def get(self, request):
        
        school_student = SchoolStudent.objects.all()
        serialized_data = SchoolStudentSerializer(school_student, many=True)
        return JsonResponse({"message": "School Students Get Successfully", "data": serialized_data.data}, status=200)

# get api for student name

class SchoolStudentNamesGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasSchoolStudentPermission]
    required_permission = 'can_view_school_student_names'

    def get(self, request):
        
        school_student = Students.objects.all()
        serialized_data = SchoolStudentDetailSerializer(school_student, many=True)
        return JsonResponse({"message": "School Students Name Get Successfully", "data": serialized_data.data}, status=200)

# get by id api for school student 

class SchoolStudentByIdGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasSchoolStudentPermission]
    required_permission = 'can_view_school_student_details'


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
    permission_classes = [IsAuthenticated, HasSchoolStudentPermission]
    required_permission = 'can_add_school_student'


    def post(self, request):
        serializer = SchoolStudentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "School Student Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# patch api for school student

class SchoolStudentPatch(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasSchoolStudentPermission]
    required_permission = 'can_edit_school_student'


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






from payment.models import  student_fees,Receipt
class FeeReportDetailAPIViewDemo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasFeeReportPermission]
    required_permission = 'can_view_fee_report_detail'

    def get(self, request, standard):
        try:
            # Get student fees data with fee type details
            student_fees_queryset = student_fees.objects.filter(
                standard_id=standard,
                is_assigned=True
            ).select_related(
                'student', 
                'standard', 
                'fee_type', 
                'fee_type__fee_master'
            )

            # Get receipt details
            receipt_details = ReceiptDetail.objects.filter(
                receipt__student__standard=standard
            ).select_related(
                'receipt', 
                'fee_type', 
                'fee_type__fee_master'
            ).values(
                'receipt__student_id',
                'fee_type__fee_master__name',
                'amount_paid',
                'amount_waived'
            )

            # Create a dictionary to store receipt totals by student and fee type
            receipt_totals = {}
            for detail in receipt_details:
                student_id = detail['receipt__student_id']
                fee_type_name = detail['fee_type__fee_master__name']
                
                if student_id not in receipt_totals:
                    receipt_totals[student_id] = {}
                
                if fee_type_name not in receipt_totals[student_id]:
                    receipt_totals[student_id][fee_type_name] = {
                        'paid': 0,
                        'waived': 0
                    }
                
                receipt_totals[student_id][fee_type_name]['paid'] += detail['amount_paid']
                receipt_totals[student_id][fee_type_name]['waived'] += detail['amount_waived']

            # Process student fees and receipts
            student_data = {}
            for fee in student_fees_queryset:
                student_id = fee.student_id
                if student_id not in student_data:
                    student_data[student_id] = {
                        'gr_no': fee.student.grno,
                        'first_name': fee.student.first_name,
                        'last_name': fee.student.last_name,
                        'standard': fee.standard.name if fee.standard else '',
                        'total_fee': 0,
                        'paid': 0,
                        'waived': 0,
                        'fee_structures': {}
                    }
                
                fee_type_name = str(fee.fee_type.fee_master) if fee.fee_type and fee.fee_type.fee_master else f'Fee Type {fee.fee_type_id}'
                fee_amount = fee.fee_type.amount if fee.fee_type else 0
                
                # Get paid and waived amounts from receipts
                paid_amount = 0
                waived_amount = 0
                if student_id in receipt_totals and fee_type_name in receipt_totals[student_id]:
                    paid_amount = receipt_totals[student_id][fee_type_name]['paid']
                    waived_amount = receipt_totals[student_id][fee_type_name]['waived']

                if fee_type_name not in student_data[student_id]['fee_structures']:
                    student_data[student_id]['fee_structures'][fee_type_name] = {
                        'amount': fee_amount,
                        'paid': paid_amount,
                        'waived': waived_amount,
                        'pending': fee_amount - paid_amount - waived_amount
                    }
                
                student_data[student_id]['total_fee'] += fee_amount
                student_data[student_id]['paid'] += paid_amount
                student_data[student_id]['waived'] += waived_amount

            # Calculate pending amount and prepare final list
            student_fees_list = []
            for student in student_data.values():
                student['pending'] = student['total_fee'] - student['paid'] - student['waived']
                student_fees_list.append(student)

            # Calculate totals
            totals = {
                'total_fee': sum(s['total_fee'] for s in student_fees_list),
                'paid': sum(s['paid'] for s in student_fees_list),
                'waived': sum(s['waived'] for s in student_fees_list),
                'pending': sum(s['pending'] for s in student_fees_list),
            }

            # Get all unique fee types
            fee_types = sorted(list(set(
                fee_type
                for student in student_fees_list
                for fee_type in student['fee_structures'].keys()
            )))

            response_data = {
                'message': 'Fee report details retrieved successfully',
                'data': {
                    'students': student_fees_list,
                    'fee_types': fee_types,
                    'totals': totals,
                    'standard': standard
                }
            }

            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse(
                {'message': 'An error occurred', 'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )