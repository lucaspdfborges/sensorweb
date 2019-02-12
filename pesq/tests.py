from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from pesq.models import DashData
from pesq.serializers import DashDataSerializer

# tests for views

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_dashdata(experimento="", dado=""):
        if experimento != "" and dado != "":
            DashData.objects.create(experimento=experimento, dado=dado)

    def setUp(self):
        # add test data
        self.create_dashdata("exp1", 1.23)
        self.create_dashdata("exp2", 1.5)
        self.create_dashdata("exp3", 5)
        self.create_dashdata("exp4", 4)


class GetAllDashDataTest(BaseViewTest):

    def test_get_all_dashdata(self):
        """
        This test ensures that all dashdata added in the setUp method
        exist when we make a GET request to the dashdata/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("dashdata-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = DashData.objects.all()
        serialized = DashDataSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
self.assertEqual(response.status_code, status.HTTP_200_OK)
