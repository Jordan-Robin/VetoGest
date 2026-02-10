import pytest

from customers.models import Customer
from customers.serializers import CustomerSerializer


@pytest.mark.django_db
class TestCustomerSerializer:
    """Tests pour CustomerSerializer."""

    def test_serialize_customer(self, customer):
        """Test la sérialisation d'un client."""
        serializer = CustomerSerializer(customer)
        data = serializer.data

        assert data["last_name"] == "Dupont"
        assert data["first_name"] == "Jean"
        assert data["email"] == "jean@dupont.com"
        assert data["phone_number"] == "0123456789"
        assert data["archive"] is False

    def test_create_customer_via_serializer(self):
        """Test la création d'un client via le serializer."""
        data = {
            "last_name": "Martin",
            "first_name": "Marie",
            "email": "marie@martin.com",
            "phone_number": "0987654321",
            "street": "20 avenue des Champs",
            "zip_code": "75008",
            "city": "Paris",
            "archive": False,
            "description": "Nouveau client"
        }
        serializer = CustomerSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        customer = serializer.save()
        assert customer.last_name == "Martin"
        assert customer.email == "marie@martin.com"

    def test_update_customer_via_serializer(self, customer):
        """Test la mise à jour d'un client via le serializer."""
        data = {"first_name": "Pierre", "last_name": "Dupont"}
        serializer = CustomerSerializer(customer, data=data, partial=True)
        assert serializer.is_valid(), serializer.errors

        updated_customer = serializer.save()
        assert updated_customer.first_name == "Pierre"

    def test_read_only_fields(self):
        """Test que les champs read_only ne peuvent pas être modifiés."""
        data = {
            "last_name": "Test",
            "first_name": "User",
            "email": "test@example.com",
            "phone_number": "0123456789",
            "street": "Rue Test",
            "zip_code": "75000",
            "city": "Paris",
            "created_at": "2020-01-01T00:00:00Z",  # read_only
            "updated_at": "2020-01-01T00:00:00Z",  # read_only
        }
        serializer = CustomerSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        customer = serializer.save()
        # Les champs read_only sont ignorés et générés automatiquement
        assert customer.created_at is not None
        assert str(customer.created_at.year) != "2020"

    def test_email_required(self):
        """Test que l'email est obligatoire."""
        data = {
            "last_name": "Test",
            "first_name": "User",
            "email": "",
            "phone_number": "0123456789",
            "street": "Rue Test",
            "zip_code": "75000",
            "city": "Paris"
        }
        serializer = CustomerSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors
