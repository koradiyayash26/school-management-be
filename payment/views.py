import json
from .serializers import FeeTypeMasterSerializer,FeeTypePostSerializer,FeeTypeGetSerializer,HistoricalFeesSerializer,ReceiptDetailsFeesSerializer,StudentFeeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from standard.serializers import StandardSerializer 
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from student.models import Students,SchoolStudent
from .models import (Receipt, ReceiptDetail, fee_type, historical_fees,fee_type_master,standard_master,
                     student_fees)

# Post api for fee-type template add

class FeeTypesPost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FeeTypePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Fee-Type Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({"message": "Invalid Data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# get api for fee-type
class FeeTypeGet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fee_types = fee_type.objects.all()
        serializer = FeeTypeGetSerializer(fee_types, many=True)
        return JsonResponse({"message": "Fee Types Retrieved Successfully", "data": serializer.data}, status=status.HTTP_200_OK)


# get api by id fee type
class FeeTypeIdGetData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            fee_type_instance = fee_type.objects.get(pk=pk)
            serializer = FeeTypeGetSerializer(fee_type_instance)
            return JsonResponse({"message": "Fee Type Retrieved Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except fee_type.DoesNotExist:
            return JsonResponse({"message": "Fee Type Not Found"}, status=status.HTTP_404_NOT_FOUND)


#  patch api fee type
class FeeTypePatch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            fee_type_instance = fee_type.objects.get(pk=pk)
        except fee_type.DoesNotExist:
            return JsonResponse({"message": "Fee Type Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeeTypePostSerializer(fee_type_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Fee Type Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({"message": "Invalid Data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
#  get api for standard-master,Fee-Type-Master

class FeeTypeGetAddDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        fee_master = fee_type_master.objects.all()
        standard = standard_master.objects.all()
        serialized_fee_master_data = FeeTypeMasterSerializer(fee_master, many=True)
        serialized_standard_data = StandardSerializer(standard, many=True)
        combined_data = {
            "fee_master": serialized_fee_master_data.data,
            "standard": serialized_standard_data.data
        }
        return JsonResponse({"message": "Fee-Type-Add Data Get Successfully", "data": combined_data}, status=200)


# delete api for feeType

class FeeTypeDelete(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            fee = fee_type.objects.get(pk=pk)
        except fee_type.DoesNotExist:
            return JsonResponse({"message": "Fee-Type Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        fee.delete()
        return JsonResponse({"message": "Fee-Type Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


# Get api for Historical Fees

class HistoricalDataGetApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fee_types = historical_fees.objects.all()
        serializer = HistoricalFeesSerializer(fee_types, many=True)
        return JsonResponse({"message": "Historical fee data Retrieved Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

#  Delete api for Historical fee

class HistoricalDataDeleteApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            fee_type = historical_fees.objects.get(pk=pk)
            fee_type.delete()
            return JsonResponse({"message": "Historical fee data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except historical_fees.DoesNotExist:
            return JsonResponse({"message": "Historical fee data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Post api For Historical Fee

class HistoricalDataPostApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HistoricalFeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Historical fee data created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# get api for studentfeee
class StudentAssignFeeApiGet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, standard, pk, year):
        # Get the queryset for assigned students
        assigned_students = Students.objects.filter(
            standard=standard, 
            student_fees__fee_type__id=pk, 
            student_fees__is_assigned=True, 
            status='ચાલુ'
        )

        # Get the list of SchoolStudent objects for the given standard and year
        school_students = SchoolStudent.objects.filter(
            standard=standard,
            year=year
        )

        # Extract the student IDs from the SchoolStudent queryset
        student_ids = school_students.values_list('student', flat=True).distinct()

        # Get the students who are not assigned
        not_assigned_students = Students.objects.filter(
            id__in=student_ids,
            status='ચાલુ'
        ).exclude(id__in=assigned_students.values_list('id', flat=True))

        # Serialize the data
        assigned_students_serializer = StudentFeeSerializer(assigned_students, many=True)
        not_assigned_students_serializer = StudentFeeSerializer(not_assigned_students, many=True)

        # Create the context for the response
        context = {
            'fee_type_id': pk,
            'standard': standard,
            'year': year,
            'assigned_students': assigned_students_serializer.data,
            'not_assigned_students': not_assigned_students_serializer.data,
        }

        return JsonResponse(context)
    


class StudentAssignUnAssign(APIView):
    def patch(self, request):
        data = request.data
        finalResponse = {
            "message": "Student Assigned",
        }
        fee_type = data['fee_type_id']
        standard = data['standard']
        students_list = data['students']
        assign = data['assign']
        for i in students_list:
            fee_paid_count = ReceiptDetail.objects.filter(receipt__student_id=i, fee_type_id=fee_type).exclude(amount_paid=0, amount_waived=0).count()
            if not assign and (fee_paid_count != 0):
                finalResponse['message'] = 'some student has already paid fee'
                continue
            student_fees.objects.update_or_create(fee_type_id=fee_type, standard_id=standard, student_id=i, defaults={"is_assigned": assign})

            

        return JsonResponse(finalResponse, safe=False, status=200)

# get api for payment student for add amount payment 1/2024 

class PaymentStudentFeeGet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, year, format=None):
        # Fetch the student
        student = get_object_or_404(Students, id=pk)

        # Fetch the school student for the given year
        try:
            school_student = SchoolStudent.objects.get(
                year=year,
                student__id=student.id,
                student__first_name=student.first_name,
                student__last_name=student.last_name
            )
        except SchoolStudent.DoesNotExist:
            return JsonResponse({"alert": "SchoolStudent not found for the selected year and student"}, status=status.HTTP_404_NOT_FOUND)

        # Prepare student context
        student_context = {
            "id": student.id,
            "name": f"{student.first_name} {student.middle_name} {student.last_name}",
            "std": student.standard,
            "grno": student.grno,
            "standard": student.standard,
            "section": student.section,
            "address": student.address,
        }

        # Fetch receipts
        receipt = Receipt.objects.filter(student_id=student.id).values(
            'id', 'note', 'fee_paid_date', 'student__first_name',
            'student__last_name', 'student__middle_name', 'student__standard',
            'student__grno'
        ).annotate(
            paid=Sum('receiptdetail__amount_paid'),
            waived=Sum('receiptdetail__amount_waived')
        ).order_by('-fee_paid_date')

        # Fetch fees
        fees = list(student_fees.objects.filter(student_id=student.id, is_assigned=True).values(
            'fee_type', 'amount_paid', 'amount_waived', 'fee_type__id',
            'fee_type__fee_master__name', 'fee_type__amount'
        ))
        for i in fees:
            pw = ReceiptDetail.objects.filter(receipt__student_id=student, fee_type=i['fee_type']).aggregate(
                paid=Sum('amount_paid'),
                waived=Sum('amount_waived')
            )
            i['amount_paid'] = pw['paid'] if pw['paid'] else 0
            i['amount_waived'] = pw['waived'] if pw['waived'] else 0

        # Calculate fee totals
        fee_total = {
            "total_fee": sum(i['fee_type__amount'] for i in fees),
            "amount_paid": sum(i['amount_paid'] for i in fees),
            "amount_waived": sum(i['amount_waived'] for i in fees)
        }

        # Prepare response data
        context = {
            "student": student_context,
            "fees": fees,
            "fee_total": fee_total,
            "receipt": list(receipt),  # Convert QuerySet to list
            "jsonfees": json.dumps(fees),
        }

        return JsonResponse(context, status=status.HTTP_200_OK)

# patch for paymentstudent 
class PaymentStudentFeePatch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        data = request.data
        fees = data['fees']
        student_id = data['student_id']
        fee_paid_date = data['fee_paid_date']
        note = data['note']

        prev_fees = list(student_fees.objects.filter(student_id=student_id, is_assigned=True).values('fee_type', 'amount_paid', 'amount_waived', 'fee_type__id', 'fee_type__fee_master__name', 'fee_type__amount'))
        for i in prev_fees:
            pw = ReceiptDetail.objects.filter(receipt__student_id=student_id, fee_type=i['fee_type']).aggregate(paid=Sum('amount_paid'), waived=Sum('amount_waived'))
            # print(pw)
            i['amount_paid'] = pw['paid'] if pw['paid'] else 0
            i['amount_waived'] = pw['waived'] if pw['waived'] else 0

        # prev_fees = list(ReceiptDetail.objects.filter(receipt__student_id=student_id).values("receipt__student__standard", "fee_type__id", "fee_type__fee_master__name", "fee_type__amount").annotate(paid=Sum('amount_paid'), waived=Sum('amount_waived')))

        # prev_fees = list(student_fees.objects.filter(student_id=student_id, is_assigned=True).values('id', 'fee_type__id', 'fee_type__fee_master__name', 'fee_type__amount', 'amount_paid', 'amount_waived', 'standard_id', 'student__id'))

        receipt_details = []

        for x, y in zip(prev_fees, fees):
            print(x, y)
            if x['amount_paid'] < int(y['amount_paid']) or x['amount_waived'] < int(y['amount_waived']):
                # student_fees.objects.filter(id=x['id']).update(amount_paid=int(y['amount_paid']), amount_waived=int(y['amount_waived']))
                if x['amount_paid'] + x['amount_waived'] == 0:
                    receipt_details.append({
                        "fee_type__id": y['fee_type__id'],
                        "total_fee": x["fee_type__amount"],
                        "amount_paid": int(y['amount_paid']),
                        "amount_waived": int(y['amount_waived']),
                    })
                else:
                    if int(y['amount_paid']) + int(y['amount_waived']) > x['fee_type__amount']:
                        return JsonResponse({"error": "can't pay more than total fees"}, safe=False, status=400)
                    new_paid = int(y['amount_paid']) - x['amount_paid']
                    new_waived = int(y['amount_waived']) - x['amount_waived']

                    receipt_details.append({
                        "fee_type__id": y['fee_type__id'],
                        "total_fee": x["fee_type__amount"],
                        "amount_paid": new_paid,
                        "amount_waived": new_waived
                    })

        if len(receipt_details) > 0:
            receipt = Receipt.objects.create(fee_paid_date=fee_paid_date, note=note, student_id=student_id)
            for i in receipt_details:
                ReceiptDetail.objects.create(receipt=receipt, fee_type_id=i['fee_type__id'], total_fee=i['total_fee'], amount_paid=int(i['amount_paid']), amount_waived=int(i['amount_waived']))

        finalResponse = {
            "message": "Fee Collected",
        }
        return JsonResponse(finalResponse, safe=False, status=200)


# api get for paymenthistory

class PaymentFeeListGet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Receipt.objects.filter().values('id', 'note', 'fee_paid_date', 'student__first_name', 'student__last_name', 'student__middle_name', 'student__standard', 'student__grno').annotate(paid=Sum('receiptdetail__amount_paid'), waived=Sum('receiptdetail__amount_waived')).order_by('-fee_paid_date')
        data = list(queryset)  # Convert queryset to a list
        return JsonResponse({"message": "Payment history fetched successfully", "data": data}, status=200)


# api get by id for receiptDetails

class PaymentReceiptDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            receipt_detail = ReceiptDetail.objects.get(pk=pk)
        except ReceiptDetail.DoesNotExist:
            return JsonResponse({"message": "ReceiptDetail not found"}, status=404)

        serializer = ReceiptDetailsFeesSerializer(receipt_detail)
        return JsonResponse({"message": "Payment history fetched successfully", "data": serializer.data}, status=200)

# api get by id for paymenthistory

class PaymentFeeListIdToGet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
            try:
                receipt = Receipt.objects.all().values(
                    'id', 'note', 'fee_paid_date', 'student__first_name',
                    'student__last_name', 'student__middle_name', 
                    'student__standard', 'student__grno'
                ).annotate(
                    paid=Sum('receiptdetail__amount_paid'),
                    waived=Sum('receiptdetail__amount_waived')
                ).first()
                if receipt:
                    return JsonResponse({"message": "Payment history fetched successfully", "data": receipt}, status=200)
                else:
                    return JsonResponse({"message": "Receipt not found"}, status=404)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)

# api for delete api 
class PaymentFeeDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            receipt = Receipt.objects.get(pk=pk)
            receipt.delete()
            return JsonResponse({"message": "Receipt deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Receipt.DoesNotExist:
            return JsonResponse({'error': 'Receipt not found'}, status=status.HTTP_404_NOT_FOUND)


class FeeTotalCount(APIView):
    def get(self, request):
        """
        Payload Example: [
            {"std": "1", "total": "51", "pending": "10", "paid": "41"}
        ]
        """
        feepayload = []
        for i in range(13):
            std = i + 1
            total_fees = student_fees.objects.filter(standard=std).aggregate(total=Sum('fee_type__amount'))
            fees_breakup = Receipt.objects.filter(student__standard=std).aggregate(total=Sum('receiptdetail__total_fee'), paid=Sum('receiptdetail__amount_paid'), waived=Sum('receiptdetail__amount_waived'))
            total_fee = total_fees['total'] if total_fees['total'] else 0
            paid_fee = fees_breakup['paid'] if fees_breakup['paid'] else 0
            waived_fee = fees_breakup['waived'] if fees_breakup['waived'] else 0

            feepayload.append(
                {
                    "std": std,
                    "total": total_fee,
                    "paid": paid_fee,
                    "pending": total_fee - paid_fee - waived_fee,
                    "waived": waived_fee
                }
            )
        
        feepayload.append(
            {
                "std": "Total",
                "total": sum([i['total'] for i in feepayload]),
                "paid": sum([i['paid'] for i in feepayload]),
                "pending": sum([i['pending'] for i in feepayload]),
                "waived": sum([i['waived'] for i in feepayload])
            }
        )

        finalResponse = {
            "message": "Fee Breakup Fetched",
            "data": feepayload
        }
        return JsonResponse(finalResponse, safe=False, status=200)
