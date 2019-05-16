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
    return service.api


def gen_fake_conference_data():
    name = fake.company() + 'Con' 
    _id = fake.password(length=13, special_chars=False)
    fake_start_datetime = maya.when(
            str(fake.future_date(end_date="+1y")),
            timezone=fake.timezone())
    fake_end_datetime = fake_start_datetime.add(days=randint(1,365))

    event_data = {
            'id': _id, 
            'name': name,
            'organizers': map(fake.company_email(), range(randint(0,5))),
            'event_start': fake_start_datetime.rfc2822(),
            'event_end': fake_end_datetime.rfc2822(),
            }

    return event_data

@pytest.fixture()
def fake_conference_data():
    return gen_fake_conference_data()

@pytest.fixture
def mocked_db_get_many():
    mocks = map(lambda x: gen_fake_conference_data(), range(randint(2,10)))
    return list(mocks)

def mocked_db_post():
    pass

def mocked_db_update():
    pass
     
def test_get_one_conference(api, mocker, fake_conference_data):
    _id = fake_conference_data['id']
    name = fake_conference_data['name']
    
    mocker.patch(
        'conferences.get_db_data', 
        lambda x, _id: fake_conference_data, 
        )
    r = api.requests.get(f'/conferences/{_id}')
    print(r.json())
    assert r.json()['id'] == _id
    assert r.json()['name'] == name


def test_get_all_conferences(api, mocker, mocked_db_get_many):
    mocker.patch(
            'conferences.get_db_data',
            lambda x: mocked_db_get_many,
            )

    r = api.requests.get('/conferences')
    for x, row in enumerate(r.json()):
        assert row['id'] == mocked_db_get_many[x]['_id']
