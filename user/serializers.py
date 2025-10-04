from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import serializers,  exceptions
from .models import UsuarioPersonalizado
from django_nutrir import settings

print("=== SERIALIZERS.PY CARGADO ===")


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField()

    class Meta:
        model = UsuarioPersonalizado
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        print("=== CUSTOMLOGINSERIALIZER INICIADO ===")
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(
                email=email,
                password=password,
            )
            if not user:
                msg = "Incorrect credentials."
                raise serializers.ValidationError(msg, code="authorization")

        else:
            msg = "No email provided."
            raise exceptions.ValidationError(msg)
        attrs["user"] = user
        return attrs

class UserDetailsSerializer(serializers.ModelSerializer):
	""" Extension de UserDetailsSerializer para que muestre también otros campos cuando te logueas"""

	def __init__(self, *args, **kwargs):
		print("=== USERDETAILSSERIALIZER INICIADO ===")
		super().__init__(*args, **kwargs)

	@staticmethod
	def validate_username(username):
		if 'allauth.email' not in settings.INSTALLED_APPS:
			# We don't need to call the all-auth
			# username validator unless its installed
			return username

		from allauth.account.adapter import get_adapter
		username = get_adapter().clean_username(username)
		return username

	def to_representation(self, instance):
		"""Override para debuggear el teléfono"""
		print("=== DEBUG USERDETAILSSERIALIZER ===")
		print(f"DEBUG - Usuario ID: {instance.pk}")
		print(f"DEBUG - Teléfono en BD: '{instance.telefono}'")
		print(f"DEBUG - Tipo de teléfono: {type(instance.telefono)}")
		print(f"DEBUG - Longitud teléfono: {len(instance.telefono) if instance.telefono else 'None'}")
		
		data = super().to_representation(instance)
		print(f"DEBUG - Teléfono serializado: '{data.get('telefono')}'")
		print("=== FIN DEBUG ===")
		return data
	
	def get_telefono(self, obj):
		"""Método específico para el campo teléfono"""
		print(f"DEBUG - get_telefono llamado para usuario {obj.pk}")
		print(f"DEBUG - Valor del teléfono: '{obj.telefono}'")
		return obj.telefono

	class Meta:
		model = UsuarioPersonalizado
		fields = ('pk', 'email', 'first_name', 'last_name', 'telefono', 'picture', 'groups')
		read_only_fields = ('pk', 'picture', 'groups')
