from django.db import models

class Customer(models.Model):
    last_name = models.CharField("Nom", max_length=100)
    first_name = models.CharField("Prénom", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone_number = models.CharField("Téléphone", max_length=20)

    # Address
    street = models.CharField("Rue", max_length=255)
    zip_code = models.CharField("Code Postal", max_length=10)
    city = models.CharField("Ville", max_length=100)

    # Notes
    archive = models.BooleanField("Archivé", default=False)
    description = models.TextField("Notes médicales/diverses", blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name}"