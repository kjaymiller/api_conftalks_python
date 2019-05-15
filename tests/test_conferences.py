import pytest
import api as service 
import conferences
import mongo

@pytest.fixture
def api():
    return service.api

def test_get_one_conference(api, mocker, faker):
    """TODO: Mock Database Connection"""
    name = faker.company() 
    id = faker.password(length=13) 
    mocker.patch.object('conferences.get_db_data', lambda:{'name': name, '_id': id})
    r = api.requests.get('/conferences/5cbfa011127c6adabe9bfcb3')


#    def test_get_all_conferences(api):
#        """TODO: Mock Database Connection"""
#        r = api.requests.get('/conferences')
#        assert r.json()[0]['id'] == '5cbfa011127c6adabe9bfcb3'
