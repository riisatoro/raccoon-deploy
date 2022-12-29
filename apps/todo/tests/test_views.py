from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from apps.todo.models import Expectation


class IndexViewTest(SimpleTestCase):
    def test_template_used(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")


password = "bsQ^L0E7D^Y8"


class TestEtaCommands(TestCase):
    fixtures = ["fixtures.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.joe = User.objects.get(username="johndoe")
        self.jack = User.objects.get(username="jack")
        self.api_client = APIClient()

        self.valid_test_cases = {
            "correct_command": "project#issue at 21:15",
            "correct_date": "project#issue at 10-12 21:15",
            "correct_verbose": "project#issue at tomorrow 21:15",
        }

        self.invalid_test_cases = {
            "empty_string": "",
            "invalid_command": "unknown command issue at today 12-01 99:99",
            "missing_issue": "project# at 12:00",
            "missing_project": "#issue at 12:00",
            "missing_time": "#issue at 10-10",
            "invalid_time": "project#issue 99:99",
            "invalid_date": "project#issue at 20-01 12:00",
            "invalid_verbose_interval": "project#issue at yesterday 12:00",
            "invalid_verbose_and_date": "project#issue at today 01-01 12:00",
        }

        self.user_eta_url = reverse("user_eta")
        self.opened_eta_url = reverse("user_eta")

    def test_eta_creation(self):
        self.client.force_login(self.user)

        response = self.client.get(self.user_eta_url)
        self.assertDictEqual(response.json(), {"current": None, "closed": []})

        response = self.client.post(self.user_eta_url, data={"command": self.valid_test_cases["correct_command"]})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.user_eta_url)
        data = response.json()
        self.assertIsNotNone(data.get("current"))

        user_expectation = Expectation.objects.filter(user=self.user, project__name="project", issue="issue")
        self.assertEqual(user_expectation.count(), 1)

        expectation_date = user_expectation.first().expected_at
        self.assertEqual(expectation_date.minute, 15)
        self.assertEqual(expectation_date.hour, 21)
        self.assertEqual(expectation_date.date(), timezone.now().date())

        response = self.client.post(self.user_eta_url, data={"command": self.valid_test_cases["correct_command"]})
        self.assertEqual(response.status_code, 400)

    def test_eta_duplicates(self):
        ...

    def test_eta_upgrate(self):
        ...

    def test_eta_close(self):
        ...

    def test_eta_invalid_commands(self):
        self.client.force_login(self.user)
        eta_before_requests = Expectation.objects.filter(user=self.user).count()

        for key, command in self.valid_test_cases.items():
            with self.subTest(msg=f"{key}: {command}"):
                response = self.client.post(self.user_eta_url)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(eta_before_requests, Expectation.objects.filter(user=self.user).count())
