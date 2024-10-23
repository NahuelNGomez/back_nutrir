from datetime import datetime
import pytest
from django.core.exceptions import ValidationError
from .factories import LocalidadFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

@pytest.mark.django_db
def test_localidad_sin_loguearse(client_unlogged):
    # Get urls
    api_url = reverse('localidades')

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
def test_localiad_logueado(client_logged):
    # SetUp
    localidad = LocalidadFactory()

    # Get urls
    api_url = reverse('localidades')

    # Issue a GET request.
    response = client_logged.get(api_url)

    # Check that the response is 200 OK.
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == localidad.id

@pytest.mark.django_db
def test_Localidades_gobiernoLocalDeptoProvincia_sin_loguearse(client_unlogged):
    # Get urls
    localidad = LocalidadFactory()
    api_url = reverse('LocalidadGobernoLocaldepartamentoProvincia',kwargs={'id_p': localidad.provincia.id, 'id_d': localidad.departamento.id,'id_gl': localidad.gobierno_local.id })

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
def test_localidad_gobiernoLocalDeptoProvincia_logueado(client_logged):
    # SetUp
    localidad = LocalidadFactory()

    # Get urls
    api_url = reverse('LocalidadGobernoLocaldepartamentoProvincia', kwargs={'id_p': localidad.provincia.id, 'id_d': localidad.departamento.id,'id_gl': localidad.gobierno_local.id })

    # Issue a GET request.
    response = client_logged.get(api_url)

    # Check that the response is 200 OK.
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['provincia'] == localidad.provincia.id and response.data[0]['departamento'] == localidad.departamento.id and response.data[0]['gobierno_local'] == localidad.gobierno_local.id
