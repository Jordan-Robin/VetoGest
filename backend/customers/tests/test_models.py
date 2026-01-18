from django.test import TestCase
from customers.models import Customer


class CustomerModelTest(TestCase):
    def test_customer_creation_and_str(self):
        """Vérifie que le client est bien créé et que __str__ fonctionne."""
        customer = Customer.objects.create(
            last_name="dupont",
            first_name="Jean",
            email="jean@dupont.com",
            phone_number="0123456789",
            street="10 rue de la Paix",
            zip_code="75000",
            city="Paris",
            archive=False,
            description="Client régulier"
        )

        self.assertEqual(str(customer), "DUPONT Jean")
        self.assertEqual(Customer.objects.count(), 1)