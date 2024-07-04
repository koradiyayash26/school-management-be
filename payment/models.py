from django.db import models

from standard.models import standard_master
from student.models import Students

STD_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
)


FEETYPE_CHOICES = (
    ("સ્કૂલ ફી", "સ્કૂલ ફી"),
    ("bus fee", "bus fee"),
    ("form fee", "form fee"),
    ("other", "other"),
)

YEAR_CHOICES = (
    ("2024", "2024"),
    ("2023", "2023"),
    ("2022", "2022"),
    ("2021", "2021"),
    ("2020", "2020"),
    ("2019", "2019"),
    ("2018", "2018"),
    ("2017", "2017"),
    ("2016", "2016"),
    ("2015", "2015"),
    ("2014", "2014"),
    ("2013", "2013"),
    ("2012", "2012"),
    ("2011", "2011"),
    ("2010", "2010"),
    ("2009", "2009"),
    ("2008", "2008"),
    ("2007", "2007"),
    ("2006", "2006"),
    ("2005", "2005"),
    ("2004", "2004"),
    ("2003", "2003"),
    ("2002", "2002"),
    ("2001", "2001"),
    ("2000", "2000"),
)


class fee_type_master(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # school_id = models.CharField(max_length=5, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'fee_type_master'
        ordering = ['created_at']
        verbose_name = "Fee-Type-Master"
        verbose_name_plural = "Fee-Type-Master"


class fee_type(models.Model):
    id = models.AutoField(primary_key=True)
    fee_master = models.ForeignKey(to=fee_type_master, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveBigIntegerField()
    standard = models.ForeignKey(to=standard_master, on_delete=models.SET_NULL, null=True)
    year = models.CharField(max_length=50,choices=YEAR_CHOICES,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.fee_master)} - {str(self.standard)}"

    class Meta:
        db_table = 'fee_type'
        ordering = ['-created_at']
        verbose_name = "Fee-Type"
        verbose_name_plural = "Fee-Type"


class student_fees(models.Model):
    id = models.AutoField(primary_key=True)
    standard = models.ForeignKey(to=standard_master, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(to=Students, on_delete=models.SET_NULL, null=True)
    fee_type = models.ForeignKey(to=fee_type, on_delete=models.SET_NULL, null=True)
    amount_paid = models.PositiveBigIntegerField(default=0)
    amount_waived = models.PositiveBigIntegerField(default=0)
    is_assigned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.student)} - {str(self.standard)}"

    class Meta:
        db_table = 'student_fees'
        ordering = ['-created_at']
        verbose_name = "Student-Fee"
        verbose_name_plural = "Student-Fee"


class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(to=Students, on_delete=models.SET_NULL, null=True)
    # receipt_no = models.PositiveIntegerField(default=0)
    fee_paid_date = models.DateField(null=True, blank=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.student)}"


class ReceiptDetail(models.Model):
    id = models.AutoField(primary_key=True)
    receipt = models.ForeignKey(to=Receipt, on_delete=models.CASCADE, null=True)
    fee_type = models.ForeignKey(to=fee_type, on_delete=models.SET_NULL, null=True)
    total_fee = models.PositiveBigIntegerField(default=0)
    amount_paid = models.PositiveBigIntegerField(default=0)
    amount_waived = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.total_fee)}"


class historical_fees(models.Model):
    standard = models.CharField(max_length=10, choices=STD_CHOICES)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    date = models.DateField()
    name = models.CharField(max_length=50)
    receipt_no = models.CharField(max_length=10)
    fee_type = models.CharField(max_length=10, choices=FEETYPE_CHOICES)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{str(self.name)} - {str(self.standard)}"

    class Meta:
        db_table = 'historical_fees'
        ordering = ['standard']
        verbose_name = "Historical-Fee"
        verbose_name_plural = "Historical-Fee"
