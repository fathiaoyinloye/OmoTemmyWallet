from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
# Create your tests here.

from .models import User

class TestRegister(TestCase):
    def test_signup_returns_201(self):
        url = reverse("register")
        data = {
        "first_name": "gvghhb",
        "last_name": "hgghjk",
        "username": "Ex_Nhjnhjkel",
        "email": "fathiaoyinloye21@gmail.com",
        "phone": "67892745328",
        "password": "dcjjdjdjj12"

        }
        response = self.client.post(url, data , format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_returns_404(self):
        url = reverse("register")
        data = {
        "first_name": "gvghhb",
        "last_name": "hgghjk",
        "username": "Ex_Nhjnhjkel",
        "email": "fathiaoyinloy",
        "phone": "67892745328",
        "password": "dcjjdjdjj12"

        }
        response = self.client.post(url, data , format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class TestLogin(TestCase):
    def setUp(self):
        self.url = reverse("register")
        self.data = {
            "first_name": "gvghhb",
            "last_name": "hgghjk",
            "username": "Ex_Nhjnhjkel",
            "email": "fathiaoyinloye21@gmail.com",
            "phone": "67892745328",
            "password": "dcjjdjdjj12"

        }

    def test_login_returns_200(self):

        response = self.client.post(self.url, self.data , format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login_url = reverse("login")
        login_data = {
            "email": "fathiaoyinloye21@gmail.com",
            "password": "dcjjdjdjj12"

        }
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)


    def test_signup_returns_404(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_url = reverse("login")
        login_data = {
            "email": "fathiaooye21@gmail.com",
            "password": "dcjjdjdjj12"

        }
        login_response = self.client.post(login_url, login_data , format="json")
        self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)


