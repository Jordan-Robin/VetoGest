import pytest
from django.db import IntegrityError

from customers.models import Customer


@pytest.mark.django_db
class TestCustomerModel:
    """Tests pour le modèle Customer."""

    def test_create_customer(self):
        """Test la création d'un client."""
        customer = Customer.objects.create(
            last_name="Dupont",
            first_name="Jean",
            email="jean@dupont.com",
            phone_number="0123456789",
            street="10 rue de la Paix",
            zip_code="75000",
            city="Paris"
        )
        assert customer.last_name == "Dupont"
        assert customer.first_name == "Jean"
        assert customer.email == "jean@dupont.com"
        assert customer.archive is False
        assert customer.created_at is not None
        assert customer.updated_at is not None

    def test_customer_str_representation(self):
        """Test la représentation string d'un client (NOM Prénom)."""
        customer = Customer.objects.create(
            last_name="dupont",
            first_name="Jean",
            email="jean@dupont.com",
            phone_number="0123456789",
            street="10 rue de la Paix",
            zip_code="75000",
            city="Paris"
        )
        assert str(customer) == "DUPONT Jean"

    def test_email_unique_constraint(self):
        """Test que l'email est unique."""
        Customer.objects.create(
            last_name="Dupont",
            first_name="Jean",
            email="unique@example.com",
            phone_number="0123456789",
            street="10 rue de la Paix",
            zip_code="75000",
            city="Paris"
        )
        with pytest.raises(IntegrityError):
            Customer.objects.create(
                last_name="Martin",
                first_name="Marie",
                email="unique@example.com",
                phone_number="0987654321",
                street="20 avenue des Champs",
                zip_code="75008",
                city="Lyon"
            )

    def test_customer_default_archive_is_false(self):
        """Test que archive est False par défaut."""
        customer = Customer.objects.create(
            last_name="Dupont",
            first_name="Jean",
            email="jean@dupont.com",
            phone_number="0123456789",
            street="10 rue de la Paix",
            zip_code="75000",
            city="Paris"
        )
        assert customer.archive is False

    def test_customer_ordering(self):
        """Test que les clients sont triés par nom puis prénom."""
        Customer.objects.create(
            last_name="Zebra",
            first_name="Anna",
            email="anna@zebra.com",
            phone_number="0123456789",
            street="Rue A",
            zip_code="75000",
            city="Paris"
        )
        Customer.objects.create(
            last_name="Alpha",
            first_name="Zoe",
            email="zoe@alpha.com",
            phone_number="0123456789",
            street="Rue B",
            zip_code="75000",
            city="Paris"
        )
        Customer.objects.create(
            last_name="Alpha",
            first_name="Anna",
            email="anna@alpha.com",
            phone_number="0123456789",
            street="Rue C",
            zip_code="75000",
            city="Paris"
        )

        customers = list(Customer.objects.all())
        assert customers[0].last_name == "Alpha"
        assert customers[0].first_name == "Anna"
        assert customers[1].last_name == "Alpha"
        assert customers[1].first_name == "Zoe"
        assert customers[2].last_name == "Zebra"
