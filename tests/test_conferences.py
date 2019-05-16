import pytest
import api as service 
import conferences
import mongo
from random import randint
from faker import Faker


fake = Faker()


@pytest.fixture
def api():
    return service.api


def gen_fake_conference():
    name = fake.company() + 'Con' 
    _id = fake.password(length=13, special_chars=False) 
    return {'name': name, '_id': {'$oid':_id}}


@pytest.fixture
def mocked_db_get_many():
    mocks = map(lambda x: gen_fake_conference(), range(randint(2,10)))
    return list(mocks)

     
def test_get_one_conference(api, mocker):
    fake_data = gen_fake_conference()
    _id = fake_data['_id']['$oid']
    name = fake_data['name']
    
    mocker.patch(
        'conferences.get_db_data', 
        lambda x, _id: fake_data, 
        )
    r = api.requests.get(f'/conferences/{_id}')
    assert r.json()['id'] == _id
    assert r.json()['name'] == name


def test_get_all_conferences(api, mocker, mocked_db_get_many):
    mocker.patch(
            'conferences.get_db_data',
            lambda x: mocked_db_get_many,
            )

    r = api.requests.get('/conferences')
    assert r.json()[1]['id'] == mocked_db_get_many[1]['_id']['$oid']

