from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone_number', 'city', 'archive')
    list_filter = ('archive', 'city')
    search_fields = ('last_name', 'first_name', 'email', 'phone_number', 'city')
    ordering = ('last_name', 'first_name')
