import pytest
from unittest.mock import Mock

from users.permissions import IsAdmin, IsVeterinarian, IsSecretary


@pytest.mark.django_db
class TestIsAdminPermission:
    """Tests pour la permission IsAdmin."""

    def test_admin_has_permission(self, mock_request, mock_view, admin_user):
        """Test qu'un admin a la permission."""
        mock_request.user = admin_user
        permission = IsAdmin()
        assert permission.has_permission(mock_request, mock_view) is True

    def test_superuser_has_permission(self, mock_request, mock_view, superuser):
        """Test qu'un superuser a la permission."""
        mock_request.user = superuser
        permission = IsAdmin()
        assert permission.has_permission(mock_request, mock_view) is True

    def test_veterinarian_denied(self, mock_request, mock_view, veterinarian_user):
        """Test qu'un vétérinaire n'a pas la permission."""
        mock_request.user = veterinarian_user
        permission = IsAdmin()
        assert permission.has_permission(mock_request, mock_view) is False

    def test_secretary_denied(self, mock_request, mock_view, secretary_user):
        """Test qu'un secrétaire n'a pas la permission."""
        mock_request.user = secretary_user
        permission = IsAdmin()
        assert permission.has_permission(mock_request, mock_view) is False

    def test_unauthenticated_denied(self, mock_request, mock_view):
        """Test qu'un utilisateur non authentifié n'a pas la permission."""
        mock_request.user = Mock(is_authenticated=False)
        permission = IsAdmin()
        assert permission.has_permission(mock_request, mock_view) is False


@pytest.mark.django_db
class TestIsVeterinarianPermission:
    """Tests pour la permission IsVeterinarian."""

    def test_veterinarian_has_permission(self, mock_request, mock_view, veterinarian_user):
        """Test qu'un vétérinaire a la permission."""
        mock_request.user = veterinarian_user
        permission = IsVeterinarian()
        assert permission.has_permission(mock_request, mock_view) is True

    def test_superuser_has_permission(self, mock_request, mock_view, superuser):
        """Test qu'un superuser a la permission."""
        mock_request.user = superuser
        permission = IsVeterinarian()
        assert permission.has_permission(mock_request, mock_view) is True

    def test_admin_denied(self, mock_request, mock_view, admin_user):
        """Test qu'un admin n'a pas la permission IsVeterinarian."""
        mock_request.user = admin_user
        permission = IsVeterinarian()
        assert permission.has_permission(mock_request, mock_view) is False

    def test_secretary_denied(self, mock_request, mock_view, secretary_user):
        """Test qu'un secrétaire n'a pas la permission."""
        mock_request.user = secretary_user
        permission = IsVeterinarian()
        assert permission.has_permission(mock_request, mock_view) is False


@pytest.mark.django_db
class TestIsSecretaryPermission:
    """Tests pour la permission IsSecretary."""

    def test_secretary_has_permission(self, mock_request, mock_view, secretary_user):
        """Test qu'un secrétaire a la permission."""
        mock_request.user = secretary_user
        permission = IsSecretary()
        assert permission.has_permission(mock_request, mock_view) is True

    def test_superuser_has_permission(self, mock_request, mock_view, superuser):
        """Test qu'un superuser a la permission."""
        mock_request.user = superuser
        permission = IsSecretary()
        assert permission.has_permission(mock_request, mock_view) is True

    def test_admin_denied(self, mock_request, mock_view, admin_user):
        """Test qu'un admin n'a pas la permission IsSecretary."""
        mock_request.user = admin_user
        permission = IsSecretary()
        assert permission.has_permission(mock_request, mock_view) is False

    def test_veterinarian_denied(self, mock_request, mock_view, veterinarian_user):
        """Test qu'un vétérinaire n'a pas la permission."""
        mock_request.user = veterinarian_user
        permission = IsSecretary()
        assert permission.has_permission(mock_request, mock_view) is False
