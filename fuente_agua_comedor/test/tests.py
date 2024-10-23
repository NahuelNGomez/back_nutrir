from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from .factories import FuenteAguaComedorFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail



@pytest.mark.django_db
def test_fuente_agua_comedor_sin_loguearse(client_unlogged):
    # Get urls
    api_url = reverse('fuente_agua_comedor')

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
def test_fuente_agua_comedor_logueado(client_logged):
    # SetUp
    fuente_agua_comedor = FuenteAguaComedorFactory()

    # Get urls
    api_url = reverse('fuente_agua_comedor')

    # Issue a GET request.
    response = client_logged.get(api_url)

    # Check that the response is 200 OK.
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == fuente_agua_comedor.id

