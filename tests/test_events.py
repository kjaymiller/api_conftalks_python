import pytest
import api as service
import os

@pytest.fixture
def api():
    return service.api


def test_add_event(api):
    
    r = api.requests.post('/event')


def test_get_event(api):
    """TODO: Mock Database Call"""
    r = api.requests.get('/event/5cccb212ac5b0e0c0c4a46ce')
    assert r.json()['_id'] == {'$oid': '5cccb212ac5b0e0c0c4a46ce'}

def test_subscribe_to_event(api):
    """TODO: Mock Database Call"""
    api_key='XbeYKnoRCaefcF6GD7jPVEO3KI0'
    headers = {'Authorization': api_key}

    r = api.requests.post('/event/5cc905e48acb082e9712a9e3/subscribe', headers=headers, json={'start': True, 'end': False})
    assert r.json()
