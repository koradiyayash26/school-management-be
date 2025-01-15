from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests
from datetime import datetime


# run command python manage.py fek_student_data 100 --token=your_token

class Command(BaseCommand):
    help = 'Create and send dummy student data to the API'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of students to be created')
        parser.add_argument('--token', type=str, help='Authentication token for the API')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        token = kwargs['token']
        fake = Faker('en_IN')
        # fake = Faker('en_US')
        api_url = 'https://school-management-be-2.onrender.com/students/add/'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        STD_CHOICES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        SECTION_CHOICES = ['A', 'B', 'C', 'D']
        GENDER_CHOICE = ['કુમાર', 'કન્યા']
        RELIGION_CHOICE = ['હિન્દુ', 'જૈન', 'મુસ્લિમ', 'શિખ', 'ખ્રિસ્તી']
        CATEGORY_CHOICE = ['જનરલ', 'ઓ.બી.સી.', 'એસસી/એસટી', 'ઇ.ડબ્લ્યુ.એસ.']
        STATUS_CHOICES = ['ચાલુ', 'પૂર્ણ', 'રદ']
        CURRENT_YEAR = datetime.now().year
        YEAR_CHOICES = [str(year) for year in range(CURRENT_YEAR - 10, CURRENT_YEAR + 1)]

        for _ in range(total):
            # Select standard first to make roll number assignment logical
            selected_standard = random.choice(STD_CHOICES)
            
            student_data = {
                'grno': fake.unique.random_number(digits=6),
                'last_name': fake.last_name(),
                'first_name': fake.first_name(),
                'middle_name': fake.first_name(),
                'mother_name': fake.name_female(),
                'gender': random.choice(GENDER_CHOICE),
                'birth_date': fake.date_of_birth(minimum_age=5, maximum_age=18).strftime('%Y-%m-%d'),
                'birth_place': fake.city(),
                'mobile_no': f'{fake.random_number(digits=10)}',
                'address': fake.address()[:100],
                'city': fake.city()[:50],
                'district': fake.city()[:50],
                'standard': selected_standard,
                'roll_no': random.randint(1, 50),
                'section': random.choice(SECTION_CHOICES),
                'academic_year': "1",  # Assuming this is the ID of an existing AcademicYear
                'last_school': fake.company()[:100],
                'admission_std': random.choice(STD_CHOICES),
                'admission_date': random.choice(YEAR_CHOICES),
                'left_school_std': random.choice(STD_CHOICES),
                'left_school_date': fake.date_this_decade().strftime('%Y-%m-%d'),
                'religion': random.choice(RELIGION_CHOICE),
                'category': random.choice(CATEGORY_CHOICE),
                'caste': fake.word()[:50],
                'udise_no': str(fake.unique.random_number(digits=11)),
                'aadhar_no': str(fake.unique.random_number(digits=12)),
                'account_no': str(fake.unique.random_number(digits=10)),
                'name_on_passbook': fake.name()[:100],
                'bank_name': fake.company()[:50],
                'ifsc_code': fake.lexify(text='????0???????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                'bank_address': fake.address()[:100],
                'reason': 'અન્યત્રે જવાથી',
                'note': fake.sentence()[:100],
                'assesment': random.randint(1, 13),
                'progress': random.randint(1, 100),
                'status': random.choice(STATUS_CHOICES)
            }

            try:
                response = requests.post(api_url, json=student_data, headers=headers)
                response.raise_for_status()
                self.stdout.write(self.style.SUCCESS(f'Successfully sent student data for {student_data["first_name"]} {student_data["last_name"]}'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Failed to send data for {student_data["first_name"]} {student_data["last_name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Finished sending {total} dummy student records to the API'))