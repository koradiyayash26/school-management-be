from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests


# run command python manage.py fek_student_data 100 --token=your_token

class Command(BaseCommand):
    help = 'Create and send dummy student data to the API'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of students to be created')
        parser.add_argument('--token', type=str, help='Authentication token for the API')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        token = kwargs['token']
        fake = Faker('en_US')
        api_url = 'http://127.0.0.1:8000/students/add/'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        STD_CHOICES = ['13','1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11','12']
        SECTION_CHOICES = ['A', 'B', 'C', 'D']
        GENDER_CHOICE = ['કુમાર', 'કન્યા']
        RELIGION_CHOICE = ['હિન્દુ', 'જૈન', 'મુસ્લિમ', 'શિખ', 'ખ્રિસ્તી']
        CATEGORY_CHOICE = ['જનરલ', 'ઓ.બી.સી.', 'એસસી/એસટી', 'ઇ.ડબ્લ્યુ.એસ.']
        STATUS_CHOICES = ['ચાલુ', 'પૂર્ણ', 'રદ']

        for _ in range(total):
            student_data = {
                'grno': fake.unique.random_number(digits=6),
                'last_name': fake.last_name(),
                'first_name': fake.first_name(),
                'middle_name': fake.first_name(),
                'mother_name': fake.name_female(),
                'gender': random.choice(GENDER_CHOICE),
                'birth_date': fake.date_of_birth(minimum_age=5, maximum_age=18).strftime('%Y-%m-%d'),
                'birth_place': fake.city(),
                'mobile_no': fake.phone_number(),
                'address': fake.address(),
                'city': fake.city(),
                'district': fake.city(),
                'standard': random.choice(STD_CHOICES),
                'section': random.choice(SECTION_CHOICES),
                'last_school': fake.company(),
                'admission_std': random.choice(STD_CHOICES),
                'admission_date': str(fake.year()),
                'left_school_std': random.choice(STD_CHOICES),
                'left_school_date': fake.date_this_decade().strftime('%Y-%m-%d'),
                'religion': random.choice(RELIGION_CHOICE),
                'category': random.choice(CATEGORY_CHOICE),
                'caste': fake.word(),
                'udise_no': fake.unique.random_number(digits=11),
                'aadhar_no': fake.unique.random_number(digits=12),
                'account_no': fake.unique.random_number(digits=10),
                'name_on_passbook': fake.name(),
                'bank_name': fake.company(),
                'ifsc_code': fake.lexify(text='????0???????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                'bank_address': fake.address(),
                'reason': 'અન્યત્રે જવાથી',
                'note': fake.sentence(),
                'assesment': random.randint(1, 10),
                'progress': random.randint(1, 10),
                'status': random.choice(STATUS_CHOICES)
            }

            try:
                response = requests.post(api_url, json=student_data, headers=headers)
                response.raise_for_status()
                self.stdout.write(self.style.SUCCESS(f'Successfully sent student data for {student_data["first_name"]} {student_data["last_name"]}'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Failed to send data for {student_data["first_name"]} {student_data["last_name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Finished sending {total} dummy student records to the API'))