import pytest
from unittest.mock import Mock

from rest_framework.test import APIClient, APIRequestFactory

from users.models import User


# ============================================================
# API Fixtures
# ============================================================

@pytest.fixture
def api_client():
    """Client API pour les tests de vues."""
    return APIClient()


@pytest.fixture
def api_request_factory():
    """Factory pour créer des requêtes API (utile pour les serializers)."""
    return APIRequestFactory()


# ============================================================
# Mock Fixtures
# ============================================================

@pytest.fixture
def mock_request():
    """Mock d'une requête HTTP."""
    return Mock()


@pytest.fixture
def mock_view():
    """Mock d'une vue DRF."""
    return Mock()


# ============================================================
# User Fixtures
# ============================================================

@pytest.fixture
def superuser(db):
    """Superutilisateur avec tous les droits."""
    return User.objects.create_superuser(
        email="superuser@example.com",
        first_name="Super",
        last_name="User",
        password="superpass123"
    )


@pytest.fixture
def admin_user(db):
    """Utilisateur avec le rôle administrateur (non superuser)."""
    return User.objects.create_user(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password="adminpass123",
        role=User.Role.ADMIN
    )


@pytest.fixture
def veterinarian_user(db):
    """Utilisateur avec le rôle vétérinaire."""
    return User.objects.create_user(
        email="vet@example.com",
        first_name="Vet",
        last_name="User",
        password="vetpass123",
        role=User.Role.VETERINARIAN
    )


@pytest.fixture
def secretary_user(db):
    """Utilisateur avec le rôle secrétaire."""
    return User.objects.create_user(
        email="secretary@example.com",
        first_name="Secretary",
        last_name="User",
        password="secretarypass123",
        role=User.Role.SECRETARY
    )
