import sys
import os
from falcon import testing
import pytest
from base64 import b64encode

sys.path.append(os.getcwd())

from auction.auction import app

ITEM_ID = 999
JOHN_AUTH_DATA = b64encode(b"john:12345").decode("ascii")
JOHN_USER_ID = 1
OTTO_AUTH_DATA = b64encode(b"otto:54321").decode("ascii")


@pytest.fixture
def client():
    return testing.TestClient(app)


def test_api(client):
    response = make_bid(client, JOHN_AUTH_DATA, ITEM_ID)
    assert response.json == {'msg': 'Bid accepted'}
    response = make_bid(client, OTTO_AUTH_DATA, ITEM_ID)
    assert response.json == {'msg': 'Bid accepted'}
    response = get_winner(client, OTTO_AUTH_DATA, ITEM_ID)
    assert response.json == 'john'
    response = get_item_bids(client, OTTO_AUTH_DATA, ITEM_ID)
    assert response.json == ['john', 'otto']
    response = get_user_bids(client, JOHN_AUTH_DATA, JOHN_USER_ID)
    assert response.json == [999]


def make_bid(client, auth_data, item_id):
    return client.simulate_put(
        '/items/{0}/bids'.format(item_id),
        headers={'Authorization': 'Basic {0}'.format(auth_data)},
    )


def get_winner(client, auth_data, item_id):
    return client.simulate_get(
        '/items/{0}/winner'.format(item_id),
        headers={'Authorization': 'Basic {0}'.format(auth_data)},
    )


def get_item_bids(client, auth_data, item_id):
    return client.simulate_get(
        '/items/{0}/bids'.format(item_id),
        headers={'Authorization': 'Basic {0}'.format(auth_data)},
    )


def get_user_bids(client, auth_data, user_id):
    return client.simulate_get(
        '/users/{0}/bids'.format(user_id),
        headers={'Authorization': 'Basic {0}'.format(auth_data)},
    )
