from unittest import mock

from {{ cookiecutter.project_slug }} import app

client = app.test_client()


def test_compute_sent_to_queue():
    response = client.get('/compute')
    assert response.status_code == 200
    assert response.json == {"message": "Successfully sent to queue."}


def test_404():
    response = client.get('/api/echoes')
    assert response.status_code == 404


@mock.patch('{{ cookiecutter.project_slug }}.commons.get_app_version', return_value='1.0')
def test_healthcheck_readiness(_mocked_version):
    response = client.get('/health-check/readiness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'ready', 'app_version', 'app_type'}


@mock.patch('{{ cookiecutter.project_slug }}.commons.get_app_version', return_value='1.0')
def test_healthcheck_liveness(_mocked_version):
    response = client.get('/health-check/liveness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'live', 'version', 'timestamp'}
