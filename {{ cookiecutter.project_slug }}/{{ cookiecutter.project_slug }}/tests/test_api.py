from unittest import mock

from {{cookiecutter.project_slug}} import app
from {{cookiecutter.project_slug}}.models import User


client = app.test_client()


def test_compute_sent_to_queue():
    response = client.get('/compute')
    assert response.status_code == 200
    assert response.json == {'message': 'Successfully sent to queue.'}


def test_404():
    response = client.get('/api/echoes')
    assert response.status_code == 404


@mock.patch('{{cookiecutter.project_slug}}.commons.get_app_version', return_value='1.0')
def test_healthcheck_readiness(_mocked_version):
    response = client.get('/health-check/readiness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'ready', 'app_version', 'app_type'}


@mock.patch('{{cookiecutter.project_slug}}.commons.get_app_version', return_value='1.0')
def test_healthcheck_liveness(_mocked_version):
    response = client.get('/health-check/liveness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'live', 'version', 'timestamp'}


class TestUserAPI:
    def submit_create_user_request(self, test_client):
        payload = {
            'username': 'jean_luc_picard',
            'email': 'jlp@startrek.com',
            'password': '12345678',
        }

        response = test_client.post('/user', json=payload)
        return response

    def submit_login_request(
        self, test_client, email: str = 'jlp@startrek.com', password: str = '12345678'
    ):
        payload = {'email': email, 'password': password}

        response = test_client.post('/login', json=payload)
        return response

    def test_create_user(self, test_client, db_session):
        response = self.submit_create_user_request(test_client=test_client)
        assert response.status_code == 201

        new_user_uuid = response.json['uuid']
        assert isinstance(new_user_uuid, str)

    def test_login_successful(self, test_client, db_session):

        login_response = self.submit_login_request(test_client=test_client)
        assert login_response.status_code == 200

        access_token = login_response.json['access_token']
        refresh_token = login_response.json['refresh_token']

        assert access_token is not None
        assert refresh_token is not None

    def test_get_user_data_after_login(self, test_client, db_session):
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']

        headers = {'Authorization': f'Bearer {access_token}'}
        response = test_client.get('/user', headers=headers)
        assert response.status_code == 200

        user_instance = User.get_by(uuid=new_user_uuid)

        expected_json_response = {
            'uuid': str(user_instance.uuid),
            'username': user_instance.username,
            'email': user_instance.email,
        }
        assert response.json == expected_json_response

    def test_get_new_jwt_temporary_token_when_logged_in(self, test_client, db_session):
        _ = self.submit_create_user_request(test_client=test_client)

        login_response = self.submit_login_request(test_client=test_client)
        assert login_response.status_code == 200

        access_token = login_response.json['access_token']
        refresh_token = login_response.json['refresh_token']

        headers = {'Authorization': f'Bearer {refresh_token}'}
        response = test_client.post('/token/new', headers=headers)
        assert response.status_code == 200

        new_access_token = response.json['access_token']
        assert new_access_token is not None
        assert new_access_token != access_token

    def test_update_user_successfully(self, test_client, db_session):
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']

        headers = {'Authorization': f'Bearer {access_token}'}
        new_email = 'jean_luc_picard.captain@startrek.com'
        new_password = 'resistance-is-futile'
        payload = {'email': new_email, 'password': new_password}
        update_response = test_client.patch('/user', headers=headers, json=payload)
        assert update_response.status_code == 200

        expected_json_response = {
            'email': new_email,
            'password': 'SUCCESSFULLY CHANGED',
            'uuid': new_user_uuid,
        }
        assert update_response.json == expected_json_response

        user_instance = User.get_by(email=new_email)
        assert str(user_instance.uuid) == new_user_uuid

        # re-attempt login with updated email and password should get new access token
        new_login_response = self.submit_login_request(
            test_client=test_client, email=new_email, password=new_password
        )
        assert new_login_response.status_code == 200

        new_access_token = new_login_response.json['access_token']
        assert new_access_token is not None
        assert new_access_token != access_token
