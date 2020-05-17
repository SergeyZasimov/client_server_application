import pytest
from datetime import datetime

from protocol import make_response

@pytest.fixture
def expected_code():
    return 200

@pytest.fixture
def expected_action():
    return 'Test'

@pytest.fixture
def expected_time():
    return datetime.now().timestamp()

@pytest.fixture
def expected_data():
    return 'Some client data'

@pytest.fixture
def initial_request(expected_action, expected_time, expected_data):
    return {
        'action': expected_action,
        'time': expected_time,
        'data': expected_data
    }

def test_action_make_response(initial_request, expected_action, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, expected_time)
    action = response.get('action')
    assert action == expected_action
