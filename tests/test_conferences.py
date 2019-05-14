import pytest
import json
import api as service
from mongo import get_db_data

@pytest.fixture
def api():
    return service.api

def test_get_one_conference(mocker, api):
    """TODO: Mock Database Connection"""
    mocker.patch(
            'mongo.get_db_data', 
            print('hi!!')
            )
    r = api.requests.get('/conferences/8675309')
    assert r.json()['id'] == '5cbfa011127c6adabe9bfcb3'


#    def test_get_all_conferences(api):
#        """TODO: Mock Database Connection"""
#        r = api.requests.get('/conferences')
#        assert r.json()[0]['id'] == '5cbfa011127c6adabe9bfcb3'
