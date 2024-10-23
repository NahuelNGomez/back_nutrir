from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from .factories import ServicioComedorFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail



@pytest.mark.django_db
def test_servicio_comedores_sin_loguearse(client_unlogged):
    # Get urls
    api_url = reverse('servicio_comedor')

    # Issue a GET request.
    response = client_unlogged.get(api_url)

    # Check that the response is 403 OK.
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': ErrorDetail(
            string='Las credenciales de autenticación no se proveyeron.',
            code='not_authenticated',
        )
    }


@pytest.mark.django_db
def test_servicio_comedores_logueado(client_logged):
    # SetUp
    servicio_comedor = ServicioComedorFactory()

    # Get urls
    api_url = reverse('servicio_comedor')

    # Issue a GET request.
    response = client_logged.get(api_url)

    # Check that the response is 200 OK.
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == servicio_comedor.id

