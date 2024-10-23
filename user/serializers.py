from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import serializers,  exceptions
from .models import UsuarioPersonalizado
from django_nutrir import settings


class CustomLoginSerializer(LoginSerializer):
    username = None
    cuil = None
    email = serializers.EmailField()

    class Meta:
        model = UsuarioPersonalizado
        fields = ['email']

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

	@staticmethod
	def validate_username(username):
		if 'allauth.email' not in settings.INSTALLED_APPS:
			# We don't need to call the all-auth
			# username validator unless its installed
			return username

		from allauth.account.adapter import get_adapter
		username = get_adapter().clean_username(username)
		return username

	class Meta:
		extra_fields = []
		read_only = []
		if hasattr(UsuarioPersonalizado, 'USERNAME_FIELD'):
			extra_fields.append(UsuarioPersonalizado.USERNAME_FIELD)
		if hasattr(UsuarioPersonalizado, 'EMAIL_FIELD'):
			extra_fields.append(UsuarioPersonalizado.EMAIL_FIELD)
		if hasattr(UsuarioPersonalizado, 'first_name'):
			extra_fields.append('first_name')
		if hasattr(UsuarioPersonalizado, 'last_name'):
			extra_fields.append('last_name')
		if hasattr(UsuarioPersonalizado, 'telefono'):
			extra_fields.append('telefono')
		if hasattr(UsuarioPersonalizado, 'picture'):
			read_only.append('picture')
			extra_fields.append('picture')
		if hasattr(UsuarioPersonalizado, 'date_joined'):
			read_only.append('date_joined')
			extra_fields.append('date_joined')

		read_only.append('cuil')
		model = UsuarioPersonalizado
		extra_fields.append('groups')
		read_only.append('groups')

		fields = ('pk', *extra_fields)
		read_only_fields = read_only
