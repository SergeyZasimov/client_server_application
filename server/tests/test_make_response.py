import pytest
from datetime import datetime

from protocol import make_response

CODE = 200

DATA = 'Some client data'

ACTION = 'test'

DATE = datetime.now().timestamp()

REQUEST = {
    'action': ACTION,
    'time': DATE,
    'data': DATA,
}

RESPONSE = {
    'action': 'test',
    'time': DATE,
    'code': CODE,
    'data': DATA,
}

def test_make_response():
    response = make_response(REQUEST, CODE, DATA, date=DATE)
    assert response == RESPONSE

def test_action_make_response():
    response = make_response(REQUEST, CODE, date=DATE)
    action = response.get('action')
    assert action == ACTION

def test_invalid_make_response():
    with pytest.raises(AttributeError):
        make_response(None, CODE)