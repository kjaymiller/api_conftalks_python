import pytest
import api as service 
from faker import Faker
import conferences
import mongo
from random import randint, choice
from faker import Faker
import maya


fake = Faker()

@pytest.fixture
def api():
    """The Base call of our API, it replaces having to run the api and then test by making requests"""
    return service.api


def gen_fake_conference_data():
    """Create Conference Data. This replaces querying the Mongo Database"""
    name = fake.company() + 'Con' 
    _id = fake.password(length=13, special_chars=False)
    fake_start_datetime = maya.when(
            str(fake.future_date(end_date="+1y")),
            timezone=fake.timezone())
    fake_end_datetime = fake_start_datetime.add(days=randint(1,365))

    event_data = {
            'id': {'$oid': _id},
            'name': name,
            'organizers': map(fake.company_email(), range(randint(0,5))),
            'event_start': fake_start_datetime.rfc2822(),
            'event_end': fake_end_datetime.rfc2822(),
            }

    return event_data

@pytest.fixture()
def fake_conference_data():
    """Calls the fake conference data as a fixture"""
    return gen_fake_conference_data()

@pytest.fixture
def mocked_db_get_many():
    """Generates a random amount of fake data"""
    mocks = [gen_fake_conference_data() for x in range(randint(2,10))] # Creates between 2-10 Items
    return mocks

     
def test_get_one_conference(api, mocker, fake_conference_data):
    """Generate Fake Data and simulate returning it"""
    _id = fake_conference_data['id']['$oid'] # a dict by default id = {'$oid': '8675309'}
    name = fake_conference_data['name']
    
    mocker.patch(
        'conferences.get_one_conference', 
        lambda **kwargs: fake_conference_data, 
        )

    r = api.requests.get(f'/conferences/{_id}')
    assert r.json() # Will fail if no json data is passed
    assert r.json()['id'] == _id # pulls just the ID as a string and NOT AS A DICT
    assert r.json()['name'] == name


def test_get_all_conferences(api, mocker, mocked_db_get_many):
    mocker.patch(
            'conferences.get_many_conferences',
            lambda **kwargs: mocked_db_get_many,
            )

    r = api.requests.get('/conferences')
    assert r.json()
    assert len(r.json()) == len(mocked_db_update)

# def test_mocked_db_post(): 
    # TODO: mock adding fake data to the database
    # TODO: mock retrieving that data

# def mocked_db_update():
    # TODO: mock fetching data and updating it with the find_one_and_update call
