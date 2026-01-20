from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
            'role_display',
            'birth_date',
            'phone_number',
            'street',
            'city',
            'zip_code',
            'is_active',
            'is_staff',
            'date_joined',
            'updated_at',
            'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'updated_at', 'last_login', 'is_staff', 'is_active']

    def validate_role(self, value):
        """Empêche la création/modification vers le rôle ADMIN sauf par un superuser."""
        request = self.context.get('request')
        if value == User.Role.ADMIN:
            if not request or not request.user or not request.user.is_superuser:
                raise serializers.ValidationError(
                    "Seul un superutilisateur peut attribuer le rôle administrateur."
                )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance