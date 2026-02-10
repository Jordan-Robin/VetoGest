import pytest

from users.models import User
from users.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    """Tests pour UserSerializer."""

    def test_serialize_user(self, veterinarian_user):
        """Test la sérialisation d'un utilisateur."""
        serializer = UserSerializer(veterinarian_user)
        data = serializer.data

        assert data["email"] == "vet@example.com"
        assert data["first_name"] == "Vet"
        assert data["last_name"] == "User"
        assert data["role"] == "veterinarian"
        assert data["role_display"] == "Vétérinaire"
        assert "password" not in data

    def test_create_user_via_serializer(self, api_request_factory, admin_user):
        """Test la création d'un utilisateur via le serializer."""
        request = api_request_factory.post("/users/")
        request.user = admin_user

        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "Str0ngP@ssword!",
            "role": "secretary"
        }
        serializer = UserSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert user.email == "newuser@example.com"
        assert user.check_password("Str0ngP@ssword!")
        assert user.role == User.Role.SECRETARY

    def test_update_user_via_serializer(self, api_request_factory, veterinarian_user, admin_user):
        """Test la mise à jour d'un utilisateur via le serializer."""
        request = api_request_factory.patch("/users/")
        request.user = admin_user

        data = {"first_name": "Updated", "last_name": "Name"}
        serializer = UserSerializer(
            veterinarian_user,
            data=data,
            partial=True,
            context={"request": request}
        )
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert user.first_name == "Updated"
        assert user.last_name == "Name"

    def test_update_password_via_serializer(self, api_request_factory, veterinarian_user, admin_user):
        """Test la mise à jour du mot de passe via le serializer."""
        request = api_request_factory.patch("/users/")
        request.user = admin_user

        data = {"password": "NewStr0ngP@ss!"}
        serializer = UserSerializer(
            veterinarian_user,
            data=data,
            partial=True,
            context={"request": request}
        )
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert user.check_password("NewStr0ngP@ss!")

    def test_password_is_write_only(self, veterinarian_user):
        """Test que le password n'est pas dans les données sérialisées."""
        serializer = UserSerializer(veterinarian_user)
        assert "password" not in serializer.data

    def test_read_only_fields(self, api_request_factory, admin_user):
        """Test que les champs read_only ne peuvent pas être modifiés."""
        request = api_request_factory.post("/users/")
        request.user = admin_user

        data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Str0ngP@ssword!",
            "role": "secretary",
            "is_staff": True,  # read_only
            "is_active": False,  # read_only
        }
        serializer = UserSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        # Les champs read_only gardent leurs valeurs par défaut
        assert user.is_staff is False
        assert user.is_active is True


@pytest.mark.django_db
class TestUserSerializerRoleValidation:
    """Tests pour la validation du rôle dans UserSerializer."""

    def test_non_superuser_cannot_create_admin(self, api_request_factory, admin_user):
        """Test qu'un non-superuser ne peut pas créer un admin."""
        request = api_request_factory.post("/users/")
        request.user = admin_user  # admin mais pas superuser

        data = {
            "email": "newadmin@example.com",
            "first_name": "New",
            "last_name": "Admin",
            "password": "Str0ngP@ssword!",
            "role": "admin"
        }
        serializer = UserSerializer(data=data, context={"request": request})
        assert not serializer.is_valid()
        assert "role" in serializer.errors

    def test_superuser_can_create_admin(self, api_request_factory, superuser):
        """Test qu'un superuser peut créer un admin."""
        request = api_request_factory.post("/users/")
        request.user = superuser

        data = {
            "email": "newadmin@example.com",
            "first_name": "New",
            "last_name": "Admin",
            "password": "Str0ngP@ssword!",
            "role": "admin"
        }
        serializer = UserSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert user.role == User.Role.ADMIN

    def test_non_superuser_can_create_veterinarian(self, api_request_factory, admin_user):
        """Test qu'un admin peut créer un vétérinaire."""
        request = api_request_factory.post("/users/")
        request.user = admin_user

        data = {
            "email": "newvet@example.com",
            "first_name": "New",
            "last_name": "Vet",
            "password": "Str0ngP@ssword!",
            "role": "veterinarian"
        }
        serializer = UserSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors

    def test_non_superuser_cannot_change_role_to_admin(
        self, api_request_factory, veterinarian_user, admin_user
    ):
        """Test qu'un non-superuser ne peut pas changer un rôle en admin."""
        request = api_request_factory.patch("/users/")
        request.user = admin_user

        data = {"role": "admin"}
        serializer = UserSerializer(
            veterinarian_user,
            data=data,
            partial=True,
            context={"request": request}
        )
        assert not serializer.is_valid()
        assert "role" in serializer.errors


@pytest.mark.django_db
class TestUserSerializerPasswordValidation:
    """Tests pour la validation du mot de passe dans UserSerializer."""

    def test_password_required_on_create(self, api_request_factory, admin_user):
        """Test que le mot de passe est obligatoire à la création."""
        request = api_request_factory.post("/users/")
        request.user = admin_user

        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "role": "secretary"
            # password manquant
        }
        serializer = UserSerializer(data=data, context={"request": request})
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_password_not_required_on_update(self, api_request_factory, veterinarian_user, admin_user):
        """Test que le mot de passe n'est pas obligatoire à la mise à jour."""
        request = api_request_factory.patch("/users/")
        request.user = admin_user

        data = {"first_name": "Updated"}
        serializer = UserSerializer(
            veterinarian_user,
            data=data,
            partial=True,
            context={"request": request}
        )
        assert serializer.is_valid(), serializer.errors
