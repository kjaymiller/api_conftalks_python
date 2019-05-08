import pytest
import api as service
import os

@pytest.fixture
def api():
    return service.api


def test_get_event(api):
    """TODO: Mock Database Call"""
    r = api.requests.get('/event/5cd10cc1bfda05ee8db8f5d9')
    assert r.status_code == 200


def test_subscribe_to_event(api):
    """TODO: Mock Database Call"""
    api_key='XbeYKnoRCaefcF6GD7jPVEO3KI0'
    headers = {'Authorization': api_key}

    r = api.requests.post('/event/5cd10cc1bfda05ee8db8f5d9/subscribe', headers=headers, json={'start': True, 'end': False})
    assert r.json()
