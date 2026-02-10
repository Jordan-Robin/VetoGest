from rest_framework import serializers

from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'archive': {
                'error_messages': {
                    'invalid': 'Cette valeur doit être un booléen (true ou false).'
                }
            }
        }