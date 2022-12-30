from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.todo.models import Expectation


class IndexViewTest(SimpleTestCase):
    def test_template_used(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")


class TestEta(TestCase):
    fixtures = ["fixtures.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.joe = User.objects.get(username="johndoe")
        self.jack = User.objects.get(username="jack")
        self.api_client = APIClient()

        self.valid_test_cases = {
            "correct_command": "project#issue at 21:15",
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

    def __assert_client_current_eta(self, user, current):
        self.client.force_login(user)
        data = self.client.get(self.user_eta_url).json()
        if current is None:
            self.assertIsNone(data.get("current"))
        else:
            self.assertDictContainsSubset(current, data.get("current"))

    def __create_new_eta(self, payload, url, status, user=None):
        if user:
            self.client.force_login(user)

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status)
        return response

    def test_eta_creation(self):
        self.__assert_client_current_eta(self.user, current=None)
        self.__assert_client_current_eta(self.joe, current=None)

        self.__create_new_eta({"command": self.valid_test_cases["correct_command"]}, self.user_eta_url, 200, self.user)
        self.__assert_client_current_eta(
            self.user,
            current={"project": {"name": "project"}, "issue": "issue", "user": {"username": self.user.username}},
        )
        self.__assert_client_current_eta(self.joe, None)

        self.__create_new_eta({"command": self.valid_test_cases["correct_command"]}, self.user_eta_url, 400, self.user)

    def test_eta_invalid_commands(self):
        self.client.force_login(self.user)
        eta_before_requests = Expectation.objects.filter(user=self.user).count()

        for key, command in self.valid_test_cases.items():
            with self.subTest(msg=f"{key}: {command}"):
                response = self.client.post(self.user_eta_url)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(eta_before_requests, Expectation.objects.filter(user=self.user).count())
