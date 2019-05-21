import pytest
import api as service
from faker import Faker
import conferences
import mongo
from bson.objectid import ObjectId
from random import randint, choice
from faker import Faker
import maya
import json


fake = Faker()

@pytest.fixture
def api():
    """The Base call of our API, it replaces having to run the api and then test by making requests"""
    return service.api


def gen_fake_conference():
    name = fake.company() + 'Con'
    _id =  str(ObjectId())
    fake_start_datetime = maya.when(
            str(fake.future_date(end_date="+1y")),
            timezone=fake.timezone())
    fake_end_datetime = fake_start_datetime.add(days=randint(1,365))

    event_data = {
            'id': _id,
            'name': name,
            'organizers': [fake.company_email() for x in  range(randint(0,5))],
            'event_start': fake_start_datetime.rfc2822(),
            'event_end': fake_end_datetime.rfc2822(),
            }

    return event_data

@pytest.fixture
def fake_conference():
    return gen_fake_conference()

def test_conference_data_variables():
    pass

def test_get_one_conference(api, mocker, fake_conference):
    """Generate Fake Data and simulate returning it"""
    _id = fake_conference['id']
    name = fake_conference['name']

    mocker.patch(
        'conferences.get_db_data',
        lambda **kwargs: fake_conference,
        )

    r = api.requests.get(f'/conferences/{_id}')
    print(r.json())
    assert r.json() # Will fail if no json data is passed
    assert r.json()['id'] == _id # pulls just the ID as a string and NOT AS A DICT
    assert r.json()['name'] == name

@pytest.fixture
def mocked_db_get_many():
    """Generates a random amount of fake data"""
    mocks = [gen_fake_conference() for x in range(randint(5,15))] # Creates between 2-10 Items
    return mocks


def test_get_all_conferences(api, mocker, mocked_db_get_many):
    mocker.patch(
            'conferences.get_db_data',
            lambda **kwargs: mocked_db_get_many,
            )

    r = api.requests.get('/conferences')
    assert r.json()
    assert len(r.json()) == len(mocked_db_get_many)

def test_get_some_conferences(api, mocker, mocked_db_get_many):
    mocker.patch(
            'conferences.find',
            lambda **kwargs: mocked_db_get_many,
            )
    limit = randint(4, len(mocked_db_get_many)-1)

    params = {'limit': limit}
    r = api.requests.get('/conferences', params=params)
    assert r.json()
    assert len(r.json()) == limit

# def test_mocked_db_post():
    # TODO: mock adding fake data to the database
    # TODO: mock retrieving that data

# def mocked_db_update():
    # TODO: mock fetching data and updating it with the find_one_and_update call
