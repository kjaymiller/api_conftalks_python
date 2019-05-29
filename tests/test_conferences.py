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
from itertools import product


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
    fake_tags = fake.words(nb=randint(1,5), unique=True)

    event_data = {
            'id': _id,
            'name': name,
            'organizers': [fake.company_email() for x in  range(randint(0,5))],
            'event_start': fake_start_datetime.rfc2822(),
            'event_end': fake_end_datetime.rfc2822(),
            'tags': fake_tags,
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
    assert r.json() # Will fail if no json data is passed
    assert r.json()['id'] == _id # pulls just the ID as a string and NOT AS A DICT
    assert r.json()['name'] == name

@pytest.fixture
def mocked_db_get_many():
    """Generates a random amount of fake data"""
    mocks = [gen_fake_conference() for x in range(randint(5,15))] # Creates between 5-15 Items
    return mocks


def test_get_all_conferences(api, mocker, mocked_db_get_many):
    mocker.patch('conferences.get_db_data', lambda **kwargs: mocked_db_get_many)
    r = api.requests.get('/conferences')
    assert len(r.json()) == len(mocked_db_get_many)


def test_get_some_conferences_sees_limit(api, mocker, mocked_db_get_many):
    m = mocker.patch('conferences.get_db_data')
    limit = randint(4, len(mocked_db_get_many)-1)
    payload = {'limit': limit}
    r = api.requests.get('/conferences', params=payload)
    _, kwargs = m.call_args
    assert kwargs['limit'][0] == str(limit)


def test_get_some_conferences_sees_sort(api, mocker, mocked_db_get_many):
    m = mocker.patch('conferences.get_db_data')
    sorter = ('asc', 'desc')
    date_variable = ('start_date', 'end_date')

    for sort in product(date_variable, sorter, repeat=1):
        payload = {
                'sort_by': sort[0],
                'order_by': sort[1],
                }

        r = api.requests.get('/conferences', params=payload)
        _, kwargs = m.call_args
        assert kwargs['sort_by'][0] == sort[0]
        assert kwargs['order_by'][0] == sort[1]


def test_get_filters_for_tags(mocked_db_get_many):
    tags = choice(mocked_db_get_many)['tags']
    search_tag = choice(tags)
    payload1 = {'filter': f'tags eq {search_tag}'}
    payload2 = {'filter': f'tags ne {search_tag}'}
    assert conferences.get_filter(payload1['filter']) == {'tags': {'$eq': search_tag}}
    assert conferences.get_filter(payload2['filter']) == {'tags': {'$ne': search_tag}}


@pytest.mark.parameterize('filter_type', ['eq', 'ne', 'lt', 'gt', 'ge', 'le'])
def test_get_filters_for_dates(mocked_db_get_many):
    date_choice = choice('event_start', 'event_end')
    dates = choice(mocked_db_get_many)[date_choice]
    payload = {'filter': f'{date_choice} {filter_type} dates'}
    assert conferences.get_filter(payload)


def test_get_some_conferences_with_filtered_tags(api, mocker, mocked_db_get_many):
    m = mocker.patch('conferences.get_db_data')
    tags = choice(mocked_db_get_many)['tags']
    search_tag = choice(tags)
    payload = {'filter': f'tags eq {search_tag}'}
    r = api.requests.get('/conferences', params=payload)
    _, kwargs = m.call_args
    print(kwargs)
    assert kwargs['filter_by'] == {'tags': {'$eq': search_tag}}


# def test_mocked_db_post():
    # TODO: mock adding fake data to the database
    # TODO: mock retrieving that data

# def mocked_db_update():
    # TODO: mock fetching data and updating it with the find_one_and_update
