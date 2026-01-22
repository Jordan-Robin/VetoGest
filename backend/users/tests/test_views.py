import pytest
from rest_framework import status

from users.models import User


@pytest.mark.django_db
class TestUserViewSetList:
    """Tests pour la liste des utilisateurs."""

    def test_unauthenticated_user_cannot_list_users(self, api_client):
        """Test qu'un utilisateur non authentifié ne peut pas lister les users."""
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_list_users(self, api_client, veterinarian_user):
        """Test qu'un utilisateur authentifié peut lister les users."""
        api_client.force_authenticate(user=veterinarian_user)
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_list_returns_all_users(self, api_client, admin_user, veterinarian_user, secretary_user):
        """Test que la liste retourne tous les utilisateurs."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3


@pytest.mark.django_db
class TestUserViewSetRetrieve:
    """Tests pour la récupération d'un utilisateur."""

    def test_authenticated_user_can_retrieve_user(self, api_client, veterinarian_user, admin_user):
        """Test qu'un utilisateur authentifié peut voir un user."""
        api_client.force_authenticate(user=veterinarian_user)
        response = api_client.get(f"/api/users/{admin_user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == admin_user.email


@pytest.mark.django_db
class TestUserViewSetCreate:
    """Tests pour la création d'utilisateurs."""

    def test_unauthenticated_user_cannot_create(self, api_client):
        """Test qu'un utilisateur non authentifié ne peut pas créer."""
        data = {
            "email": "new@example.com",
            "firstName": "New",
            "lastName": "User",
            "password": "Str0ngP@ss!",
            "role": "secretary"
        }
        response = api_client.post("/api/users/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_veterinarian_cannot_create_user(self, api_client, veterinarian_user):
        """Test qu'un vétérinaire ne peut pas créer d'utilisateur."""
        api_client.force_authenticate(user=veterinarian_user)
        data = {
            "email": "new@example.com",
            "firstName": "New",
            "lastName": "User",
            "password": "Str0ngP@ss!",
            "role": "secretary"
        }
        response = api_client.post("/api/users/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_secretary_cannot_create_user(self, api_client, secretary_user):
        """Test qu'un secrétaire ne peut pas créer d'utilisateur."""
        api_client.force_authenticate(user=secretary_user)
        data = {
            "email": "new@example.com",
            "firstName": "New",
            "lastName": "User",
            "password": "Str0ngP@ss!",
            "role": "secretary"
        }
        response = api_client.post("/api/users/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_create_user(self, api_client, admin_user):
        """Test qu'un admin peut créer un utilisateur."""
        api_client.force_authenticate(user=admin_user)
        data = {
            "email": "new@example.com",
            "firstName": "New",
            "lastName": "User",
            "password": "Str0ngP@ss!",
            "role": "secretary"
        }
        response = api_client.post("/api/users/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="new@example.com").exists()

    def test_admin_cannot_create_admin_user(self, api_client, admin_user):
        """Test qu'un admin non-superuser ne peut pas créer un autre admin."""
        api_client.force_authenticate(user=admin_user)
        data = {
            "email": "newadmin@example.com",
            "firstName": "New",
            "lastName": "Admin",
            "password": "Str0ngP@ss!",
            "role": "admin"
        }
        response = api_client.post("/api/users/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_superuser_can_create_admin_user(self, api_client, superuser):
        """Test qu'un superuser peut créer un admin."""
        api_client.force_authenticate(user=superuser)
        data = {
            "email": "newadmin@example.com",
            "firstName": "New",
            "lastName": "Admin",
            "password": "Str0ngP@ss!",
            "role": "admin"
        }
        response = api_client.post("/api/users/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newadmin@example.com", role=User.Role.ADMIN).exists()

    def test_create_user_without_password_fails(self, api_client, admin_user):
        """Test que la création sans mot de passe échoue."""
        api_client.force_authenticate(user=admin_user)
        data = {
            "email": "new@example.com",
            "firstName": "New",
            "lastName": "User",
            "role": "secretary"
            # password manquant
        }
        response = api_client.post("/api/users/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data


@pytest.mark.django_db
class TestUserViewSetUpdate:
    """Tests pour la mise à jour d'utilisateurs."""

    def test_veterinarian_cannot_update_user(self, api_client, veterinarian_user, secretary_user):
        """Test qu'un vétérinaire ne peut pas modifier un utilisateur."""
        api_client.force_authenticate(user=veterinarian_user)
        data = {"firstName": "Updated"}
        response = api_client.patch(f"/api/users/{secretary_user.id}/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_user(self, api_client, admin_user, veterinarian_user):
        """Test qu'un admin peut modifier un utilisateur."""
        api_client.force_authenticate(user=admin_user)
        data = {"firstName": "Updated"}
        response = api_client.patch(f"/api/users/{veterinarian_user.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        veterinarian_user.refresh_from_db()
        assert veterinarian_user.first_name == "Updated"

    def test_admin_cannot_change_role_to_admin(self, api_client, admin_user, veterinarian_user):
        """Test qu'un admin ne peut pas promouvoir en admin."""
        api_client.force_authenticate(user=admin_user)
        data = {"role": "admin"}
        response = api_client.patch(f"/api/users/{veterinarian_user.id}/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserViewSetDelete:
    """Tests pour la suppression d'utilisateurs."""

    def test_veterinarian_cannot_delete_user(self, api_client, veterinarian_user, secretary_user):
        """Test qu'un vétérinaire ne peut pas supprimer un utilisateur."""
        api_client.force_authenticate(user=veterinarian_user)
        response = api_client.delete(f"/api/users/{secretary_user.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_non_admin_user(self, api_client, admin_user, veterinarian_user):
        """Test qu'un admin peut supprimer un non-admin."""
        api_client.force_authenticate(user=admin_user)
        user_id = veterinarian_user.id
        response = api_client.delete(f"/api/users/{user_id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user_id).exists()

    def test_admin_cannot_delete_admin_user(self, api_client, admin_user):
        """Test qu'un admin non-superuser ne peut pas supprimer un admin."""
        other_admin = User.objects.create_user(
            email="other_admin@example.com",
            first_name="Other",
            last_name="Admin",
            password="pass123",
            role=User.Role.ADMIN
        )
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f"/api/users/{other_admin.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superuser_can_delete_admin_user(self, api_client, superuser, admin_user):
        """Test qu'un superuser peut supprimer un admin."""
        api_client.force_authenticate(user=superuser)
        user_id = admin_user.id
        response = api_client.delete(f"/api/users/{user_id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user_id).exists()
