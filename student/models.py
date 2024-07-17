from django.db import models

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


SECTION_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

GENDER_CHOICE = (
    ('કુમાર', 'કુમાર'),
    ('કન્યા', 'કન્યા'),
)

STATUS_CHOICES = (
    ('ચાલુ', 'ચાલુ'),
    ('કમી', 'કમી'),
)

RELIGION_CHOICE = (
    ('હિન્દુ', 'હિન્દુ'),
    ('જૈન', 'જૈન'),
    ('મુસ્લિમ', 'મુસ્લિમ'),
    ('શિખ', 'શિખ'),
    ('ખ્રિસ્તી', 'ખ્રિસ્તી'),
)

CATEGORY_CHOICE = (
    ('જનરલ', 'જનરલ'),
    ('ઓ.બી.સી.', 'ઓ.બી.સી.'),
    ('એસસી/એસટી', 'એસસી/એસટી'),
    ('ઇ.ડબ્લ્યુ.એસ.', 'ઇ.ડબ્લ્યુ.એસ.'),
)
YEAR_CHOICES = (
    ("2025", "2025"),
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



class Students(models.Model):
    id = models.AutoField(primary_key=True)
    grno = models.IntegerField(unique=True)

    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=False)
    mother_name = models.CharField(max_length=60, null=True, blank=True, default="")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100, null=True, blank=True, default="")
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=False)
    district = models.CharField(max_length=50, null=True, blank=False)

    standard = models.CharField(max_length=14, choices=STD_CHOICES)
    section = models.CharField(max_length=2, choices=SECTION_CHOICES, null=True, blank=True)

    last_school = models.CharField(max_length=100, null=True, blank=True, default="")
    admission_std = models.CharField(max_length=10, choices=STD_CHOICES)
    admission_date = models.CharField(max_length=50,choices=YEAR_CHOICES)

    left_school_std = models.CharField(max_length=2, blank=True, null=True)
    left_school_date = models.DateField(blank=True, null=True)

    religion = models.CharField(max_length=50, choices=RELIGION_CHOICE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)
    caste = models.CharField(max_length=50, null=True, blank=True, default="")

    udise_no = models.CharField(max_length=50, blank=True, null=True, default="")
    aadhar_no = models.CharField(max_length=50, blank=True, null=True, default="")

    account_no = models.CharField(max_length=50, blank=True, null=True, default="")
    name_on_passbook = models.CharField(max_length=100, blank=True, null=True, default="")
    bank_name = models.CharField(max_length=50, blank=True, null=True, default="")
    ifsc_code = models.CharField(max_length=50, blank=True, null=True, default="")
    bank_address = models.CharField(max_length=100, blank=True, null=True, default="")

    reason = models.CharField(default=r"અન્યત્રે જવાથી",max_length=100, null=True, blank=True)
    note = models.CharField(max_length=100, blank=True, null=True, default="")

    assesment = models.IntegerField(default=1)
    progress = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ચાલુ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

    class Meta:
        db_table = 'students'
        verbose_name = "Student"
        verbose_name_plural = "Students"




class ExamMarks(models.Model):
    student = models.ForeignKey(to=Students, on_delete=models.SET_NULL, null=True)
    sub = models.CharField(max_length=100)
    std = models.CharField(max_length=10, choices=STD_CHOICES)
    date = models.DateField()
    total_marks = models.IntegerField()
    marks = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.student)
    
    
    
class EducationalYear(models.Model):
    year = models.CharField(max_length=50,choices=YEAR_CHOICES)
    
    def __str__(self):
        return str(self.year)
    
    
class SchoolStudent(models.Model):
    student = models.ForeignKey(to=Students, on_delete=models.SET_NULL, null=True)
    year = models.CharField(max_length=50,choices=YEAR_CHOICES,null=False)
    standard = models.CharField(max_length=14, choices=STD_CHOICES,null=False)
    note = models.CharField(max_length=100, blank=True, null=True)
    update_date=models.CharField(max_length=100,null=False,default='')
        
    def __str__(self):
        return str(self.student)
    
    
class UpdateStudent(models.Model):
    year = models.CharField(max_length=50,choices=YEAR_CHOICES,null=False)
    standard = models.CharField(max_length=10, choices=STD_CHOICES,null=False)


    def __str__(self):
        return str(self.year)
    
    
class StudentsStdMultiList(models.Model):
    id = models.AutoField(primary_key=True)
    grno = models.IntegerField(unique=False)
    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    year = models.CharField(max_length=50,choices=YEAR_CHOICES,null=False)
    standard = models.CharField(max_length=10, choices=STD_CHOICES,null=False)
    is_active = models.BooleanField(default=False)
    is_active_year = models.BooleanField(default=False)


    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name + " " + str(self.year))
    


class StudentsUpdateList(models.Model):
    id = models.AutoField(primary_key=True)
    grno = models.IntegerField(unique=False)

    student = models.ForeignKey(to=Students, on_delete=models.SET_NULL, null=True)
    
    middle_name = models.CharField(max_length=50, blank=False)
    mother_name = models.CharField(max_length=60, null=True, blank=True, default="")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100, null=True, blank=True, default="")
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=False)
    district = models.CharField(max_length=50, null=True, blank=False)

    standard = models.CharField(max_length=10, choices=STD_CHOICES)
    section = models.CharField(max_length=2, choices=SECTION_CHOICES, null=True, blank=True)

    last_school = models.CharField(max_length=100, null=True, blank=True, default="")
    admission_std = models.CharField(max_length=10, choices=STD_CHOICES)
    admission_date = models.CharField(max_length=50,choices=YEAR_CHOICES)
    left_school_std = models.CharField(max_length=2, blank=True, null=True)
    left_school_date = models.DateField(blank=True, null=True)

    religion = models.CharField(max_length=50, choices=RELIGION_CHOICE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)
    caste = models.CharField(max_length=50, null=True, blank=True, default="")

    udise_no = models.CharField(max_length=50, blank=True, null=True, default="")
    aadhar_no = models.CharField(max_length=50, blank=True, null=True, default="")

    account_no = models.CharField(max_length=50, blank=True, null=True, default="")
    name_on_passbook = models.CharField(max_length=100, blank=True, null=True, default="")
    bank_name = models.CharField(max_length=50, blank=True, null=True, default="")
    ifsc_code = models.CharField(max_length=50, blank=True, null=True, default="")
    bank_address = models.CharField(max_length=100, blank=True, null=True, default="")

    reason = models.CharField(default=r"અન્યત્રે જવાથી",max_length=100, null=True, blank=True)
    note = models.CharField(max_length=100, blank=True, null=True, default="")

    assesment = models.IntegerField(default=1)
    progress = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ચાલુ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student)

  


    
class StudentsUpdatesHistory(models.Model):
    name = models.CharField(max_length=50, blank=False,default='')
    year = models.CharField(max_length=50,choices=YEAR_CHOICES,null=False)
    standard = models.CharField(max_length=20, choices=STD_CHOICES,null=False)
    note = models.CharField(max_length=100, blank=True, null=True)
    update_date=models.CharField(max_length=100,null=False,default='')
        
    def __str__(self):
        return str(self.name)


class ExamMarksTemplateAdd(models.Model):
    id = models.AutoField(primary_key=True)
    standard = models.CharField(max_length=14, choices=STD_CHOICES)
    total_marks = models.IntegerField()
    subject = models.CharField(max_length=100)
    date = models.DateField()
    note = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.standard} - {self.subject} - {self.total_marks}"



class ExamMarkAssingData(models.Model):
    # id = models.AutoField(primary_key=True)
    ids = models.IntegerField(null=True)
    standard = models.CharField(max_length=14, choices=STD_CHOICES)
    total_marks = models.IntegerField()
    subject = models.CharField(max_length=100)
    date = models.DateField()
    note = models.CharField(max_length=100, blank=True, null=True)
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE,null=True)
    mark = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - Mark: {self.mark}"    