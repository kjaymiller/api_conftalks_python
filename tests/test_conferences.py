import pytest
import json
import api as service

@pytest.fixture
def api():
    return service.api


def test_get_one_conference(api):
    """TODO: Mock Database Connection"""
    r = api.requests.get('/conferences/5cbfa011127c6adabe9bfcb3')
    print(r.json())
    assert r.json()['id'] == '5cbfa011127c6adabe9bfcb3'


def test_get_all_conferences(api):
    """TODO: Mock Database Connection"""
    r = api.requests.get('/conferences')
    print(r.json())
    assert r.json()[0][0]['id'] == '5cbfa011127c6adabe9bfcb3'
