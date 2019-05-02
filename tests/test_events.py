import pytest
import api as service
import os

@pytest.fixture
def api():
    return service.api


def test_get_event(api):
    """TODO: Mock Database Call"""
    r = api.requests.get('/event/5cc905e48acb082e9712a9e3')
    assert r.json()['_id'] == {'$oid': '5cc905e48acb082e9712a9e3'}

def test_subscribe_to_event(api):
    """TODO: Mock Database Call"""
    api_key='XbeYKnoRCaefcF6GD7jPVEO3KI0'
    headers = {'Authorization': api_key}

    r = api.requests.post('/event/5cc905e48acb082e9712a9e3/subscribe', headers=headers, json={'start': True, 'end': False})
    assert r.json()
