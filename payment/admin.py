from django.contrib import admin

# Register your models here.
from .models import Receipt, ReceiptDetail, fee_type_master, fee_type, student_fees, historical_fees

admin.site.register(fee_type_master)
admin.site.register(fee_type)
admin.site.register(student_fees)
admin.site.register(historical_fees)
admin.site.register(Receipt)
admin.site.register(ReceiptDetail)
