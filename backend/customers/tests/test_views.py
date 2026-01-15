from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from customers.models import Customer


class CustomerApiTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            last_name="Dupont",
            first_name="Jean",
            email="jean@dupont.com",
            phone_number="0123456789",
            street="10 rue de la Paix",
            zip_code="75000",
            city="Paris",
            archive=False,
            description="Client régulier"
        )
        self.list_url = reverse('customer-list')

    def test_get_all_customers(self):
        """Vérifie que la liste des clients est accessible et en CamelCase."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]['lastName'], "Dupont")

    def test_create_customer_invalid_data(self):
        """Vérifie que l'API renvoie une erreur 400 si l'email est vide."""
        data = {
            "lastName": "Durand",
            "firstName": "Paul",
            "email": "",
            "phoneNumber": "0987654321",
            "street": "20 avenue des Champs",
            "zipCode": "75008",
            "city": "Paris",
            "archive": False,
            "description": "Nouveau client"
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
