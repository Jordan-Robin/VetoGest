import pytest
from rest_framework import status

from customers.models import Customer


@pytest.mark.django_db
class TestCustomerViewSetList:
    """Tests pour la liste des clients."""

    def test_unauthenticated_user_cannot_list_customers(self, api_client):
        """Test qu'un utilisateur non authentifié ne peut pas lister les clients."""
        response = api_client.get("/api/customers/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_list_customers(self, api_client, veterinarian_user, customer):
        """Test qu'un utilisateur authentifié peut lister les clients."""
        api_client.force_authenticate(user=veterinarian_user)
        response = api_client.get("/api/customers/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_returns_customers_in_camel_case(self, api_client, admin_user, customer):
        """Test que la liste retourne les données en camelCase (au niveau JSON)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get("/api/customers/")
        assert response.status_code == status.HTTP_200_OK

        json_data = response.json()
        assert "lastName" in json_data[0]
        assert "firstName" in json_data[0]
        assert "phoneNumber" in json_data[0]


@pytest.mark.django_db
class TestCustomerViewSetRetrieve:
    """Tests pour la récupération d'un client."""

    def test_authenticated_user_can_retrieve_customer(self, api_client, veterinarian_user, customer):
        """Test qu'un utilisateur authentifié peut voir un client."""
        api_client.force_authenticate(user=veterinarian_user)
        response = api_client.get(f"/api/customers/{customer.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == customer.email


@pytest.mark.django_db
class TestCustomerViewSetCreate:
    """Tests pour la création de clients."""

    def test_unauthenticated_user_cannot_create(self, api_client, customer_data):
        """Test qu'un utilisateur non authentifié ne peut pas créer."""
        response = api_client.post("/api/customers/", customer_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_create_customer(self, api_client, admin_user, customer_data):
        """Test qu'un utilisateur authentifié peut créer un client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post("/api/customers/", customer_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.filter(email="marie@martin.com").exists()

    def test_create_customer_with_invalid_email(self, api_client, admin_user):
        """Test que la création avec un email invalide échoue."""
        api_client.force_authenticate(user=admin_user)
        data = {
            "lastName": "Test",
            "firstName": "User",
            "email": "",
            "phoneNumber": "0123456789",
            "street": "Rue Test",
            "zipCode": "75000",
            "city": "Paris"
        }
        response = api_client.post("/api/customers/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_create_customer_with_duplicate_email(self, api_client, admin_user, customer):
        """Test que la création avec un email dupliqué échoue."""
        api_client.force_authenticate(user=admin_user)
        data = {
            "lastName": "Autre",
            "firstName": "Client",
            "email": customer.email,  # email déjà utilisé
            "phoneNumber": "0999999999",
            "street": "Autre rue",
            "zipCode": "69000",
            "city": "Lyon"
        }
        response = api_client.post("/api/customers/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCustomerViewSetUpdate:
    """Tests pour la mise à jour de clients."""

    def test_authenticated_user_can_update_customer(self, api_client, admin_user, customer):
        """Test qu'un utilisateur authentifié peut modifier un client."""
        api_client.force_authenticate(user=admin_user)
        data = {"firstName": "Pierre"}
        response = api_client.patch(f"/api/customers/{customer.id}/", data, format="json")
        assert response.status_code == status.HTTP_200_OK
        customer.refresh_from_db()
        assert customer.first_name == "Pierre"

    def test_can_archive_customer(self, api_client, admin_user, customer):
        """Test qu'on peut archiver un client."""
        api_client.force_authenticate(user=admin_user)
        data = {"archive": True}
        response = api_client.patch(f"/api/customers/{customer.id}/", data, format="json")
        assert response.status_code == status.HTTP_200_OK
        customer.refresh_from_db()
        assert customer.archive is True


@pytest.mark.django_db
class TestCustomerViewSetDelete:
    """Tests pour la suppression de clients."""

    def test_unauthenticated_user_cannot_delete(self, api_client, customer):
        """Test qu'un utilisateur non authentifié ne peut pas supprimer."""
        response = api_client.delete(f"/api/customers/{customer.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_delete_customer(self, api_client, admin_user, customer):
        """Test qu'un utilisateur authentifié peut supprimer un client."""
        api_client.force_authenticate(user=admin_user)
        customer_id = customer.id
        response = api_client.delete(f"/api/customers/{customer_id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Customer.objects.filter(id=customer_id).exists()
