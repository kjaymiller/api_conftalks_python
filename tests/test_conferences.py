import pytest
import json
import api as service

@pytest.fixture
def api():
    return service.api


def test_get_all_conferences(api):
    """TODO: Mock Database Connection"""
    r = api.requests.get('/conferences')
    assert r.json()[0]['_id'] == {'$oid': '5cbfa011127c6adabe9bfcb3'}


