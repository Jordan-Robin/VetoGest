import pytest
from django.db import IntegrityError

from users.models import User


@pytest.mark.django_db
class TestUserModel:
    """Tests pour le modèle User."""

    def test_create_user(self):
        """Test la création d'un utilisateur standard."""
        user = User.objects.create_user(
            email="test@example.com",
            first_name="Jean",
            last_name="Dupont",
            password="testpass123",
            role=User.Role.VETERINARIAN
        )
        assert user.email == "test@example.com"
        assert user.first_name == "Jean"
        assert user.last_name == "Dupont"
        assert user.role == User.Role.VETERINARIAN
        assert user.check_password("testpass123")
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_without_email_raises_error(self):
        """Test qu'un utilisateur sans email lève une erreur."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(
                email="",
                first_name="Jean",
                last_name="Dupont",
                password="testpass123"
            )

    def test_create_user_normalizes_email(self):
        """Test que l'email est normalisé."""
        user = User.objects.create_user(
            email="Test@EXAMPLE.COM",
            first_name="Jean",
            last_name="Dupont",
            password="testpass123",
            role=User.Role.SECRETARY
        )
        assert user.email == "Test@example.com"

    def test_create_superuser(self):
        """Test la création d'un superutilisateur."""
        admin = User.objects.create_superuser(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            password="adminpass123"
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.role == User.Role.ADMIN

    def test_create_superuser_without_is_staff_raises_error(self):
        """Test qu'un superuser sans is_staff lève une erreur."""
        with pytest.raises(ValueError, match="Superuser must have is_staff=True"):
            User.objects.create_superuser(
                email="admin@example.com",
                first_name="Admin",
                last_name="User",
                password="adminpass123",
                is_staff=False
            )

    def test_create_superuser_without_is_superuser_raises_error(self):
        """Test qu'un superuser sans is_superuser lève une erreur."""
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True"):
            User.objects.create_superuser(
                email="admin@example.com",
                first_name="Admin",
                last_name="User",
                password="adminpass123",
                is_superuser=False
            )

    def test_create_superuser_with_wrong_role_raises_error(self):
        """Test qu'un superuser avec un rôle non-admin lève une erreur."""
        with pytest.raises(ValueError, match="Superuser must have role=ADMIN"):
            User.objects.create_superuser(
                email="admin@example.com",
                first_name="Admin",
                last_name="User",
                password="adminpass123",
                role=User.Role.VETERINARIAN
            )

    def test_email_unique_constraint(self):
        """Test que l'email est unique."""
        User.objects.create_user(
            email="unique@example.com",
            first_name="Jean",
            last_name="Dupont",
            password="testpass123",
            role=User.Role.SECRETARY
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="unique@example.com",
                first_name="Marie",
                last_name="Martin",
                password="testpass456",
                role=User.Role.SECRETARY
            )

    def test_user_str_representation(self):
        """Test la représentation string d'un utilisateur."""
        user = User.objects.create_user(
            email="test@example.com",
            first_name="Jean",
            last_name="Dupont",
            password="testpass123",
            role=User.Role.VETERINARIAN
        )
        assert str(user) == "Jean Dupont - test@example.com"


@pytest.mark.django_db
class TestUserRoleProperties:
    """Tests pour les propriétés de rôle."""

    def test_is_admin_property(self, admin_user):
        """Test la propriété is_admin."""
        assert admin_user.is_admin is True
        assert admin_user.is_veterinarian is False
        assert admin_user.is_secretary is False

    def test_is_veterinarian_property(self, veterinarian_user):
        """Test la propriété is_veterinarian."""
        assert veterinarian_user.is_admin is False
        assert veterinarian_user.is_veterinarian is True
        assert veterinarian_user.is_secretary is False

    def test_is_secretary_property(self, secretary_user):
        """Test la propriété is_secretary."""
        assert secretary_user.is_admin is False
        assert secretary_user.is_veterinarian is False
        assert secretary_user.is_secretary is True
