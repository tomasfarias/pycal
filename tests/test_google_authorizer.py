import json

import pytest

from pycal.authorizer import GoogleAuthorizer


class DummyCredentials:
    def __init__(self, expired=None, refresh_token=None, client_id=None, client_secret=None):
        self.expired = expired
        self.refresh_token = refresh_token
        self.refreshed = False
        self.client_id = client_id
        self.client_secret = client_secret

    def refresh(self, *args, **kwargs):
        self.refreshed = True


@pytest.fixture
def authorizer():
    ga = GoogleAuthorizer(
        credentials_path='some/path.json',
        config_path='other/path.json',
    )
    return ga


@pytest.fixture
def credentials():
    credentials = DummyCredentials(
        expired=False,
        refresh_token='SomeToken',
        client_id='SomeId',
        client_secret='SomeSecret'
    )
    return credentials


def test_credentials_exist_not_expired(authorizer, credentials):
    authorizer._credentials = credentials

    result = authorizer.credentials

    assert result.refresh_token == 'SomeToken'
    assert not result.expired
    assert not result.refreshed


def test_credentials_exist_expired(authorizer, credentials):
    credentials.expired = True
    authorizer._credentials = credentials

    result = authorizer.credentials

    assert result.refresh_token == 'SomeToken'
    assert result.expired
    assert result.refreshed


def test_save_credentials(authorizer, credentials, tmpdir):
    p = tmpdir.mkdir('test').join('credentials.json')
    authorizer._credentials = credentials
    authorizer.credentials_path = p

    authorizer.save_credentials()

    result = json.loads(p.read())

    assert result['refresh_token'] == credentials.refresh_token
    assert result['client_id'] == credentials.client_id
    assert result['client_secret'] == credentials.client_secret
