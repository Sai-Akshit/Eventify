from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Participant

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('main:home')
        self.login_url = reverse('main:login')
        self.logout_url = reverse('main:logout')
        self.upload_url = reverse('main:upload_file')
        self.verify_url = reverse('main:verifyUser')
        self.download_url = reverse('main:download_data')
        self.register_url = reverse('main:register')

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )

        self.participant = Participant.objects.create(
            name='Test Participant',
            email='testparticipant@test.com',
            regNum='TEST1234',
            course='Test Course',
            branch='Test Branch',
            year='2'
        )

        self.client.login(username='testuser', password='testpass')

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('main:verifyUser'))

    def test_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/login')

    def test_upload_file_view(self):
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/upload.html')

        with open('test_data.xlsx', 'rb') as f:
            response = self.client.post(self.upload_url, {'excel_file': f})
            self.assertRedirects(response, reverse('main:home'))

    def test_verifyUser_view(self):
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/scan.html')

        response = self.client.post(self.verify_url, {'regNo': 'TEST1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User verified successfully')

    def test_download_data_view(self):
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_register_user_access(self):
        data = {
            'name': 'John Doe',
            'email': 'johndoe@gitam.in',
            'regno': 'ABC123',
            'course': 'Computer Science',
            'branch': 'CSE',
            'year': '3',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/success.html')
        self.assertEqual(Participant.objects.count(), 1)
        participant = Participant.objects.first()
        self.assertEqual(participant.name, 'John Doe')
        self.assertEqual(participant.email, 'johndoe@example.com')
        self.assertEqual(participant.regNum, 'ABC123')
        self.assertEqual(participant.course, 'Computer Science')
        self.assertEqual(participant.branch, 'CSE')
        self.assertEqual(participant.year, '3')

