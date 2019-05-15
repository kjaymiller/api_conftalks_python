import pytest
import json
import api as service
import mongo

@pytest.fixture
def api():
    return service.api

def test_get_one_conference(mocker, api):
    """TODO: Mock Database Connection"""
#    mocker.patch('mongo.jsonify').return_value = {'email': 'kjaymiller@gmail.com', 'id':'5cbfa011127c6adabe9bfcb3'}
    r = api.requests.get('/conferences/5cbfa011127c6adabe9bfcb3')
    print(r.status_code)
    assert r.json()


#    def test_get_all_conferences(api):
#        """TODO: Mock Database Connection"""
#        r = api.requests.get('/conferences')
#        assert r.json()[0]['id'] == '5cbfa011127c6adabe9bfcb3'
