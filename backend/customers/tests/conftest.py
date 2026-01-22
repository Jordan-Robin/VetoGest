import pytest
from unittest.mock import Mock

from rest_framework.test import APIClient, APIRequestFactory

from customers.models import Customer
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


# ============================================================
# Customer Fixtures
# ============================================================

@pytest.fixture
def customer(db):
    """Un client de test."""
    return Customer.objects.create(
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


@pytest.fixture
def customer_data():
    """Données pour créer un nouveau client."""
    return {
        "lastName": "Martin",
        "firstName": "Marie",
        "email": "marie@martin.com",
        "phoneNumber": "0987654321",
        "street": "20 avenue des Champs",
        "zipCode": "75008",
        "city": "Paris",
        "archive": False,
        "description": "Nouveau client"
    }
