from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'email', 'phone_number', 'city', 'archive')
    list_filter = ('archive', 'city')
    search_fields = ('lastname', 'firstname', 'email', 'phone_number', 'city')
    ordering = ('lastname', 'firstname')
