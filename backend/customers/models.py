from django.db import models

class Customer(models.Model):
    lastname = models.CharField("Nom", max_length=100)
    firstname = models.CharField("Prénom", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone_number = models.CharField("Téléphone", max_length=20)

    # Address
    street = models.CharField("Rue", max_length=255)
    zipcode = models.CharField("Code Postal", max_length=10)
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
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return f"{self.lastname.upper()} {self.firstname}"