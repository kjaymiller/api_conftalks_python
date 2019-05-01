import pytest
import api as service

@pytest.fixture
def api():
    return service.api


def test_base_url(api):
    r = api.requests.get('/')
    assert r.text == 'Hello from Conftalks'
