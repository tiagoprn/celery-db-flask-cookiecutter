from {{ cookiecutter.project_slug }} import app

client = app.test_client()


def test_sucessfull_echo():
    response = client.get('/api/echo/john')
    assert response.status_code == 200
    assert response.json == {'value': 'john'}


def test_404():
    response = client.get('/api/echoes')
    assert response.status_code == 404
